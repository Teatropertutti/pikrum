from django.contrib import admin
from .models import CatalogedImage, ImageDetection, Feature, FeatureValue

# --- TASSONOMIA (Features e Valori) ---

class FeatureValueInline(admin.TabularInline):
    model = FeatureValue
    extra = 3

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')
    inlines = [FeatureValueInline]

# --- IMMAGINI E DETECTIONS ---

class ImageDetectionInline(admin.TabularInline):
    """Permette di vedere i ritagli/oggetti dentro la CatalogedImage"""
    model = ImageDetection
    extra = 0
    fields = ('label', 'is_reference', 'is_verified', 'bounding_box', 'ai_description')
    readonly_fields = ('embedding_vector', 'generated_tags')
    can_delete = True

@admin.register(CatalogedImage)
class CatalogedImageAdmin(admin.ModelAdmin):
    list_display = ('original_name', 'title', 'created_at')
    search_fields = ('original_name', 'title')
    inlines = [ImageDetectionInline]

@admin.register(ImageDetection)
class ImageDetectionAdmin(admin.ModelAdmin):
    list_display = ('label', 'parent_image', 'created_at')
    list_filter = ('parent_image', 'label')
    readonly_fields = ('embedding_vector',)