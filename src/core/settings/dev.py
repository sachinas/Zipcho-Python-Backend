from .base import *

DEBUG = True

ALLOWED_HOSTS =['127.0.0.1', 'http://zipchodev.com/','zipchodev.com', '65.0.89.205',
                '0.0.0.0', 'http://65.0.89.205/']

CSRF_TRUSTED_ORIGINS= ['http://zipchodev.com/', 'zipchodev.com',
                         'http://65.0.89.205/', '65.0.89.205']
                         
CORS_ORIGIN_ALLOW_ALL=True

CORS_ORIGIN_WHITELIST=[
    'http://127.0.0.1:9090',
    'http://127.0.0.1:8000',
    'http://65.0.89.205',
    'http://zipchodev.com'
]

INSTALLED_APPS += [
    'debug_toolbar'
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]


MIDDLEWARE +=[
     'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'zipchoDevDB',
        'OPTIONS' : {
            'read_default_file': '/etc/mysql/my.cnf',
            'charset':'utf8mb4'
        },
    }
}

# DEBUG TOOLBAR SETTINGS 
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'debug_toolbar.panels.profiling.ProfilingPanel',
]

def show_toolbar(request):
    return True

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECT' : False,
    'SHOW_TOOLBAR_CALLBACK': show_toolbar
}