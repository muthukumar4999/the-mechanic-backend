from .base import *
from .base import *
import dj_database_url

DEBUG = os.environ.get('DEBUG').lower() == 'true'

ALLOWED_HOSTS = ["*"]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_HOST = 'https://d4663kmspf1sqa.cloudfront.net' if not DEBUG else ''
STATIC_URL = STATIC_HOST + '/static/'
MIDDLEWARE.append('whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
try:
    from .databases import DBCONFIG

except ModuleNotFoundError:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                             'NAME': 'themechanic',
                             'HOST': 'localhost',
                             'PORT': 5432,
                             'USER': 'muthukumar',
                             'PASSWORD': 'muthukumar',
                             'ATOMIC_REQUESTS': True,
                             }
                 }
else:
    DATABASES = DBCONFIG

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

EMAIL_HOST_USER = 'themechanicbot@gmail.com'
EMAIL_HOST_PASSWORD = 'TheMechanic123'
BACKEND_URL = "http://the-mechanic-backend.herokuapp.com/api/v0/docs/"
