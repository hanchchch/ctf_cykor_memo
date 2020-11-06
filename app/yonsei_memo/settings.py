from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'KOREA{th4t_w4snt_r3a1_h0st_n4m3_4nd_th4t_w4snt_re4l_t3mp1at3}'
HOSTNAME = '211.217.69.153'

DEBUG = False

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'admin.apps.AdminConfig',
    'memo.apps.MemoConfig',
]

MIDDLEWARE = [

]

ROOT_URLCONF = 'yonsei_memo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR],
        'APP_DIRS': False,
    },
]

WSGI_APPLICATION = 'yonsei_memo.wsgi.application'

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

