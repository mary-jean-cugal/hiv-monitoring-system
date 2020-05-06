import os
import json

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aidsecure.settings")

if os.name == 'nt':
    import platform
    OSGEO4W = r"C:\OSGeo4W"
    if '64' in platform.architecture()[0]:
        OSGEO4W += "64"
    assert os.path.isdir(OSGEO4W), "Directory does not exist: " + OSGEO4W
    os.environ['OSGEO4W_ROOT'] = OSGEO4W
    os.environ['GDAL_DATA'] = OSGEO4W + r"\share\gdal"
    os.environ['PROJ_LIB'] = OSGEO4W + r"\share\proj"
    os.environ['PATH'] = OSGEO4W + r"\bin;" + os.environ['PATH']

#django.setup()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


with open('/etc/aidsecure/config.json') as config_file:
    config = json.load(config_file)

SECRET_KEY =  config['SECRET_KEY']
#DEBUG = True
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.0','i153-70.upd.edu.ph', '202.92.153.70']


CSRF_COOKIE_DOMAIN = None


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # for map
    'django.contrib.gis',
    'leaflet',
    'djgeojson',
    'xhtml2pdf',

    # for db management
    'dbbackup', 
    'storages',
    'paramiko',

    # apps
    'portal',
    'doctor',
    'patient',
    'cebuMap',
    'backup_and_restore', 
]

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'data-backup/backups/'}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'aidsecure.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'aidsecure.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'aidsecure_storage',
        'USER': config.get('DB_USER'),
        'HOST': '',
        'PASSWORD': config.get('DB_PASSWORD'),
        'PORT': '',
    }
}


# Password validation
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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/dlao/hiv-monitoring-system/aidsecure/profile-pictures/media/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'aidsecure/static/'),
    os.path.join(BASE_DIR, 'portal/static/'),
    os.path.join(BASE_DIR, 'cebuMap/static/'),    
)
