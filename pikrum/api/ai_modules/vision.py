import json
import google.generativeai as genai
from django.conf import settings

def get_image_metadata(image_bytes, project_id, location, taxonomy_guidance=None):
    # Prendiamo la chiave che hai messo nelle variabili di Railway
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    
    # Configuriamo Gemini direttamente
    genai.configure(api_key=api_key)
    
    # Selezioniamo il modello più veloce ed economico per le immagini
    model = genai.GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    Sei un esperto catalogatore. Analizza l'immagine e restituisci SOLO un JSON:
    {
      "title": "nome prodotto",
      "long_description": "descrizione accurata",
      "tags": ["tag1", "tag2"]
    }
    """
    if taxonomy_guidance:
        prompt += f"\nUsa questi tag se pertinenti: {taxonomy_guidance}"

    # Chiamata diretta (non serve più Part.from_data di vertexai)
    response = model.generate_content([
        {"mime_type": "image/jpeg", "data": image_bytes},
        prompt
    ])
    
    try:
        # Puliamo il testo da eventuali ```json ... ```
        clean_json = response.text.strip().removeprefix("```json").removesuffix("```").strip()
        return json.loads(clean_json)
    except Exception as e:
        # Se l'AI chiacchiera troppo, cerchiamo il JSON tra le parentesi graffe
        import re
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise Exception(f"Errore parsing AI: {str(e)}")