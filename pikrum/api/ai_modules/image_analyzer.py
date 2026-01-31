from django.conf import settings
from .vision import get_image_metadata
from .embeddings import get_image_embedding
from .detection import detect_objects_in_image 
from io import BytesIO
from PIL import Image

def _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance):
    # Rimuoviamo la necessità di passare project_id/location se vision.py e embeddings.py 
    # pescano già tutto da settings.py, ma li teniamo per compatibilità con la firma
    metadata = get_image_metadata(image_bytes, project_id, location, taxonomy_guidance)
    vector = get_image_embedding(image_bytes, project_id, location)
    
    return {
        "title": metadata.get('title', 'Senza Titolo'),
        "long_description": metadata.get('long_description', 'Nessuna descrizione.'),
        "tags": metadata.get('tags', []),
        "embedding": vector
    }

def analyze_and_split_image(image_bytes, taxonomy_guidance=None):
    config = settings.VERTEX_AI_CONFIG
    p_id = config.get("PROJECT_ID")
    loc = config.get("LOCATION")

    # Logica di scomposizione... (Il resto del tuo codice originale va bene)
    # [Mantieni il resto della tua funzione originale qui]