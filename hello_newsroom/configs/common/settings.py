import os
import django

# Base paths
DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Debugging
DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'beatboxdb',                      # Or path to database file if using sqlite3.
        'USER': 'beatbox:',                      # Not used with sqlite3.
        'PASSWORD': 'shamoo5',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Local time
TIME_ZONE = 'America/Chicago'

# Local language
LANGUAGE_CODE = 'en-gb'

# Site framework
SITE_ID = 1

# Internationalization
USE_I18N = False

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(SITE_ROOT, 'assets')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '%zz*y$4lq&ji+d0==wy9jt$v19l&1#31pj)s_ahy+gtr5vld)#'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
    'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    #'django.middleware.common.CommonMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'hello_newsroom.configs.common.urls'

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.gis',
    'django.contrib.sitemaps',
    'hello_newsroom.apps.core',
    'django.contrib.auth' 
)

# Predefined domain
MY_SITE_DOMAIN = 'localhost:8000'

# Email
# run "python -m smtpd -n -c DebuggingServer localhost:1025" to see outgoing
# messages dumped to the terminal
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
DEFAULT_FROM_EMAIL = 'do.not.reply@tribune.com'

# Caching
CACHE_MIDDLEWARE_KEY_PREFIX='hello_newsroom'
CACHE_MIDDLEWARE_SECONDS=90 * 60 # 90 minutes
CACHE_BACKEND="dummy:///"

# Analytics
OMNITURE_PAGE_NAME = "hello_newsroom"
OMNITURE_SECTION = ""
OMNITURE_SUBSECTION = ""
GOOGLE_ANALYTICS_KEY = ""

GOOGLE_MAPS_API_KEY = "ABQIAAAA3uGjGrzq3HsSSbZWegPbIhSMhkig1Gd5B_2j4H1Xz7hsATFBFhSnBeYqZ7F7xlyJh-_KEClsWgAO6Q" # for all 'amazonaws.com'

# Allow for local (per-user) override
try:
    from local_settings import *
except ImportError:
    pass
