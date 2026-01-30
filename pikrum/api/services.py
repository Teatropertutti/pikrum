from django.conf import settings
from django.db.models import F
from .models import Feature, CatalogedImage, ImageDetection
from .ai_modules.image_analyzer import analyze_and_split_image, _execute_core_analysis
from .ai_modules.embeddings import get_text_embedding, get_image_embedding

def process_new_image_upload(image_file, is_reference_upload=False):
    """
    Gestisce l'ingestione:
    - Se Reference: Analisi singola (100% foto).
    - Se Catalogo: Detection e scomposizione.
    """
    config = settings.VERTEX_AI_CONFIG
    project_id = config["PROJECT_ID"]
    location = config["LOCATION"]

    # 1. Recupero tassonomia per guidance
    features = Feature.objects.prefetch_related('values').all()
    taxonomy_guidance = {f.name: [v.value for v in f.values.all()] for f in features}

    # 2. Lettura byte
    image_bytes = image_file.read()
    image_file.seek(0) 

    # 3. Salvataggio Immagine Fisica
    main_image = CatalogedImage.objects.create(
        image_file=image_file,
        original_name=image_file.name,
        title=f"{'REF' if is_reference_upload else 'CAT'}: {image_file.name}"
    )

    # 4. Bivio: Reference vs Catalogo
    if is_reference_upload:
        # Analisi singola sull'intera immagine
        analysis = _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance)
        
        ImageDetection.objects.create(
            parent_image=main_image,
            label=analysis.get('title', 'Reference'),
            ai_description=analysis['long_description'],
            generated_tags=analysis['tags'],
            is_reference=True,
            is_verified=True,
            bounding_box=[0, 0, 1000, 1000],
            embedding_vector=analysis['embedding']
        )
    else:
        # Scomposizione in oggetti
        analyses = analyze_and_split_image(image_bytes, taxonomy_guidance)
        for result in analyses:
            ImageDetection.objects.create(
                parent_image=main_image,
                label=result.get('detected_label', 'Oggetto'),
                ai_description=result['long_description'],
                generated_tags=result['tags'],
                is_reference=False,
                is_verified=False,
                bounding_box=result.get('box_2d'),
                embedding_vector=result['embedding']
            )

    return main_image

def search_by_text(query_text):
    """Ricerca semantica partendo da testo"""
    config = settings.VERTEX_AI_CONFIG
    query_vector = get_text_embedding(query_text, config["PROJECT_ID"], config["LOCATION"])
    
    return _execute_vector_search(query_vector)

def search_by_image(image_file):
    """Ricerca semantica partendo da un'immagine di riferimento"""
    config = settings.VERTEX_AI_CONFIG
    image_bytes = image_file.read()
    
    query_vector = get_image_embedding(image_bytes, config["PROJECT_ID"], config["LOCATION"])
    
    return _execute_vector_search(query_vector)

def _execute_vector_search(query_vector):
    """Logica comune di ricerca vettoriale sui ponti (detections)"""
    # Cerchiamo tra tutte le detections, dando priorità a quelle che non sono reference 
    # (per trovare il prodotto nel catalogo reale)
    results = ImageDetection.objects.select_related('parent_image').annotate(
        distance=F('embedding_vector').cosine_distance(query_vector)
    ).order_by('distance')[:10]
    
    return results