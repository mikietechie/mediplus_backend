from .base import *


ALLOWED_HOSTS = ["mediplus.co.zw"]

CORS_ORIGIN_WHITELIST = ["mediplus.co.zw"]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('mediplus_db_password', 'a1mtwstdb'),
        'USER': os.getenv('mediplus_db_password', 'postgres'),
        'PASSWORD': os.getenv('mediplus_db_password', 'mediplus1234'),
        'HOST': os.getenv('mediplus_db_password', '127.0.0.1'),
        'PORT': os.getenv('mediplus_db_password', '5432')
    }
}