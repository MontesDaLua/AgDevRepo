from project.settings.development_local import *

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': os.path.join(DATA_DIR,'onlinegv-soap.sqlite3'),
   },
}

INSTALLED_APPS += ['devserver',]

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
            'level':'ERROR',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'ogv_webservice.models': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}