import os
from pathlib import Path
import dj_database_url  # Fondamentale per Railway

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
# Su Railway usiamo la variabile d'ambiente, se manca usiamo quella di default
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-(y$2o)yq987f*v-!t6q=@))@#vb&i3ixhig++kcdz1csq7&mca')

# In produzione su Railway DEBUG dovrebbe essere False
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Permettiamo a Railway di gestire il dominio
ALLOWED_HOSTS = ['*']

# --- Application definition ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_spectacular',
    'api', # La tua app
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Per i file statici su Railway
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pikrum_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pikrum_backend.wsgi.application'

# --- DATABASE (Configurazione Railway) ---
# Legge automaticamente la variabile DATABASE_URL di Railway
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization ---
LANGUAGE_CODE = 'it-it'
TIME_ZONE = 'Europe/Rome'
USE_I18N = True
USE_TZ = True

# --- Static & Media Files ---
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# --- Default primary key ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CORS & REST Framework ---
CORS_ALLOW_ALL_ORIGINS = True 
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# --- Vertex AI / Gemini Configuration ---
# Ora usiamo la API KEY invece del file JSON
VERTEX_AI_CONFIG = {
    'API_KEY': os.environ.get('GOOGLE_API_KEY'),
    'PROJECT_ID': os.environ.get('PROJECT_ID', 'project-62082eb5-3b25-4adb-bd0'),
    'LOCATION': 'us-central1',  
    'MODELS': {
        'VISION': 'gemini-1.5-flash', # Versione stabile per API Key
        'EMBEDDING': 'multimodalembedding',
    }
}