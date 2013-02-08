from project.settings.development import *
from ogv_documents.server.backends.default import DefaultServer
from ogv_documents.server.backends.nginx import NginxXAccelRedirectServer
from ogv_documents.storage import PrivateFileSystemStorage

DEBUG = True
TEMPLATE_DEBUG = False

HTTPS_URLS_BY_DEFAULT = True


EMAIL_BACKEND_LIST = ['django.core.mail.backends.smtp.EmailBackend',
                      'database_email_backend.backend.DatabaseEmailBackend']
EMAIL_HOST = 'mailtrap.io'
EMAIL_HOST_USER = 'onlinegv-dev-divio-ch'
EMAIL_HOST_PASSWORD = '265f8a184e5af8c6'
EMAIL_PORT = 2525
EMAIL_USE_TLS = False

SENDSMS_BACKEND = 'sendsms_admin.backend.DatabaseSmsBackend'


INSTALLED_APPS += ['sentry.client', 
                   'paging',
                   'indexer',
                   'nexus_memcache',
                   'gunicorn',]

PROJECT_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../') )
DATA_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../../../../') )
MEDIA_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'upload'))

SQL_LOG_FILE = os.path.abspath( os.path.join(DATA_DIR,'sql.log') )
SQL_LOG_ENABLE = False

WEBSERVICE_LOG_FILE = os.path.abspath( os.path.join(DATA_DIR,'webservice.log') )
WEBSERVICE_LOG_ENABLE = True


STATIC_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'static'))
STATICFILES_DIRS = [
    ('', os.path.join(PROJECT_DIR, 'static')),
]

#MIDDLEWARE_CLASSES.insert(MIDDLEWARE_CLASSES.index('django.middleware.common.CommonMiddleware'),)
#                          'project.middleware.limit_access.LimitedAccessMiddleware')
MIDDLEWARE_CLASSES.insert(0, 'project.middleware.remote_addr.SetRemoteAddrMiddleware')

#BROKER_USER = 'onlinegv'
#BROKER_PASSWORD = 'kPFwm?>Scs0lq9PeY'
#BROKER_VHOST = '/onlinegv/dev'

SENTRY_TESTING=True
SENTRY_SITE = 'onlinegv-dev'
SENTRY_REMOTE_URL = 'https://ogv-sentry.divio.ch/store/'
SENTRY_KEY = 'zEnR8meyespLeOIMHLbsOaWEoF5HlV6eQApdDzDMRnIhXNwGj6'

# Secure cookies by default (HTTPS)
SESSION_COOKIE_SECURE=True

try:
    from django_secrets import *
except ImportError, e:
    print 'ImportError: ', e

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "onlinegv-dev",
        'USER': "onlinegv-dev",
    }
}


OGV_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
            location=os.path.join(DATA_DIR, 'private_uploads/documents/'),
            base_url='/documents/general/')
OGV_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()

OGV_AUTH_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
            location=os.path.join(DATA_DIR, 'private_uploads/legal_documents/'),
            base_url='/documents/legal/')
OGV_AUTH_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()


SESSION_COOKIE_AGE = 1800
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 500
SECURE_FRAME_DENY = True
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True

OGV_USE_MTAN_LOGIN_FOR_ADMIN = False
OGV_USE_MTAN_LOGIN = False

CELERY_ALWAYS_EAGER = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(name)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        },
    'handlers': {
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'sql_logfile':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': SQL_LOG_FILE,
            },
        'webservice_logfile':{
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': WEBSERVICE_LOG_FILE,
            },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry.client.handlers.SentryHandler'
        },
        },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
            },
        'django.request': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': False,
            },
        'sql_logger': {
            'handlers': ['sql_logfile'],
            'level': 'INFO',
            },
        'ogv_webservice': {
            'handlers': ['webservice_logfile'],
            'level': 'INFO',
            },
        'root': {
            'handler': ['console',],
            'level': 'INFO',
            },
        'django.db.backends': {
            'handlers': ['console',],
            'level': 'INFO',
            },
        }
}