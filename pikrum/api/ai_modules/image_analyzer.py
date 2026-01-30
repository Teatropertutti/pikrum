from django.conf import settings
from .vision import get_image_metadata
from .embeddings import get_image_embedding
from .detection import detect_objects_in_image 
from io import BytesIO
from PIL import Image

def _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance):
    """
    LOGICA REALE: Chiama vision ed embeddings per un singolo frame.
    """
    # 1. Costruzione guidance testuale
    formatted_guidance = ""
    if taxonomy_guidance:
        formatted_guidance = "\nBASATI SUI SEGUENTI DATI ESISTENTI:\n"
        for feature, tags in taxonomy_guidance.items():
            formatted_guidance += f"- {feature}: {', '.join(tags)}\n"

    # 2. Analisi Metadati (Gemini)
    metadata = get_image_metadata(
        image_bytes, 
        project_id, 
        location, 
        taxonomy_guidance=formatted_guidance
    )
    
    # 3. Analisi Vettoriale (Embeddings)
    vector = get_image_embedding(image_bytes, project_id, location)
    
    return {
        "title": metadata.get('title', 'Senza Titolo'),
        "long_description": metadata.get('long_description', 'Nessuna descrizione generata.'),
        "tags": metadata.get('tags', []),
        "embedding": vector
    }

def analyze_and_split_image(image_bytes, taxonomy_guidance=None):
    """
    ORCHESTRATORE: Decide se analizzare l'immagine intera o i singoli oggetti.
    """
    config = settings.VERTEX_AI_CONFIG
    project_id = config["PROJECT_ID"]
    location = config["LOCATION"]

    # 1. Identifica gli oggetti
    objects = detect_objects_in_image(image_bytes, project_id, location)
    
    results = []
    
    if not objects:
        # Nessun oggetto trovato: analizza l'immagine intera
        analysis = _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance)
        results.append(analysis)
    else:
        # Ritagliamo e analizziamo ogni oggetto
        img = Image.open(BytesIO(image_bytes))
        width, height = img.size
        
        for obj in objects:
            try:
                ymin, xmin, ymax, xmax = obj['box_2d']
                
                # Calcolo pixel reali
                left, top = xmin * width / 1000, ymin * height / 1000
                right, bottom = xmax * width / 1000, ymax * height / 1000
                
                # Ritaglio in memoria
                crop = img.crop((left, top, right, bottom))
                crop_io = BytesIO()
                crop.save(crop_io, format='JPEG')
                crop_bytes = crop_io.getvalue()
                
                # Analisi del ritaglio
                analysis = _execute_core_analysis(crop_bytes, project_id, location, taxonomy_guidance)
                analysis['detected_label'] = obj.get('label', 'oggetto')
                results.append(analysis)
            except Exception as e:
                print(f"Errore nel ritaglio: {e}")
                continue
                
    return results