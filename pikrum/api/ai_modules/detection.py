import json
import google.generativeai as genai
from django.conf import settings

def detect_objects_in_image(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    
    prompt = "Individua gli oggetti. Restituisci solo JSON: [{\"box_2d\": [ymin, xmin, ymax, xmax], \"label\": \"nome\"}]"
    
    try:
        response = model.generate_content([
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ])
        return json.loads(response.text.strip().strip('```json').strip('```'))
    except:
        return []