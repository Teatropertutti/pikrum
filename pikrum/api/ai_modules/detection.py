import json
from genai import Client
from django.conf import settings

def detect_objects_in_image(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    client = Client(api_key=api_key)
    
    prompt = "Individua gli oggetti. Restituisci solo JSON: [{\"box_2d\": [ymin, xmin, ymax, xmax], \"label\": \"nome\"}]"
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[{"mime_type": "image/jpeg", "data": image_bytes}, prompt]
        )
        clean_json = response.text.strip().strip('```json').strip('```')
        return json.loads(clean_json)
    except:
        return []