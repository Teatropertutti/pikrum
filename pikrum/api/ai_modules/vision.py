import json
import vertexai
from vertexai.generative_models import GenerativeModel, Part

def get_image_metadata(image_bytes, project_id, location, taxonomy_guidance=None):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-1.5-flash")
    
    prompt = """
    Sei un esperto catalogatore museale. Analizza l'immagine e restituisci un JSON:
    {
      "title": "max 60 caratteri",
      "long_description": "circa 300 caratteri",
      "tags": ["tag1", "tag2"]
    }
    """
    if taxonomy_guidance:
        prompt += f"\nUsa questi tag se pertinenti: {taxonomy_guidance}"

    response = model.generate_content([
        Part.from_data(data=image_bytes, mime_type="image/jpeg"),
        prompt
    ])
    
    clean_json = response.text.replace('```json', '').replace('```', '').strip()
    return json.loads(clean_json)