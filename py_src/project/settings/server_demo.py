from project.settings.development import *
from ogv_documents.server.backends.default import DefaultServer
from ogv_documents.server.backends.nginx import NginxXAccelRedirectServer
from ogv_documents.storage import PrivateFileSystemStorage

DEBUG = False
TEMPLATE_DEBUG = False

EMAIL_BACKEND_LIST = ['django.core.mail.backends.smtp.EmailBackend',
                      'database_email_backend.backend.DatabaseEmailBackend']

INSTALLED_APPS += ['sentry.client', 'paging','indexer',
                   'nexus_memcache',
                   'gunicorn',]

PROJECT_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../') )
DATA_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../../../../') )
MEDIA_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'uploads'))


STATIC_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'static_collected'))
STATICFILES_DIRS = [
    ('', os.path.join(PROJECT_DIR, 'static')),
]

#MIDDLEWARE_CLASSES.insert(MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware'),)
#                          'project.middleware.limit_access.LimitedAccessMiddleware')
MIDDLEWARE_CLASSES.insert(0, 'project.middleware.remote_addr.SetRemoteAddrMiddleware')

SENTRY_SITE = 'onlinegv-demo'
SENTRY_REMOTE_URL = 'https://sentry.divio.ch/store/'
SENTRY_KEY = 'zEnR8meyespLeOIMHLbsOaWEoF5HlV6eQApdDzDMRnIhXNwGj6'

try:
    from django_secrets import *
except ImportError, e:
    print 'ImportError: ', e

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(DATA_DIR,'onlinegv.sqlite3'),
    },
}


OGV_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
            location=os.path.join(DATA_DIR, 'private_uploads/documents/'),
            base_url='/documents/general/')
OGV_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()

OGV_AUTH_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
            location=os.path.join(DATA_DIR, 'private_uploads/legal_documents/'),
            base_url='/documents/legal/')
OGV_AUTH_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()
