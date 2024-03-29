"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "cc)*5=(s+i2-&9x7&&&o+y7$g5!db3tvu85ykok#mwxf#6gir2"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

PROJECT_APPS = [
    "core.apps.CoreConfig",
    "users.apps.UsersConfig",
    "rooms.apps.RoomsConfig",
]

THIRD_PARTY_APPS = [
    "rest_framework",
]

INSTALLED_APPS = DJANGO_APPS + PROJECT_APPS + THIRD_PARTY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "uploads")

MEDIA_URL = "/media/"


# Auth

AUTH_USER_MODEL = "users.User"

# http://www.cdrf.co/
# Django Rest Framework

REST_FRAMEWORK = {
    # DRF의 view에서 전달하는 모든 api 데이터에 대하여 pagination을 적용하는 경우 다음과 같이 사용
    # 공식문서에 보면 더 많은 종류의 pagination이 있
    # https://www.django-rest-framework.org/api-guide/pagination/#api-reference
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    # 2가지 인증방식을 갖게 됨
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # session을 이용한 인증방식
        # -> api로 정보를 보냄으로써 user가 누군지 확인하는 방식
        "rest_framework.authentication.SessionAuthentication",
        # 다른 인증방식 구현 -> custom authentication
        # -> header에 담긴 token 정보를 이용하여 user가 누군지 확인하는 방식
        # 밑의 문서를 참고할 것
        # https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication
        "config.authentication.JWTAuthentication",
    ],
}


# Rest_Framework 팁
# 1. AWS에 deploy할때 WSGIPassAuthorization를 On 해줘야하만 한다
# https://www.django-rest-framework.org/api-guide/authentication/#apache-mod_wsgi-specific-configuration
# https://docs.aws.amazon.com/ko_kr/elasticbeanstalk/latest/dg/create-deploy-python-container.html

# 2.renderers
# renderers는 일반유저들에게 내가 만든 api 페이지를 보여주지 않기 위해 설정하는 것이다
# https://www.django-rest-framework.org/api-guide/renderers/
# REST_FRAMEWORK = {
#     'DEFAULT_RENDERER_CLASSES': [
#         'rest_framework.renderers.JSONRenderer',
#         'rest_framework.renderers.BrowsableAPIRenderer',
#     ]
# }
# 기본적으로 'rest_framework.renderers.BrowsableAPIRenderer',로 세팅되어 있는데 settings.py에서 DEBUG가 False일때(=deploy를 했다는 의미)는 이 설정을 꺼주도록 만들어야한다
if not DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [
        "rest_framework.renderers.JSONRenderer",
    ]

# 3.throttling
# 하루에 얼만큼 api를 요청할 수 있는지 설정
# https://www.django-rest-framework.org/api-guide/throttling/

# 4.
