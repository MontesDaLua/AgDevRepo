from project.settings.server_demo import *

SENTRY_SITE = 'onlinegv-apidev'

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "onlinegv-bosw",
        'USER': "onlinegv-bosw",
    }
}

try:
    # this loads the sendsms and email config!
    from django_settings import *
except ImportError, e:
    print 'ImportError: ', e

MEDIA_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'upload'))
STATIC_ROOT = os.path.abspath(os.path.join(DATA_DIR, 'static'))