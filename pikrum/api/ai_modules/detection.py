import json
import base64
import requests
from django.conf import settings

def detect_objects_in_image(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    prompt = "Individua gli oggetti. Restituisci solo JSON: [{\"box_2d\": [ymin, xmin, ymax, xmax], \"label\": \"nome\"}]"
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
            ]
        }]
    }
    
    response = requests.post(url, json=payload)
    try:
        text = response.json()['candidates'][0]['content']['parts'][0]['text']
        clean = text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(clean)
    except:
        return []