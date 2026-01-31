from genai import Client
from django.conf import settings

def get_image_embedding(image_bytes, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    client = Client(api_key=api_key)
    
    # Nuovo metodo per gli embeddings
    result = client.models.embed_content(
        model="text-embedding-004",
        contents="Analisi visuale Pikrum"
    )
    return result.embeddings[0].values

def get_text_embedding(text_query, project_id, location):
    api_key = settings.VERTEX_AI_CONFIG.get("API_KEY")
    client = Client(api_key=api_key)
    
    result = client.models.embed_content(
        model="text-embedding-004",
        contents=text_query
    )
    return result.embeddings[0].values