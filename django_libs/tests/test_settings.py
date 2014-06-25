"""Settings that need to be set in order to run the tests."""
import os


PROJECT_ROOT = os.path.dirname(__file__)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

ROOT_URLCONF = 'django_libs.tests.urls'

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(__file__, '../../static/')
MEDIA_ROOT = os.path.join(__file__, '../../media/')
STATICFILES_DIRS = (
    os.path.join(__file__, 'test_static'),
)

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'test_app/templates'),
)

COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(
    os.path.dirname(__file__), 'coverage')
COVERAGE_MODULE_EXCLUDES = [
    'tests$', 'settings$', 'urls$', 'locale$',
    'migrations', 'fixtures', 'admin$', 'django_extensions',
    'testrunner',
]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django_nose',
    'mailer',
]

INTERNAL_APPS = [
    'django_libs',
    'django_libs.tests.test_app',
]

INSTALLED_APPS = EXTERNAL_APPS + INTERNAL_APPS
COVERAGE_MODULE_EXCLUDES += EXTERNAL_APPS

TEST_LOAD_MEMBER = 'django_libs.loaders.load_member'

AUTH_PROFILE_MODULE = 'test_app.DummyProfile'

ANALYTICS_TRACKING_ID = 'UA-THISISNOREAL-ID'
