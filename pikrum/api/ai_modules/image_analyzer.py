from django.conf import settings
from .vision import get_image_metadata
from .embeddings import get_image_embedding
from .detection import detect_objects_in_image 
from io import BytesIO
from PIL import Image

def _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance):
    """Chiama vision ed embeddings per un singolo ritaglio."""
    
    # 1. Costruzione guidance
    formatted_guidance = ""
    if taxonomy_guidance:
        formatted_guidance = "\nBASATI SUI SEGUENTI DATI ESISTENTI:\n"
        for feature, tags in taxonomy_guidance.items():
            formatted_guidance += f"- {feature}: {', '.join(tags)}\n"

    # 2. Analisi Metadati (Gemini puro)
    metadata = get_image_metadata(
        image_bytes, 
        project_id, 
        location, 
        taxonomy_guidance=formatted_guidance
    )
    
    # 3. Analisi Vettoriale
    vector = get_image_embedding(image_bytes, project_id, location)
    
    return {
        "title": metadata.get('title', 'Senza Titolo'),
        "long_description": metadata.get('long_description', 'Nessuna descrizione.'),
        "tags": metadata.get('tags', []),
        "embedding": vector
    }

def analyze_and_split_image(image_bytes, taxonomy_guidance=None):
    """Orchestratore: rileva oggetti, ritaglia e analizza."""
    config = settings.VERTEX_AI_CONFIG
    project_id = config.get("PROJECT_ID")
    location = config.get("LOCATION")

    # Rilevamento oggetti
    objects = detect_objects_in_image(image_bytes, project_id, location)
    
    results = []
    
    if not objects:
        analysis = _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance)
        results.append(analysis)
    else:
        img = Image.open(BytesIO(image_bytes))
        width, height = img.size
        
        for obj in objects:
            try:
                ymin, xmin, ymax, xmax = obj['box_2d']
                left, top = xmin * width / 1000, ymin * height / 1000
                right, bottom = xmax * width / 1000, ymax * height / 1000
                
                crop = img.crop((left, top, right, bottom))
                crop_io = BytesIO()
                crop.save(crop_io, format='JPEG')
                crop_bytes = crop_io.getvalue()
                
                analysis = _execute_core_analysis(crop_bytes, project_id, location, taxonomy_guidance)
                analysis['detected_label'] = obj.get('label', 'oggetto')
                results.append(analysis)
            except Exception as e:
                print(f"Errore nel ritaglio oggetto: {e}")
                
    return results