from .base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ["*"]

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
BACKEND_URL = "http://the-mechanic-backend-dev.herokuapp.com/api/v0/docs/"