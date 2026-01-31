import google.generativeai as genai
import json
from django.conf import settings

def detect_objects_in_image(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    # AGGIORNATO: gemini-2.5-flash
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = "Individua gli oggetti. Restituisci solo JSON: [{\"box_2d\": [ymin, xmin, ymax, xmax], \"label\": \"nome\"}]"
    
    try:
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ])
        clean_json = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_json)
    except:
        return []