from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.admin.site.urls),
    # Questo collega il file urls.py della tua app
    path('api/', include('pikrum.api.urls')), 
]