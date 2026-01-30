from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Importa i settings
from django.conf.urls.static import static # Importa la funzione per i file statici

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)