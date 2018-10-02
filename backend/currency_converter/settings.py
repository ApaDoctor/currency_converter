"""
Django settings for currency_converter project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

import environ

env = environ.Env()
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z1vl^cgrhibb#l@b0j2v*q-=z)-_3*73tgsw34@zo8p9s1^0s!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'api',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django.contrib.admindocs.middleware.XViewMiddleware'
]

ROOT_URLCONF = 'currency_converter.urls'

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

WSGI_APPLICATION = 'currency_converter.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'cc_dsk',
#         'USER': 'cc_dsk',
#         'PASSWORD': '4g5h453dfs32sd32',
#         'HOST': 'db',
#         'PORT': '5432',
#     }
# }
if env('TRAVIS_CI', default=False):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'cc_dsk',
            'USER': 'cc_dsk',
            'PASSWORD': '4g5h453dfs32sd32',
            'HOST': 'db',
            'PORT': '5432',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'mydatabase',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

SUPPORTED_CURRENCIES = {'AED': 'United Arab Emirates Dirham', 'AFN': 'Afghan Afghani', 'ALL': 'Albanian Lek',
                        'AMD': 'Armenian Dram', 'ARS': 'Argentine Peso', 'AUD': 'Australian Dollar',
                        'AZN': 'Azerbaijani Manat', 'BAM': 'Bosnia-Herzegovina Convertible Mark',
                        'BDT': 'Bangladeshi Taka', 'BGN': 'Bulgarian Lev', 'BHD': 'Bahraini Dinar',
                        'BIF': 'Burundian Franc', 'BND': 'Brunei Dollar', 'BOB': 'Bolivian Boliviano',
                        'BRL': 'Brazilian Real', 'BWP': 'Botswanan Pula', 'BYR': 'Belarusian Ruble',
                        'BZD': 'Belize Dollar', 'CAD': 'Canadian Dollar', 'CDF': 'Congolese Franc',
                        'CHF': 'Swiss Franc', 'CLP': 'Chilean Peso', 'CNY': 'Chinese Yuan', 'COP': 'Colombian Peso',
                        'CRC': 'Costa Rican Colón', 'CVE': 'Cape Verdean Escudo', 'CZK': 'Czech Republic Koruna',
                        'DJF': 'Djiboutian Franc', 'DKK': 'Danish Krone', 'DOP': 'Dominican Peso',
                        'DZD': 'Algerian Dinar', 'EGP': 'Egyptian Pound', 'ERN': 'Eritrean Nakfa',
                        'ETB': 'Ethiopian Birr', 'EUR': 'Euro', 'GBP': 'British Pound Sterling', 'GEL': 'Georgian Lari',
                        'GHS': 'Ghanaian Cedi', 'GNF': 'Guinean Franc', 'GTQ': 'Guatemalan Quetzal',
                        'HKD': 'Hong Kong Dollar', 'HNL': 'Honduran Lempira', 'HRK': 'Croatian Kuna',
                        'HUF': 'Hungarian Forint', 'IDR': 'Indonesian Rupiah', 'ILS': 'Israeli New Sheqel',
                        'INR': 'Indian Rupee', 'IQD': 'Iraqi Dinar', 'IRR': 'Iranian Rial', 'ISK': 'Icelandic Króna',
                        'JMD': 'Jamaican Dollar', 'JOD': 'Jordanian Dinar', 'JPY': 'Japanese Yen',
                        'KES': 'Kenyan Shilling', 'KHR': 'Cambodian Riel', 'KMF': 'Comorian Franc',
                        'KRW': 'South Korean Won', 'KWD': 'Kuwaiti Dinar', 'KZT': 'Kazakhstani Tenge',
                        'LBP': 'Lebanese Pound', 'LKR': 'Sri Lankan Rupee', 'LTL': 'Lithuanian Litas',
                        'LVL': 'Latvian Lats', 'LYD': 'Libyan Dinar', 'MAD': 'Moroccan Dirham', 'MDL': 'Moldovan Leu',
                        'MGA': 'Malagasy Ariary', 'MKD': 'Macedonian Denar', 'MMK': 'Myanma Kyat',
                        'MOP': 'Macanese Pataca', 'MUR': 'Mauritian Rupee', 'MXN': 'Mexican Peso',
                        'MYR': 'Malaysian Ringgit', 'MZN': 'Mozambican Metical', 'NAD': 'Namibian Dollar',
                        'NGN': 'Nigerian Naira', 'NIO': 'Nicaraguan Córdoba', 'NOK': 'Norwegian Krone',
                        'NPR': 'Nepalese Rupee', 'NZD': 'New Zealand Dollar', 'OMR': 'Omani Rial',
                        'PAB': 'Panamanian Balboa', 'PEN': 'Peruvian Nuevo Sol', 'PHP': 'Philippine Peso',
                        'PKR': 'Pakistani Rupee', 'PLN': 'Polish Zloty', 'PYG': 'Paraguayan Guarani',
                        'QAR': 'Qatari Rial', 'RON': 'Romanian Leu', 'RSD': 'Serbian Dinar', 'RUB': 'Russian Ruble',
                        'RWF': 'Rwandan Franc', 'SAR': 'Saudi Riyal', 'SDG': 'Sudanese Pound', 'SEK': 'Swedish Krona',
                        'SGD': 'Singapore Dollar', 'SOS': 'Somali Shilling', 'SYP': 'Syrian Pound', 'THB': 'Thai Baht',
                        'TND': 'Tunisian Dinar', 'TOP': 'Tongan Paʻanga', 'TRY': 'Turkish Lira',
                        'TTD': 'Trinidad and Tobago Dollar', 'TWD': 'New Taiwan Dollar', 'TZS': 'Tanzanian Shilling',
                        'UAH': 'Ukrainian Hryvnia', 'UGX': 'Ugandan Shilling', 'USD': 'US Dollar',
                        'UYU': 'Uruguayan Peso', 'UZS': 'Uzbekistan Som', 'VEF': 'Venezuelan Bolívar',
                        'VND': 'Vietnamese Dong', 'XAF': 'CFA Franc BEAC', 'XOF': 'CFA Franc BCEAO',
                        'YER': 'Yemeni Rial', 'ZAR': 'South African Rand', 'ZMK': 'Zambian Kwacha'}

EXCHANGE_RATE_PROVIDER = 'ratesapi'
