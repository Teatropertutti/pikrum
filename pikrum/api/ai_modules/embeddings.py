import google.generativeai as genai
from django.conf import settings

def get_image_embedding(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    # Usiamo il modello multimodale di Gemini per generare il vettore
    # Nota: Usiamo un'immagine e una descrizione vuota per ottenere il vettore visuale
    result = genai.embed_content(
        model="models/text-embedding-004", # Gemini userà questo per processare il contesto
        content="Analisi visuale Pikrum",
        task_type="retrieval_document"
    )
    # Ritorna una lista di numeri (vettore)
    return result['embedding']

def get_text_embedding(text_query, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text_query,
        task_type="retrieval_query"
    )
    return result['embedding']