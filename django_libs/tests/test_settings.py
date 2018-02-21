"""Settings that need to be set in order to run the tests."""
import os
import logging

from ..settings.django_settings import *  # NOQA


logging.getLogger("factory").setLevel(logging.WARN)


DEBUG = True
SITE_ID = 1

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', 'English'),
    ('de', 'Deutsch'),
]
USE_I18N = True
USE_L10N = True
USE_TZ = True


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

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
)

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': [os.path.join(os.path.dirname(__file__), 'test_app/templates')],
    'OPTIONS': {
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.i18n',
            'django.template.context_processors.request',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
        )
    }
}]

EXTERNAL_APPS = [
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
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

TEST_LOAD_MEMBER = 'django_libs.loaders.load_member'

DJANGO_LIBS_EMAIL_CONTEXT = 'django_libs.tests.utils.email_tests.context_fn'

AUTH_PROFILE_MODULE = 'django_libs.tests.test_app.DummyProfile'

ANALYTICS_TRACKING_ID = 'UA-THISISNOREAL-ID'
SECRET_KEY = 'foo'
