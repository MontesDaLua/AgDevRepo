# -*- coding: utf-8 -*-
#from base_paths import *
#from base_secrets import *
from base_i18n import *
from base_cms import *

import os
ugettext = gettext = lambda s: s

import re

# it's used in email, templates, etc for standardization.
APPLICATION_NAME = 'Sherpany'

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = False

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_NAME = 'onlinegv_session_id'

TEMPLATE_DEBUG = DEBUG
PREPEND_WWW = False
FORCE_SCRIPT_NAME = ''

ADMINS = [('onlineGV Developers', 'onlinegv-developers@divio.ch')]

USE_ETAGS = False

INTERNAL_IPS = ['127.0.0.1',]

PUBLIC_URLS = [
    r'^admin/(.*)',
    r'^nexus/(.*)',
    #r'^admin/filer/clipboard/operations/upload/',

]



STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "project.staticfiles_finders.AppDirectoriesFinderAsMedia",
)

STATIC_URL = '/static/'
FILER_STATICMEDIA_PREFIX = os.path.join(STATIC_URL, 'filer')
FILER_IS_PUBLIC_DEFAULT = True
CMS_MEDIA_URL = "/static/cms/"
TINYMCE_JS_URL = STATIC_URL + 'js/tiny_mce/tiny_mce.js'

OGV_DOCUMENTS_ALLOWED_UPLOAD_MIMETYPES = [
    'application/pdf', # pdf
    'application/msword', # doc
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document', # docx
    'application/vnd.ms-powerpoint', # ppt
    'application/vnd.openxmlformats-officedocument.presentationml.presentation', #pptx
    'application/vnd.ms-excel', # xls
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', # xlsx
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

MANAGERS = ADMINS

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': 'template.sqlite3',
   },
}

TIME_ZONE = 'Europe/Zurich'

SITE_ID = 1

ROOT_URLCONF = 'project.urls'

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

SECRET_KEY = 'apusihvaèsovhèairvienhè]vhsjèv¬½¼@spuhvdspovhus!äüö£'

TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'project.middleware.request_id.SetUniqueRequestUuid',
    'djangosecure.middleware.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'localeurl.middleware.LocaleURLMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
]

TEMPLATE_CONTEXT_PROCESSORS = [
    "django.core.context_processors.i18n",
    "django.core.context_processors.debug",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    "onlinegv.context_processors.company_list_context_processor",
    "onlinegv.context_processors.user_authorization_context_processor",
    'onlinegv.context_processors.default_context',
    "sekizai.context_processors.sekizai",
    "notifyme_onsite.context_processors.sticky_notifications",
    'cms.context_processors.media'
]

INSTALLED_APPS = [
    'ogv_monkeypatches',
    'project',
    'cms',
    'localeurl', # Should be first!

    # django core apps
    'django.contrib.auth',
    'django.contrib.staticfiles',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',

    # tools
    'nexus',
    'gargoyle',
    'django_jenkins',
    'raven.contrib.django',

    # standard plugins
    'cms.plugins.link',
    'cms.plugins.snippet',
    'cms.plugins.text',

    # 3rd party apps
    'filer',
    'menus',
    'mptt',
    'sekizai',
    'easy_thumbnails',
    'south',
    'tinymce',
    'floppyforms',
    'snippets',

    #Security
    'rulez',

    # custom apps
    'onlinegv',
    'ogv_webservice',
    'ogv_testdata',
    'ogv_documents',
    'ogv_wizard',
    'ogv_notification',
    'ogv_authdoc_import',
    'ogv_orders',
    'ogv_consistency_checker',
    'ogv_mailing',
    'ogv_testmail',
    'custom_company',
    'nani',
    'djcelery',
    'notifyme',
    'notifyme_onsite',
    'notifyme_by_email',
    'database_email_backend',
    'contactform',
    'uni_form',
    'sendsms_admin',
    'mtan_login',
    'health_check',
    'health_check_celery',
    'health_check_db',
    'health_check_cache',
    'phonenumber_field', # only here because of tests
    'ogv_password_reset',
    'djangosecure',
    'jsonfield',
    'actstream',
    'tastypie',
    'templatetag_handlebars',

    # Internal Applications
    'sherpany_contact',
    'sherpany_faq',
    'sherpany_flatpage',
    'sherpany_qa',
    'sherpany_watchlist',
    'sherpany_org',

    # Obsoleted Applications
    # TODO: remove cms application with all it's plugins after migration.
    'cmsplugin_multiple_faq',
]

SERVER_EMAIL = 'django@%s' % os.uname()[1]
EMAIL_BACKEND = "django_multiple_email_backends.backend.CombinedEmailBackend"
EMAIL_BACKEND_LIST = ['django.core.mail.backends.console.EmailBackend',
                      'database_email_backend.backend.DatabaseEmailBackend']

#SENDSMS_BACKEND = 'sendsms_admin.backend.DatabaseSmsBackend'
SENDSMS_BACKEND = 'sendsms.backends.console.SmsBackend'
SENDSMS_DEFAULT_FROM_PHONE = '+41798137382'

DATE_FORMAT = 'd.m.Y'
DATETIME_FORMAT = 'd.m.Y H:i'
TIME_FORMAT = 'H:i'
YEAR_MONTH_FORMAT = 'F Y'
MONTH_DAY_FORMAT = 'j. F'

AUTHENTICATION_BACKENDS = [
    'onlinegv.auth_backend.EmailOrUsernameModelBackend',
    'mtan_login.auth_backend.MTANBackend',
#    'django.contrib.auth.backends.ModelBackend',
#    'login_as.auth_backend.LoginAsBackend',
    'rulez.backends.ObjectPermissionBackend',
]

AUTH_PROFILE_MODULE = 'onlinegv.UserProfile'

THUMBNAIL_BASEDIR = 'tmp'
THUMBNAIL_QUALITY = 70
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'project.thumbnail_processors.inactive',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

SOUTH_TESTS_MIGRATE = False

JENKINS_TASKS = (
#    'django_jenkins.tasks.run_pylint', # pylint fails on osx
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.django_tests',
)

LOCALE_INDEPENDENT_PATHS = [
    re.compile(r'^/api/.*'),
    re.compile(r'^/documents/.*'),
    re.compile(r'^/media/.*'),
    re.compile(r'^/static/.*'),
    re.compile(r'^/ht/.*'),
]



import djcelery
djcelery.setup_loader()

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"

NOTIFYME_USE_CELERY = True


NANI_TABLE_NAME_SEPARATOR = ""

EMAIL_DEFAULT_RECEIVER = ['onlinegv-developers@divio.ch']

## Activity Stream Settings
ACTSTREAM_SETTINGS = {
    'MODELS': (
        'auth.user',
        'onlinegv.company',
        'onlinegv.assembly',
        'ogv_documents.document',
        'sherpany_qa.qa',
    ),
    'MANAGER': 'actstream.managers.ActionManager',
    'USE_JSONFIELD': True
}

## Contact Settings
SHERPANY_CONTACT_EMAILS = ['info@agilentia.ch']

## Django Tastypie Settings
API_LIMIT_PER_PAGE = 15

## Boardroom Settings
BOARDROOM_URL = 'https://board.sherpany.com'

## Whitepaper Settings
WHITEPAPER_EMAILS = ['contact@sherpany.com']
