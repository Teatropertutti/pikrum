from django.conf import settings
from .vision import get_image_metadata
from .embeddings import get_image_embedding
from .detection import detect_objects_in_image 
from io import BytesIO
from PIL import Image

def _execute_core_analysis(image_bytes, project_id, location, taxonomy_guidance):
    metadata = get_image_metadata(image_bytes, project_id, location, taxonomy_guidance)
    vector = get_image_embedding(image_bytes, project_id, location)
    
    return {
        "title": metadata.get('title', 'Senza Titolo'),
        "long_description": metadata.get('long_description', 'Descrizione non disponibile.'),
        "tags": metadata.get('tags', []),
        "embedding": vector
    }

def analyze_and_split_image(image_bytes, taxonomy_guidance=None):
    config = settings.VERTEX_AI_CONFIG
    p_id = config.get("PROJECT_ID")
    loc = config.get("LOCATION")

    # 1. Trova oggetti
    objects = detect_objects_in_image(image_bytes, p_id, loc)
    results = []
    
    if not objects:
        results.append(_execute_core_analysis(image_bytes, p_id, loc, taxonomy_guidance))
    else:
        img = Image.open(BytesIO(image_bytes))
        for obj in objects:
            try:
                ymin, xmin, ymax, xmax = obj['box_2d']
                left = xmin * img.width / 1000
                top = ymin * img.height / 1000
                right = xmax * img.width / 1000
                bottom = ymax * img.height / 1000
                
                crop_io = BytesIO()
                img.crop((left, top, right, bottom)).save(crop_io, format='JPEG')
                results.append(_execute_core_analysis(crop_io.getvalue(), p_id, loc, taxonomy_guidance))
            except:
                continue
    return results