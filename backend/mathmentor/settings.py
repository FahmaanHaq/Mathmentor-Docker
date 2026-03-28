import os
from pathlib import Path
from decouple import config
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- SECURITY ---
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)

# Allow Railway and Localhost
ALLOWED_HOSTS = [
    'localhost', 
    '127.0.0.1', 
    '.localhost', 
    '.up.railway.app', 
    '*' 
]

# --- APPLICATION DEFINITION ---
INSTALLED_APPS = [
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'channels',
    'anymail',
    'accounts',
    'tutoring',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # Priority 1
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # For production static files
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mathmentor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mathmentor.wsgi.application'
ASGI_APPLICATION = 'mathmentor.asgi.application'

# --- DATABASE CONFIGURATION ---
# Uses DATABASE_URL on Railway, falls back to SQLite locally
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- CHANNELS / REDIS ---
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [config('REDIS_URL', default='redis://localhost:6379')],
        },
    },
}

# --- AUTHENTICATION ---
AUTH_USER_MODEL = 'accounts.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- INTERNATIONALIZATION ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- STATIC & MEDIA FILES ---
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- REST FRAMEWORK ---
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.authentication.CsrfExemptSessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
}

# --- CORS & CSRF ---
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = False # False for production security

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://mathmentor-main.vercel.app",
    "https://mathmentor-main-fakv3m92s-fahmaanhaqs-projects.vercel.app",
]

CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://mathmentor-main-.*\.vercel\.app$",
]

# Crucial for Railway/Vercel communication
CSRF_TRUSTED_ORIGINS = [
    "https://mathmentor-main.vercel.app",
    "https://*.up.railway.app",
    "https://mathmentor-main-fakv3m92s-fahmaanhaqs-projects.vercel.app",
]

# --- SESSION & COOKIES ---
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_NAME = 'csrftoken'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_NAME = config('SESSION_COOKIE_NAME', default='mathmentor_sessionid')

if DEBUG:
    # Local development: Lax is fine for same-site requests
    CSRF_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=False, cast=bool)
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=False, cast=bool)
else:
    # Production: cross-site (Vercel frontend → Railway backend) requires SameSite=None + Secure
    CSRF_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
    SESSION_COOKIE_SAMESITE = 'None'
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)

# --- EXTERNAL SERVICES ---

# Email
# SendGrid (preferred on Railway where outbound SMTP is blocked)
SENDGRID_API_KEY = config('SENDGRID_API_KEY', default='')
EMAIL_TIMEOUT = config('EMAIL_TIMEOUT', default=10, cast=int)
DEFAULT_FROM_EMAIL = config('EMAIL_FROM_ADDRESS', default='noreply@mathmentor.com')

if SENDGRID_API_KEY:
    EMAIL_BACKEND = 'anymail.backends.sendgrid.EmailBackend'
    ANYMAIL = {'SENDGRID_API_KEY': SENDGRID_API_KEY}
else:
    EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
    EMAIL_HOST = config('EMAIL_HOST', default='smtp.gmail.com')
    EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
    EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
    EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
    EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')

# Stripe
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')

# Frontend URL
FRONTEND_URL = config('FRONTEND_URL', default='http://localhost:3000')

# Jitsi / JaaS
JAAS_APP_ID = config('JAAS_APP_ID', default='vpaas-magic-cookie-7b66c51250a5450c8228c052d21ee9a8')
JAAS_API_KEY_ID = config('JAAS_API_KEY_ID', default='vpaas-magic-cookie-7b66c51250a5450c8228c052d21ee9a8/c85043')
JAAS_PRIVATE_KEY_PATH = config('JAAS_PRIVATE_KEY_PATH', default=str(BASE_DIR / 'jitsi-keys' / 'private_key.pem'))
