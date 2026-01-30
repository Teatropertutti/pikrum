import vertexai
from vertexai.generative_models import GenerativeModel, Part
import json

def detect_objects_in_image(image_bytes, project_id, location):
    vertexai.init(project=project_id, location=location)
    model = GenerativeModel("gemini-1.5-flash")
    
    # Prompt specifico per ottenere le coordinate degli oggetti
    prompt = """
    Individua gli oggetti principali in questa immagine. 
    Per ogni oggetto, restituisci un JSON con il nome dell'oggetto e le coordinate box 2D 
    nel formato [ymin, xmin, ymax, xmax] normalizzato (0-1000).
    Restituisci solo una lista JSON: [{"box_2d": [ymin, xmin, ymax, xmax], "label": "nome_oggetto"}]
    """
    
    response = model.generate_content([
        Part.from_data(data=image_bytes, mime_type="image/jpeg"),
        prompt
    ])
    
    try:
        clean_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(clean_json)
    except:
        return [] # Se fallisce, restituisce lista vuota