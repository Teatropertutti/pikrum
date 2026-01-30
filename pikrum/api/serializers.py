from rest_framework import serializers
from .models import CatalogedImage

class CatalogedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CatalogedImage
        fields = ['id', 'image_file', 'original_name', 'ai_description', 'generated_tags', 'created_at']
        read_only_fields = ['id', 'ai_description', 'generated_tags', 'created_at']


def get_text_embedding(text, project_id, location):
    """Trasforma una stringa di ricerca in un vettore numerico"""
    vertexai.init(project=project_id, location=location)
    model = MultiModalEmbeddingModel.from_pretrained("multimodalembedding")
    
    embeddings = model.get_embeddings(contextual_text=text)
    return embeddings.text_embedding