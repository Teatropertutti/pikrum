import google.generativeai as genai
import json
from django.conf import settings

def detect_objects_in_image(image_bytes, project_id, location):
    # Recupero API Key dai settings
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    Individua gli oggetti principali in questa immagine. 
    Per ogni oggetto, restituisci un JSON con il nome dell'oggetto e le coordinate box 2D 
    nel formato [ymin, xmin, ymax, xmax] normalizzato (0-1000).
    Restituisci solo una lista JSON: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "nome_oggetto"}]
    """
    
    try:
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ])
        
        # Pulizia dell'output
        text_response = response.text.strip()
        clean_json = text_response.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except Exception as e:
        print(f"Errore in detection: {e}")
        return []