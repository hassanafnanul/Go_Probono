from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-x=js4414xd7&eg=716%4_=5ytrm-vh%p2uel+iv=-2p91gc*1e'


DEBUG = True

ALLOWED_HOSTS = ['www.goprobono.org', 'goprobono.org', '36.255.71.251', '127.0.0.1']


INITIAL_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
    'rest_framework'
]

DEVELOPED_APPS = [
    'UserAuthentication',
    'ModuleManagement',
    'RoleAssignment',
    'RoleCreation',
    'LogWithAudit',
    'Customer',
    'LawManagement',
    'SliderManagement',
    'HelpCenter',
    'KnowYourLaw',
    'EventManagement',
    'TeamManagement',
    'LawyerManagement',
    'Appoinment',
    'Address',
    'Payment',
    'PaymentPlans',
    'CallHistory'
]

INSTALLED_APPS = INITIAL_APPS + THIRD_PARTY_APPS + DEVELOPED_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'token'
)

ROOT_URLCONF = 'Go_Probono.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [Path.joinpath(BASE_DIR, 'z_templates')],
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

WSGI_APPLICATION = 'Go_Probono.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        # 'ENGINE': 'django.db.backends.mysql',   # MySQL
        'ENGINE': 'django.db.backends.postgresql',   # PostGRE
        'NAME': 'go_probono',  
        'USER': 'root',
        'PASSWORD': 'root',  
        'HOST': '127.0.0.1',  
        # 'PORT': '3306',   # MySQL
        'PORT': '5432',   # PostGRE
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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




SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600
SESSION_SAVE_EVERY_REQUEST = True


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Etc/GMT-6'

USE_I18N = True

USE_L10N = True

USE_TZ = True


CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_ALLOW_NONIMAGE_FILES = False
CKEDITOR_REQUIRE_STAFF=False



# STATIC_ROOT = Path.joinpath(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    Path.joinpath(BASE_DIR, "static"),
)

MEDIA_ROOT = Path.joinpath(BASE_DIR, "media")
MEDIA_URL = '/media/'
MEDIA_DIRS = (
    Path.joinpath(BASE_DIR, "media"),
)

FILES_ROOT = Path.joinpath(BASE_DIR, "files")
FILES_URL = '/files/'
FILES_DIRS = (
    Path.joinpath(BASE_DIR, "files"),
)



LOGIN_REDIRECT_URL='/userauth/home/'
LOGIN_URL = 'loginpage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

