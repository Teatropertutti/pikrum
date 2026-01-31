import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part
from django.conf import settings

def get_image_metadata(image_bytes, project_id, location, taxonomy_guidance=None):
    # Recuperiamo la chiave API dai settaggi che abbiamo configurato prima
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    
    # Inizializziamo Vertex AI passando esplicitamente la API_KEY.
    # Questo evita l'errore DefaultCredentialsError.
    vertexai.init(
        project=project_id, 
        location=location,
        api_key=api_key
    )
    
    model = GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    Sei un esperto catalogatore museale. Analizza l'immagine e restituisci SOLO un JSON:
    {
      "title": "max 60 caratteri",
      "long_description": "circa 300 caratteri",
      "tags": ["tag1", "tag2"]
    }
    """
    if taxonomy_guidance:
        prompt += f"\nUsa questi tag se pertinenti: {taxonomy_guidance}"

    # Chiamata al modello
    response = model.generate_content([
        Part.from_data(data=image_bytes, mime_type="image/jpeg"),
        prompt
    ])
    
    # Pulizia dell'output per evitare errori di parsing JSON
    text_response = response.text
    clean_json = text_response.replace('```json', '').replace('```', '').strip()
    
    try:
        return json.loads(clean_json)
    except json.JSONDecodeError:
        # Fallback nel caso l'AI aggiunga testo extra non previsto
        import re
        json_match = re.search(r'\{.*\}', clean_json, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
        raise Exception("L'AI ha restituito un formato non valido")