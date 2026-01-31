import google.generativeai as genai
import json
from django.conf import settings

def detect_objects_in_image(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    Individua gli oggetti principali in questa immagine. 
    Restituisci solo una lista JSON: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "nome_oggetto"}]
    Le coordinate box 2D devono essere nel formato normalizzato (0-1000).
    """
    
    try:
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ])
        clean_json = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_json)
    except:
        return []