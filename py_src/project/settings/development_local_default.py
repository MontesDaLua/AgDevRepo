from project.settings.development_local import *
from project.settings.base import INSTALLED_APPS

INSTALLED_APPS += ('django_extensions',)

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(DATA_DIR,'sherpany.sqlite3'),
   },
}

## Sentry && Raven Settings
# SENTRY_DSN = ''

## Clamav Settings
CLAMAV_SOCKET_PATH = '/tmp/clamd.socket'

if os.path.exists(CLAMAV_SOCKET_PATH):
    from onlinegv.utils import pyclamd

    pyclamd.init_unix_socket(CLAMAV_SOCKET_PATH)
    print("Clamav enabled: %s" % pyclamd.version())

    CLAMAV_ENABLED = True

else:
    CLAMAV_ENABLED = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
