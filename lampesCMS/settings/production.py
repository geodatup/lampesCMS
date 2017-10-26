from lampesCMS.settings.base import *

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 't21etvwc@m3165@n$e*+@mr&4fd+y7=^j&kzgemjzhfd=8-0qf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
    'gunicorn', # other apps for production site
)

DATABASES = {
    'default': {
        'CONN_MAX_AGE': 0,
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'HOST': '192.168.1.99',
        'NAME': 'postgres',
        'PASSWORD': 'mcot9a9.u',
        'PORT': '5432',
        'USER': 'postgres'
    }
}
