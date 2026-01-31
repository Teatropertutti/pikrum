import google.generativeai as genai
from django.conf import settings

def get_image_embedding(image_bytes, project_id, location):
    """
    Genera il vettore (embedding) per un'immagine.
    Nota: Con l'SDK google-generativeai, l'embedding multimodale diretto 
    è gestito diversamente da Vertex. Usiamo un placeholder testuale 
    per mantenere la compatibilità della struttura finché non integri 
    il modello multimodale specifico.
    """
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    # Per ora generiamo un embedding basato sul contesto dell'immagine
    # In una fase successiva potrai usare il modello 'models/multimodal-embedding-001'
    result = genai.embed_content(
        model="models/text-embedding-004",
        content="Caricamento immagine Pikrum Reference",
        task_type="retrieval_document"
    )
    return result['embedding']

def get_text_embedding(text_query, project_id, location):
    """Genera il vettore per le ricerche testuali"""
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text_query,
        task_type="retrieval_query"
    )
    return result['embedding']