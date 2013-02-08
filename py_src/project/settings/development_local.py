from ogv_documents.server.backends.default import DefaultServer
from ogv_documents.storage import PrivateFileSystemStorage
from project.settings.development import *

CACHE_BACKEND = 'db://dbcache'

PROJECT_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../') )
DATA_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../../../tmp/') )
MEDIA_ROOT = os.path.abspath(os.path.join(PROJECT_DIR, '../../tmp/uploads'))

SQL_LOG_FILE = os.path.abspath( os.path.join(os.path.dirname(__file__),'../../../tmp/sql.log') )
SQL_LOG_ENABLE = False

WEBSERVICE_RAW_LOG_FILE = os.path.abspath( os.path.join(os.path.dirname(__file__),'../../../tmp/webservice.log') )
WEBSERVICE_RAW_LOG_ENABLE = False

STATIC_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'static_collected'))
STATICFILES_DIRS = [
    ('', os.path.join(PROJECT_DIR, 'static')),
]


OGV_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
            location=os.path.join(DATA_DIR, 'private_uploads/documents/'),
            base_url='/documents/general/')
OGV_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()

OGV_AUTH_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
            location=os.path.join(DATA_DIR, 'private_uploads/legal_documents/'),
            base_url='/documents/legal/')
OGV_AUTH_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()

CELERY_ALWAYS_EAGER = True
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True

OGV_USE_MTAN_LOGIN_FOR_ADMIN = False
OGV_USE_MTAN_LOGIN = True

# Uncomment the following lines to use a local nginx server to serve static
# files
#OGV_DOCUMENTS_PRIVATE_FILE_SERVER = NginxXAccelRedirectServer(
#                               location=OGV_DOCUMENTS_PRIVATE_FILE_STORAGE.location,
#                               nginx_location='/nginx_ogv_documents')

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
        'console': {
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'console_debug': {
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
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
            'filename': WEBSERVICE_RAW_LOG_FILE,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry.client.handlers.SentryHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'ogv_documents': {
            'handlers': ['console_debug'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'ogv_notification': {
            'handlers':['console'],
            'propagate': True,
            'level':'INFO',
        },
        'ogv_mailing': {
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
            'handlers': [], #['console','sql_logfile'],
            'level': 'INFO',
        },
        'ogv_webservice': {
            'handlers': [], #['console','webservice_logfile'],
            'level': 'INFO',
        },
        'root': {
            'handler': ['console',],
            'level': 'INFO',
        },
        'django.db.backends': {
            'handlers': ['console',],
            'level': 'INFO',
        }
    }
}

#INSTALLED_APPS += (
#    'debug_toolbar',
#)
#
#DEBUG_TOOLBAR_PANELS = (
#    'debug_toolbar.panels.version.VersionDebugPanel',
#    'debug_toolbar.panels.timer.TimerDebugPanel',
#    'debug_toolbar.panels.settings_vars.SettingsVarsDebugPanel',
#    'debug_toolbar.panels.headers.HeaderDebugPanel',
#    'debug_toolbar.panels.request_vars.RequestVarsDebugPanel',
#    'debug_toolbar.panels.template.TemplateDebugPanel',
#    'debug_toolbar.panels.sql.SQLDebugPanel',
#    'debug_toolbar.panels.signals.SignalDebugPanel',
#    'debug_toolbar.panels.logger.LoggingPanel',
#)
#
#DEBUG_TOOLBAR_CONFIG = {
#    'INTERCEPT_REDIRECTS': False
#}
#
#MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
