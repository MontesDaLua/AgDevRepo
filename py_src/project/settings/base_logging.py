#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': True,
#    'formatters': {
#        'verbose': {
#            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
#        },
#        'simple': {
#            'format': '%(levelname)s %(message)s'
#        },
#    },
#    'handlers': {
#        'null': {
#            'level':'DEBUG',
#            'class':'django.utils.log.NullHandler',
#        },
#        'console':{
#            'level':'DEBUG',
#            'class':'logging.StreamHandler',
#            'formatter': 'simple'
#        },
#        'mail_admins': {
#            'level': 'ERROR',
#            'class': 'django.utils.log.AdminEmailHandler',
#        },
#        'sentry': {
#            'level': 'ERROR',
#            'class': 'sentry.client.handlers.SentryHandler'
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers':['null'],
#            'propagate': True,
#            'level':'INFO',
#        },
#        'django.request': {
#            'handlers': ['console','sentry'],
#            'level': 'ERROR',
#            'propagate': False,
#        },
#        'onlinegv': {
#            'handlers': ['console','sentry'],
#            'level': 'INFO',
#        },
#        'root': {
#            'handler': ['console', 'sentry'],
#            'level': 'INFO',
#        }
#    }
#}