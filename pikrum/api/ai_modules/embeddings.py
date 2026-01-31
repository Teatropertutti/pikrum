import google.generativeai as genai
from django.conf import settings

def get_image_embedding(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    genai.configure(api_key=api_key)
    
    # Modello di embedding standard per API Key
    result = genai.embed_content(
        model="models/text-embedding-004",
        content="Pikrum Image Analysis",
        task_type="retrieval_document"
    )
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