import os, sys

PROJECT_ROOT = os.path.dirname(__file__)

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')
TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
)

DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
DATABASE_NAME = 'ifam'
INSTALLED_APPS = ['django.contrib.admin', 'registration_defaults', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles', 'registration','gui']
ROOT_URLCONF = 'gui.urls'
SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = True
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATIC_ROOT = os.path.join(os.path.abspath(os.path.join(PROJECT_ROOT, '..', MEDIA_ROOT, 'static')), '')
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
'django.contrib.staticfiles.finders.FileSystemFinder',
'django.contrib.staticfiles.finders.AppDirectoriesFinder',
'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

