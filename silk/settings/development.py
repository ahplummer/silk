from base import *

DEBUG=True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'silk',
        'USER': 'silkuser',
        'PASSWORD': 'silkpass',
        'HOST': '127.0.0.1',
    }
}

