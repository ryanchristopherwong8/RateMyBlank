"""
Django settings for RateMyBlank project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p@)=3m0x4tr)lmdv40k@6qi(d$620i4(6b0@k=u%p28ysa_-(j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ["https://rate-my-blank.herokuapp.com/"]


# Application definition

INSTALLED_APPS = (
    'src',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'RateMyBlank.urls'

WSGI_APPLICATION = 'RateMyBlank.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

import dj_database_url
DATABASES = {'default' : dj_database_url.config() }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static asset configuration
# import os
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

#STATICFILES_DIRS = (
 #   os.path.join(BASE_DIR, 'static'),
#)
#STATIC_ROOT = '../RateMyBlank/src/static'

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

try:
    from RateMyBlank.local_settings import *
except ImportError:
    pass