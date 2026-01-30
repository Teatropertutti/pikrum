import vertexai
from vertexai.generative_models import GenerativeModel
import os

PROJECT_ID = "project-62082eb5-3b25-4adb-bd0"
LOCATION = "us-central1"

print(f"--- 🕵️ CERCO IL NOME ESATTO DEL MODELLO ---")
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Le varianti da provare (in ordine di probabilità)
candidates = [
    "gemini-1.5-flash-001",  # Versione stabile
    "gemini-1.5-flash-002",  # Versione nuova
    "gemini-1.5-pro-001",    # Versione Pro
    "gemini-1.0-pro"         # Vecchia generazione (fallback)
]

found = False
for name in candidates:
    print(f"\n👉 Testo: '{name}'...")
    try:
        model = GenerativeModel(name)
        response = model.generate_content("Scrivi: OK")
        print(f"✅ TROVATO! Il modello attivo è: {name}")
        found = name
        break
    except Exception as e:
        if "404" in str(e):
            print("❌ 404: Non trovato.")
        else:
            print(f"⚠️ Errore diverso: {str(e)[:50]}...")

print("\n" + "="*40)
if found:
    print(f"🏆 COPIA QUESTO IN SETTINGS.PY:  '{found}'")
else:
    print("😭 Nessun modello trovato. Verifica se l'API Vertex AI è abilitata.")
print("="*40)