# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

if DEBUG:
    from .development import *
else:
    from .production import *

if "test" in str(sys.argv):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }