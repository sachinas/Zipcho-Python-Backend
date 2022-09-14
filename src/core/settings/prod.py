from .base import *

DEBUG = True

ALLOWED_HOSTS =['http://zipchodev.com/','zipchodev.com', '52.66.149.110', '0.0.0.0', 'http://52.66.149.110/']
CSRF_TRUSTED_ORIGINS= ['http://zipchodev.com/', 'zipchodev.com', 'http://52.66.149.110/', '52.66.149.110']
CORS_ORIGIN_ALLOW_ALL=True

CORS_ORIGIN_WHITELIST=[
    'http://127.0.0.1:9090',
    'http://127.0.0.1:8000',
    'http://52.66.149.110',
    'http://zipchodev.com'
]


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
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


INTERNAL_IPS = [
    '127.0.0.1',
]