import json
import google.generativeai as genai
from django.conf import settings

def get_image_metadata(image_bytes, project_id, location, taxonomy_guidance=None):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    # AGGIORNATO: Usiamo il codice modello visto nel tuo screenshot
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = """
    Analizza l'immagine e restituisci SOLO un JSON:
    {
      "title": "nome prodotto",
      "long_description": "descrizione accurata",
      "tags": ["tag1", "tag2"]
    }
    """
    
    # Chiamata ottimizzata per Gemini 2.5+
    response = model.generate_content([
        {"mime_type": "image/jpeg", "data": image_bytes},
        prompt
    ])
    
    try:
        clean_json = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_json)
    except:
        import re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        return json.loads(match.group()) if match else {}