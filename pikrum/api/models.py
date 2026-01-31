import uuid
from django.db import models


# --- TABELLE IMMAGINI ---

class CatalogedImage(models.Model):
    """Rappresenta il file fisico originale caricato (es. pagina di catalogo)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200, blank=True, null=True) 
    image_file = models.ImageField(upload_to='catalog/')
    original_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cataloged_images'
        verbose_name_plural = "Cataloged Images"

    def __str__(self):
        return self.title or self.original_name


class ImageDetection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parent_image = models.ForeignKey(
        CatalogedImage, 
        related_name='detections', 
        on_delete=models.CASCADE
    )
    
    label = models.CharField(max_length=100, blank=True)
    ai_description = models.TextField(blank=True)
    generated_tags = models.JSONField(default=list, blank=True)
    
    # Indica se questo oggetto è una Reference (campione di riferimento)
    is_reference = models.BooleanField(default=True)
    
    # Indica se l'utente ha confermato l'identificazione (utile per il flusso "al volo")
    is_verified = models.BooleanField(default=True)
    
    bounding_box = models.JSONField(help_text="Formato: [ymin, xmin, ymax, xmax]")
    embedding_vector = models.JSONField(blank=True, null=True)    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'image_detections'
        verbose_name_plural = "Image Detections"


# --- TABELLE TASSONOMIA (GUIDANCE) ---

class Feature(models.Model):
    """Esempio: Forma, Colore, Materiale"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Features"

    def __str__(self):
        return self.name

class FeatureValue(models.Model):
    """Esempio: Tondo, Quadrato (collegati a Forma)"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    feature = models.ForeignKey(Feature, related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=100)

    class Meta:
        unique_together = ('feature', 'value')
        verbose_name_plural = "Feature Values"

    def __str__(self):
        return f"{self.feature.name}: {self.value}"