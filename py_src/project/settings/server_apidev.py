from project.settings.server_dev import *

#BROKER_USER = 'onlinegv-apidev'
#BROKER_PASSWORD = 'kPFwm?>Scs0lq9PeY'
#BROKER_VHOST = '/onlinegv/apidev'

SENTRY_SITE = 'onlinegv-apidev'

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "onlinegv-apidev",
        'USER': "onlinegv-apidev",
    }
}

try:
    # this loads the sendsms and email config!
    from django_settings import *
except ImportError, e:
    print 'ImportError: ', e
