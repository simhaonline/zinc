"""
Django settings for zinc project.

Generated by 'django-admin startproject' using Django 1.9.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.getenv('ZINC_DATA_DIR', PROJECT_ROOT)
WEBROOT_DIR = os.getenv('ZINC_WEBROOT_DIR', os.path.join(PROJECT_ROOT,
                                                         'webroot/'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('ZINC_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('ZINC_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = list(map(lambda x: x.strip(),
                         os.getenv('ZINC_ALLOWED_HOSTS', '').split(',')))

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'dns',
    'lattice_sync',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zinc.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'zinc.wsgi.application'

DATA_DIR = os.getenv('ZINC_DATA_DIR', PROJECT_ROOT)


DATABASES = {
    'default': {
        'ENGINE': os.getenv('ZINC_DB_ENGINE',
                            'django.db.backends.sqlite3'),
        'USER': os.getenv('ZINC_DB_USER', 'zinc'),
        'PASSWORD': os.getenv('ZINC_DB_PASSWORD', 'password'),
        'HOST': os.getenv('ZINC_DB_HOST', ''),
        'PORT': os.getenv('ZINC_DB_PORT', ''),
    }
}

if DATABASES['default']['ENGINE'] == 'django.db.backends.sqlite3':
    DATABASES['default']['NAME'] = os.getenv('ZINC_DB_NAME',
                                             os.path.join(DATA_DIR, 'db.sqlite3'))
else:
    DATABASES['default']['NAME'] = os.getenv('ZINC_DB_NAME', 'zinc')


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = os.getenv('ZINC_STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(WEBROOT_DIR, 'static/')

# CELERY
BROKER_URL = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
CELERYBEAT_SCHEDULE = {
    'reconcile_policy_records': {
        'task': 'dns.tasks.reconcile_policy_records',
        'schedule': 30
    },
    'cleanup_deleted_zones': {
        'task': 'dns.tasks.cleanup_deleted_zones',
        'schedule': 300
    },
    'lattice_sync': {
        'task': 'lattice_sync.tasks.lattice_sync',
        'schedule': 30
    },
    'reconcile_healthchecks': {
        'task': 'dns.tasks.reconcile_healthchecks',
        # these are already performed synchronously, reconcile handles transient AWS errors,
        # so it doesn't need to run frequently
        'schedule': 300
    },
}

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# HASHIDS

HASHIDS_MIN_LENGTH = 0

AWS_KEY = ''
AWS_SECRET = ''

REST_FRAMEWORK = {
    'PAGE_SIZE': 100,
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

HEALTH_CHECK_CONFIG = {
    'Port': 80,
    'Type': 'HTTP',
    'ResourcePath': '/status',
    'FullyQualifiedDomainName': 'node.presslabs.net.',
}
LATTICE_URL = os.getenv('LATTICE_URL', 'https://lattice.presslabs.net/')
LATTICE_USER = os.getenv('LATTICE_USER')
LATTICE_PASSWORD = os.getenv('LATTICE_PASSWORD')
LATTICE_ROLES = list(map(lambda x: x.strip(),
                         os.getenv('LATTICE_ROLES', 'edge-node').split(',')))

AWS_KEY = os.getenv('ZINC_AWS_KEY')
AWS_SECRET = os.getenv('ZINC_AWS_SECRET')


# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('ZINC_LOG_LEVEL', 'INFO'),
        },
        'zinc': {
            'handlers': ['console'],
            'level': os.getenv('ZINC_LOG_LEVEL', 'INFO'),
        },
    },
}
if os.getenv('ZINC_SENTRY_DSN', None):
    import raven
    INSTALLED_APPS += ['raven.contrib.django.raven_compat']
    RAVEN_CONFIG = {
        'dsn': os.getenv('ZINC_SENTRY_DSN'),
        # If you are using git, you can also automatically configure the
        # release based on the git info.
        'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
    }

    # Sentry logging with celery is a real pain in the ass
    # https://github.com/getsentry/sentry/issues/4565
    CELERYD_HIJACK_ROOT_LOGGER = False
    LOGGING['handlers']['sentry'] = {
        'level': 'ERROR',
        'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler'
    }
    LOGGING['loggers']['celery.task'] = {
        'level': os.getenv('ZINC_LOG_LEVEL', 'INFO'),
        'handlers': ['console', 'sentry']
    }
    LOGGING['loggers']['zinc'] = {
        'level': os.getenv('ZINC_LOG_LEVEL', 'INFO'),
        'handlers': ['console', 'sentry']
    }
