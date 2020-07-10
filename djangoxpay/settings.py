"""
Django settings for djangoxpay project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'yjce%7=z^lk^eix^b7r&9b94vhda))3ue=$%e^5fw)^dot&%kz')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = list(filter(lambda x: len(x) > 0, os.environ.get('ALLOWED_HOSTS', '').split(',')))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user.apps.UserConfig',
    'xstripe.apps.XstripeConfig',
    'xsquare.apps.XsquareConfig',
    'xbraintree.apps.XbraintreeConfig',
    'xmpesa.apps.XmpesaConfig',
    'xauth',
    'rest_framework',
    'django_extensions',
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

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',  # For faster test execution
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

ROOT_URLCONF = 'djangoxpay.urls'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'xauth.authentication.BasicTokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'EXCEPTION_HANDLER': 'xauth.utils.exceptions.exception_handler',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

XAUTH = {
    'APP_NAME': 'Xently Pay',
    'USER_LOOKUP_FIELD': 'username',
    'PROFILE_ENDPOINT': r'profile/(?P<username>\w+)/',
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
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

WSGI_APPLICATION = 'djangoxpay.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators
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

AUTH_USER_MODEL = 'user.User'

EMAIL_HOST = os.environ.get('EMAIL_HOST', settings.EMAIL_HOST)

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', settings.EMAIL_HOST_USER)

EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', settings.EMAIL_HOST_PASSWORD)

EMAIL_USE_TLS = True

EMAIL_PORT = 587

# EMAIL_PORT = 1025

EMAIL_TIMEOUT = 20  # seconds

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

PAYMENT = {
    'MPESA': {
        'CONSUMER_KEY': os.environ.get('MPESA_CONSUMER_KEY', ),
        'CONSUMER_SECRET': os.environ.get('MPESA_CONSUMER_SECRET', ),
        'LNM': {
            'SHORTCODE': os.environ.get('MPESA_LNM_SHORTCODE', ),
            'PASSKEY': os.environ.get('MPESA_LNM_PASSKEY', ),
        },
        'SECURITY_CREDENTIALS': os.environ.get('MPESA_SECURITY_CREDENTIALS', ),
    },
    'BRAINTREE': {
        'MERCHANT_ID': os.environ.get('BRAINTREE_MERCHANT_ID', ),
        'PUBLIC_KEY': os.environ.get('BRAINTREE_PUBLIC_KEY', ),
        'PRIVATE_KEY': os.environ.get('BRAINTREE_PRIVATE_KEY', ),
    },
    'STRIPE': {
        'API_KEY': os.environ.get('STRIPE_API_KEY', ),
    },
    'SQUARE': {
        'ACCESS_TOKEN': os.environ.get('SQUARE_ACCESS_TOKEN', ),
    },
}
