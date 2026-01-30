from django.urls import path
from .views import CatalogUploadView, ReferenceUploadView, SemanticSearchView

urlpatterns = [
    # Caricamento foto di catalogo (scomposizione AI in oggetti)
    path('v1/upload/catalog/', CatalogUploadView.as_view(), name='catalog-upload'),
    
    # Caricamento Reference (prodotto singolo di riferimento)
    path('v1/upload/reference/', ReferenceUploadView.as_view(), name='reference-upload'),
    
    # Ricerca semantica (testo o immagine)
    path('v1/search/', SemanticSearchView.as_view(), name='semantic-search'),
]