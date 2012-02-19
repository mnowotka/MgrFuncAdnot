import os, sys

PROJECT_ROOT = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')
MEDIA_URL = 'http://127.0.0.1:8000/static/'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
DATABASE_NAME = 'ifam'
DAJAXICE_MEDIA_PREFIX = "dajaxice"

INSTALLED_APPS = (
    'django.contrib.admin', 
    'registration_defaults', 
    'django.contrib.auth', 
    'django.contrib.contenttypes', 
    'django.contrib.sessions', 
    'django.contrib.sites', 
    'django.contrib.messages', 
    'django.contrib.staticfiles', 
    'django_jquery_ui',
    'registration',
    'dajaxice',
    'dajax',
    'gui',
)

ROOT_URLCONF = 'gui.urls'
SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = True
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = os.path.join(os.path.abspath(os.path.join(PROJECT_ROOT, '..', MEDIA_ROOT, 'static')), '')
STATIC_URL = '/static/'

TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.request",
                               "django.contrib.messages.context_processors.messages")

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

