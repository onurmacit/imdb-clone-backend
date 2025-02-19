from .settings import *  
import os
import getpass

current_user = getpass.getuser()  

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'test_imdb',  
        'USER': current_user,  
        'PASSWORD': '',  
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'NAME': 'test_imdb',  
        },
    }
}


PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

CELERY_TASK_ALWAYS_EAGER = True
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'memory://')

DEBUG = os.getenv('DEBUG', 'True') == 'True'
