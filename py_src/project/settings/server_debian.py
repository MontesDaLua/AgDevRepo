from project.settings.base import *
import ConfigParser
import sys, os
from ogv_documents.server.backends.default import DefaultServer

EMAIL_DEFAULT_RECEIVER = ["operator@sherpany.com"]

SESSION_COOKIE_AGE = 60 * 30
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_SECURE = True
SECURE_FRAME_DENY = False  # We can't activate this, because the cms uses iframes for plugin editing
#SECURE_SSL_REDIRECT = True  # We can't use this, because SSL termination happens on the WAF. Redirect already happens there
SECURE_HSTS_SECONDS = 500

HTTPS_URLS_BY_DEFAULT = True

USE_X_FORWARDED_HOST = False  # X-Forwarded-Host from the WAF contains the IP instead of the Hostname
ADMINS = []  # Don't send Exception Emails (we have Sentry instead)

# A helper to workaround the fact that the configparser allow_no_value option is Python 2.7 only.
def get_config_or_none(config, section_name, option_name, default=None):
    try:
        return config.get(section_name, option_name)
    except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
        return default

# Actual config parsing starts here.
config = ConfigParser.RawConfigParser()
file_lines = []
if os.path.exists('/etc/onlinegv/config.cfg'):
    # the file may not exist, but the import should still work.
    # This is needed to collectstatic while building the package on the package building server that does not have
    # config.cfg
    with open('/etc/onlinegv/config.cfg', 'r') as myfile:
        file_lines = myfile.readlines()
        myfile.seek(0)
        config.readfp(myfile)

DEBUG = str(get_config_or_none(config, 'Django', 'debug', 'no')).lower() in ('true', 'yes')

########################
# EXTRA INSTALLED APPS #
########################

INSTALLED_APPS += ['sentry.client',
                   'gunicorn',] # We need gunicorn in there too.

#MIDDLEWARE_CLASSES = ['project.middleware.debug_headers.DebugHeadersMiddleware'] + MIDDLEWARE_CLASSES


############
# DATABASE #
############

db_name = get_config_or_none(config,'Database', 'name')
db_engine = get_config_or_none(config,'Database', 'engine') or ''
db_user = get_config_or_none(config,'Database', 'user')
db_password = get_config_or_none(config,'Database', 'password')
db_host = get_config_or_none(config,'Database', 'host')
db_port = get_config_or_none(config,'Database', 'port')
if db_name and db_engine:  # only set db config from config file if it exists
    DATABASES = {
        'default': {
            'ENGINE': db_engine,
            'NAME': db_name,
            'PASSWORD': db_password,
            'USER': db_user,
            'HOST': db_host,
            'PORT': db_port,
        }
    }


#########
# CACHE #
#########

if get_config_or_none(config,'Memcached', 'enable') == 'yes':
    cache_locations = [s.strip() for s in get_config_or_none(config,'Memcached', 'ips', '').split(',')]
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': cache_locations
        }
    }


################
# CELERY QUEUE #
################

import djcelery
djcelery.setup_loader()

BROKER_HOST = get_config_or_none(config,'QueueBroker', 'host')
BROKER_PORT = get_config_or_none(config,'QueueBroker', 'port')
BROKER_USER = get_config_or_none(config,'QueueBroker', 'user')
BROKER_PASSWORD = get_config_or_none(config,'QueueBroker', 'password')
BROKER_VHOST = get_config_or_none(config,'QueueBroker', 'vhost')
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'


#########
# EMAIL #
#########

SERVER_EMAIL = get_config_or_none(config,'Email', 'default_from_email', 'noreply@sherpany.com')
DEFAULT_FROM_EMAIL = get_config_or_none(config,'Email', 'default_from_email', 'noreply@sherpany.com')
EMAIL_SUBJECT_PREFIX = '[%s] ' % get_config_or_none(config,'Logging', 'name', 'onlinegv')

EMAIL_BACKEND_LIST = ['database_email_backend.backend.DatabaseEmailBackend']

if get_config_or_none(config,'Email', 'enable') == 'yes':
    EMAIL_BACKEND_LIST.append('django.core.mail.backends.smtp.EmailBackend')
    EMAIL_HOST = get_config_or_none(config,'Email', 'host') or 'localhost'
    EMAIL_PORT = get_config_or_none(config,'Email', 'port') or 25
    EMAIL_HOST_USER = get_config_or_none(config,'Email', 'user') or ''
    EMAIL_HOST_PASSWORD = get_config_or_none(config,'Email', 'password') or ''
    EMAIL_USE_TLS = get_config_or_none(config,'Email', 'password')=='yes'



#######
# SMS #
#######

if get_config_or_none(config,'Sms', 'enable') == 'yes':
    SENDSMS_BACKEND = 'onlinegv.backends.sms_backends.atrila.SmsBackend'
    SENDSMS_ATRILA_SERVICE_URL = get_config_or_none(config,'Sms', 'url')
    SENDSMS_ATRILA_USERNAME = get_config_or_none(config,'Sms', 'user')
    SENDSMS_ATRILA_PASSWORD = get_config_or_none(config,'Sms', 'password')
else:
    SENDSMS_BACKEND = 'sendsms_admin.backend.DatabaseSmsBackend'


##################
# SENTRY LOGGING #
##################

if get_config_or_none(config,'Logging', 'enable') == 'yes':
    SENTRY_TESTING = get_config_or_none(config,'Logging', 'debug') == 'yes'
    SENTRY_SITE = get_config_or_none(config,'Logging', 'name')
    SENTRY_REMOTE_URL = get_config_or_none(config,'Logging', 'url')
    SENTRY_KEY = get_config_or_none(config,'Logging', 'key')


##################
# SECURITY STUFF #
##################

SESSION_COOKIE_AGE = 1800
# Settings deactivated because the firewall/WAF already does this stuff
# and it only results in problems if we check again and make redirects.
#SECURE_SSL_REDIRECT = True
#SECURE_HSTS_SECONDS = 500
#SECURE_FRAME_DENY = True
#SESSION_COOKIE_SECURE = True
#SESSION_COOKIE_HTTPONLY = True

OGV_USE_MTAN_LOGIN_FOR_ADMIN = get_config_or_none(config,'Security', 'admin_mtan_login', 'yes') == 'yes'
OGV_USE_MTAN_LOGIN = get_config_or_none(config,'Security', 'mtan_login', 'yes') == 'yes'


########################
# FILESYSTEM LOCATIONS #
########################

PROJECT_DIR = os.path.abspath( os.path.join(os.path.dirname(__file__),'../') )
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__),'../../../') )

STATIC_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'static_collected'))
STATICFILES_DIRS = [
    ('', os.path.join(PROJECT_DIR, 'static')),
]

if get_config_or_none(config,'MogileFS', 'enable')=='yes':
    from ogv_documents.storage.mogilefs import MogilefsStorage
    from ogv_documents.server.backends.nginx_mogilefs import NginxMogilefsXAccelRedirectServer
    MOGILEFS_DOMAIN = get_config_or_none(config, 'MogileFS', 'public_domain')
    MOGILEFS_TRACKERS = [x.strip() for x in get_config_or_none(config, 'MogileFS', 'trackers', '').split(',')]
    DEFAULT_FILE_STORAGE = 'ogv_documents.storage.mogilefs.MogilefsStorage'
    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE
    OGV_DOCUMENTS_PRIVATE_FILE_STORAGE = MogilefsStorage(
                domain=get_config_or_none(config,'MogileFS', 'private_domain'),
                container='documents',
                base_url='/documents/general/',
                trackers=MOGILEFS_TRACKERS
    )
    OGV_DOCUMENTS_PRIVATE_FILE_SERVER = NginxMogilefsXAccelRedirectServer(
        nginx_location='/private/'
    )

    OGV_AUTH_DOCUMENTS_PRIVATE_FILE_STORAGE = MogilefsStorage(
                domain=get_config_or_none(config,'MogileFS', 'private_domain'),
                container='authorization_documents',
                base_url='/documents/legal/',
                trackers=MOGILEFS_TRACKERS
    )
    OGV_AUTH_DOCUMENTS_PRIVATE_FILE_SERVER = NginxMogilefsXAccelRedirectServer(
        nginx_location='/private/'
    )
else:
    # This is only to make the server function properly for the time being.
    # We need a switch to make it work with mogile FS in the future.
    from ogv_documents.storage import PrivateFileSystemStorage
    MEDIA_ROOT = os.path.join(DATA_DIR, 'public_media')

    OGV_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
                location=os.path.join(DATA_DIR, 'private_uploads/documents/'),
                base_url='/documents/general/')
    OGV_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()

    OGV_AUTH_DOCUMENTS_PRIVATE_FILE_STORAGE = PrivateFileSystemStorage(
                location=os.path.join(DATA_DIR, 'private_uploads/legal_documents/'),
                base_url='/documents/legal/')
    OGV_AUTH_DOCUMENTS_PRIVATE_FILE_SERVER = DefaultServer()


#####################
# LOGFILE LOCATIONS #
#####################

SQL_LOG_ENABLE = get_config_or_none(config, 'SqlLogging', 'enable', default=False) == 'yes'
#SQL_LOG_FILE = get_config_or_none(config, 'SqlLogging', 'file', default='')

WEBSERVICE_LOG_ENABLE = get_config_or_none(config, 'WebserviceLogging', 'enable', default=False) == 'yes'
WEBSERVICE_LOG_FILE = get_config_or_none(config, 'WebserviceLogging', 'file', default='')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
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
            'handlers':[],
            'propagate': True,
            'level':'INFO',
        },
        'django.request': {
            'handlers': ['console',],
            'level': 'ERROR',
            'propagate': False,
        },
#        'sql_logger': {
#            'handlers': [], #['console','sql_logfile'],
#            'level': 'INFO',
#        },
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
        },
    }
}
#if SQL_LOG_FILE:
#    # only actually log to the logfile handler if a logfile was defined
#    LOGGING['loggers']['sql_logger']['handlers'] = ['sql_logfile']
#    LOGGING['handlers']['sql_logfile'] = {
#        'level': 'INFO',
#        'class': 'logging.FileHandler',
#        'formatter': 'verbose',
#        'filename': SQL_LOG_FILE,
#    }

if WEBSERVICE_LOG_FILE and WEBSERVICE_LOG_ENABLE:
    # only actually log to the logfile handler if a logfile was defined
    LOGGING['loggers']['ogv_webservice']['handlers'] = ['webservice_logfile']
    LOGGING['handlers']['webservice_logfile'] = {
        'level': 'INFO',
        'class': 'logging.FileHandler',
        'formatter': 'verbose',
        'filename': WEBSERVICE_LOG_FILE,
    }


############
# NewRelic #
############

NEWRELIC_ENABLED = get_config_or_none(config, 'NewRelic', 'enable', default=False) == 'yes'

##################
# Raven & Sentry #
##################

SENTRY_DSN = get_config_or_none(config, 'raven', 'dsn', default='')


###################
# Clamav Settings #
###################

CLAMAV_SOCKET_PATH = get_config_or_none(config, 'clamav', 'socket_path', default='')

if os.path.exists(CLAMAV_SOCKET_PATH):
    from onlinegv.utils import pyclamd

    pyclamd.init_unix_socket(CLAMAV_SOCKET_PATH)

    CLAMAV_ENABLED = True

else:
    CLAMAV_ENABLED = False
