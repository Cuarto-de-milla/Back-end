""" Django settings for oilApp project. """

# Utilities
from pathlib import Path
import os

# Envron 
import environ

# Deploy 
import django_heroku

# Path of the base Dir
BASE_DIR = Path(__file__).resolve().parent.parent

# environ config
env = environ.Env()
env_file = os.path.join(BASE_DIR,'.env')
environ.Env.read_env(env_file)

# Secret Key
SECRET_KEY = env.str('SECRET_KEY')

# Debug  variable
DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = [ '*']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
]
THIRD_PARTY_APPS = [
    'graphene_django',
    'django_filters',
    'corsheaders',
]
LOCAL_APPS = [
    'gasoline',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',

]
CORS_ORIGIN_ALLOW_ALL = True 
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'oilApp.urls'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (
    os.path.join('static'),
    )
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

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

WSGI_APPLICATION = 'oilApp.wsgi.application'

# Graphene
GRAPHENE = {
    "SCHEMA": "gasoline.schema.schema"
}

# DATABASES
DATABASES = {
    'default': env.db('DATABASE_URL'),
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL= '/media/'

# Heroku
django_heroku.settings(locals())