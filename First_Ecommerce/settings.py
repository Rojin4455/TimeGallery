# settings.py

from pathlib import Path
from dotenv import load_dotenv
import os
from django.urls import reverse_lazy


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = True

ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = ['https://api.razorpay.com']

LOGIN_REDIRECT_URL = '/'
# ACCOUNT_LOGOUT_REDIRECT_URL = '/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_app',
    'admin_app',
    'category',
    'store',
    'user_management',
    'product_management',
    'cart_app',
    'checkout_app',
    'orders',
    'order_management',
    'wallet',
    'admin_dashboard',
    'offer_management',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook', 
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "allauth.account.middleware.AccountMiddleware",

]

ROOT_URLCONF = 'First_Ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        # 'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 'django.contrib.messages.context_processors.messages',
                'category.context_processors.menu_links',
                'cart_app.context_processors.counter',
                'cart_app.context_processors.global_order_summary',  # Replace 'myapp' with your app name

                
            ],
        },
    },
]

WSGI_APPLICATION = 'First_Ecommerce.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': os.environ['ENGINE'],
        'NAME': os.environ['NAME'],
        'USER': os.environ['USER'],
        'PASSWORD': os.environ['PASSWORD'],
        'HOST': os.environ['HOST'],
        'PORT': os.environ['PORT'],
    }
}

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

USE_TZ = True

#Email Config

EMAIL_BACKEND       = os.environ["EMAIL_BACKEND"]
EMAIL_HOST          = os.environ["EMAIL_HOST"]
EMAIL_USE_TLS       = os.environ["EMAIL_USE_TLS"]
EMAIL_PORT          = os.environ["EMAIL_PORT"]
EMAIL_HOST_USER     = os.environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"] 


STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media/')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [

    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_LOGIN_ON_GET=True

AUTH_USER_MODEL = 'admin_app.User'

LOGIN_URL = reverse_lazy('user_app:login')
# LOGIN_URL_ADMIN = reverse_lazy('admin_app:admin_login')

RAZOR_PAY_KEY_ID = 'rzp_test_dSu8p6gC5RjeXR'
KEY_SECRET = 'gbLg8Tb8J5mNibxFPEOcrNKX'

SESSION_COOKIE_AGE = 3600  # 1 hour in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False




