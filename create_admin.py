import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pikrum.backend.settings')
django.setup()

from django.contrib.auth.models import User

username = "admin"  # Puoi cambiarlo
password = "KRK_rokit_5" # Cambiala assolutamente!
email = "admin@example.com"

if not User.objects.filter(username=username).exists():
    print(f"Creazione utente {username}...")
    User.objects.create_superuser(username, email, password)
    print("Utente creato con successo!")
else:
    print(f"L'utente {username} esiste già.")