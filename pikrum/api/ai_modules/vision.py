import json
import base64
import requests
from django.conf import settings

def get_image_metadata(image_bytes, project_id, location, taxonomy_guidance=None):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    image_base64 = base64.b64encode(image_bytes).decode('utf-8')
    
    prompt = "Sei un esperto catalogatore. Analizza l'immagine e restituisci SOLO un JSON: {\"title\": \"...\", \"long_description\": \"...\", \"tags\": []}"
    
    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": image_base64}}
            ]
        }]
    }
    
    response = requests.post(url, json=payload)
    res_json = response.json()
    
    try:
        text = res_json['candidates'][0]['content']['parts'][0]['text']
        clean = text.strip().replace('```json', '').replace('```', '').strip()
        return json.loads(clean)
    except:
        return {"title": "Oggetto Rilevato", "long_description": "Descrizione non disponibile", "tags": []}