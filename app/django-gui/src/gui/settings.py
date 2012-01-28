DATABASE_ENGINE = 'django.db.backends.postgresql_psycopg2'
DATABASE_NAME = 'ifam'
INSTALLED_APPS = ['django.contrib.admin', 'registration_defaults', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.sites', 'django.contrib.messages', 'django.contrib.staticfiles', 'registration','gui']
ROOT_URLCONF = 'gui.urls'
SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = True
STATIC_URL = './media/'
