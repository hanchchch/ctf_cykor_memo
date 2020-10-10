from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'KOREA{flag}'
DOMAIN = '127.0.0.1:8080'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'admin.apps.AdminConfig',
    'memo.apps.MemoConfig',
]

MIDDLEWARE = [

]

ROOT_URLCONF = 'cykor_memo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
        'APP_DIRS': False,
    },
]

WSGI_APPLICATION = 'cykor_memo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

