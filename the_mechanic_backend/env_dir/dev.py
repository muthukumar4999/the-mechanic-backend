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
                             'USER': 'dev',
                             'PASSWORD': 'dev',
                             'ATOMIC_REQUESTS': True,
                             }
                 }
else:
    DATABASES = DBCONFIG

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

EMAIL_HOST_USER = 'ixespresso@gmail.com'
EMAIL_HOST_PASSWORD = 'Espresso@1'
