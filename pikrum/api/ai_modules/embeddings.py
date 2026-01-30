import vertexai
from vertexai.vision_models import MultiModalEmbeddingModel, MultiModalEmbeddingResponse
from vertexai.generative_models import Part

def get_image_embedding(image_bytes, project_id, location):
    """Genera il vettore (embedding) partendo dai pixel di un'immagine"""
    vertexai.init(project=project_id, location=location)
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    
    embeddings = model.get_embeddings(
        image=Part.from_data(data=image_bytes, mime_type="image/jpeg")
    )
    return embeddings.image_embedding

def get_text_embedding(text_query, project_id, location):
    """Genera il vettore (embedding) partendo da una stringa di testo"""
    vertexai.init(project=project_id, location=location)
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    
    embeddings = model.get_embeddings(
        contextual_text=text_query
    )
    return embeddings.text_embedding