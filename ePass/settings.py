"""
Django settings for ePass project.

Generated by 'django-admin startproject' using Django 4.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

import environ
from dotenv import load_dotenv

load_dotenv()

env = environ.Env(
    DEBUG=bool,
    SECRET_KEY=str,

    # Token
    ACCESS_TOKEN_LIFE_TIME=int,

    # SMS
    SMSRU_API_TOKEN=str,
    CONFIRMATION_CODE_EXPIRATION=int,

    # Redis
    REDIS_HOST=str,
    REDIS_PORT=int,

    # Postgres
    POSTGRES_DB=str,
    POSTGRES_USER=str,
    POSTGRES_PASSWORD=str,
    POSTGRES_DB_HOST=str,
    POSTGRES_DB_PORT=int,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3-rd party app
    'phonenumber_field',
    'rest_framework_swagger',
    'rest_framework_simplejwt',
    'rest_framework',
    'drf_yasg',
    'drf_standardized_errors',
    'django_celery_results',

    # Local apps
    'users',
    'sections',
    'user_verification'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'ePass.core.CustomPagination.CustomPagination',
    'PAGE_SIZE': 15,
}

DRF_STANDARDIZED_ERRORS = {
    'ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS': True,
}

ROOT_URLCONF = 'ePass.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'ePass.wsgi.application'

APPEND_SLASH = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Postgres
DB_NAME = env('POSTGRES_DB')
DB_USER = env('POSTGRES_USER')
DB_PASSWORD = env('POSTGRES_PASSWORD')
DB_HOST = env('POSTGRES_DB_HOST')
DB_PORT = env('POSTGRES_DB_PORT')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Users
AUTH_USER_MODEL = 'users.UserModel'

PHONE_NUMBER_REGION = 'RU'

CONFIRMATION_CODE_EXPIRATION = env('CONFIRMATION_CODE_EXPIRATION')  # Seconds

# JWT Token Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=env('ACCESS_TOKEN_LIFE_TIME')),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=env('ACCESS_TOKEN_LIFE_TIME')),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': '',
    'AUDIENCE': None,
    'ISSUER': None,
    'JSON_ENCODER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.user_verification.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    'TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
}

# SMS service
SMSRU_API_TOKEN = env('SMSRU_API_TOKEN')

# Redis
REDIS_HOST = env('REDIS_HOST')
REDIS_PORT = env('REDIS_PORT')

# Celery
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
CELERY_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}'

# settings.py

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(levelname)s - %(asctime)s] %(name)s.%(funcName)s:%(lineno)s- %(message)s',
        },
    },
    'handlers': {
        'django_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'django.log'),
            'maxBytes': 1024 * 1024 * 3,  # 3 MB
            'backupCount': 1,
            'formatter': 'simple',
        },
        'requests_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'request.log'),
            'maxBytes': 1024 * 1024 * 3,  # 3 MB
            'backupCount': 3,
            'formatter': 'simple',
        },
        'database_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'db.log'),
            'maxBytes': 1024 * 1024 * 3,  # 3 MB
            'backupCount': 3,
            'formatter': 'simple',
        },
        'celery_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'celery.log'),
            'maxBytes': 1024 * 1024 * 3,  # 3 MB
            'backupCount': 3,
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['django_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['requests_file'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['database_file'],
            'level': 'INFO',
        },
        'celery': {
            'handlers': ['celery_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
