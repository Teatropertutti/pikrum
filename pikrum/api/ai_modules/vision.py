import json
from genai import Client
from django.conf import settings

def get_image_metadata(image_bytes, project_id, location, taxonomy_guidance=None):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    
    # Nuovo client della libreria 2026
    client = Client(api_key=api_key)
    
    prompt = """
    Sei un esperto catalogatore. Analizza l'immagine e restituisci SOLO un JSON:
    {
      "title": "nome prodotto",
      "long_description": "descrizione accurata",
      "tags": ["tag1", "tag2"]
    }
    """
    
    # Utilizziamo gemini-2.0-flash come da documentazione aggiornata
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[
            {"mime_type": "image/jpeg", "data": image_bytes},
            prompt
        ]
    )
    
    try:
        # La nuova libreria restituisce l'oggetto in modo più diretto
        return json.loads(response.text.strip().strip('```json').strip('```'))
    except:
        import re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else {}