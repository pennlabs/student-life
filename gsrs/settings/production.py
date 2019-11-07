import os

# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

from gsrs.settings.base import *  # noqa


DEBUG = False

# Fix MySQL Emoji support
DATABASES['default']['OPTIONS'] = {'charset': 'utf8mb4'}

# Honour the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow production host headers
ALLOWED_HOSTS = [BACKEND_DOMAIN]

SENTRY_URL = os.environ.get('SENTRY_URL', '')

# sentry_sdk.init(
#     dsn=SENTRY_URL,
#     integrations=[DjangoIntegration()]
# )

###############################################################
# SETTINGS TO ALLOW FRONTEND TO MAKE AJAX REQUESTS TO BACKEND #
###############################################################
# DO NOT USE IF DJANGO APP IS STANDALONE
# Django CORS Settings
CORS_ORIGIN_WHITELIST = [
    'https://www.{}'.format(FRONTEND_DOMAIN),
    'https://{}'.format(FRONTEND_DOMAIN),
]

CSRF_TRUSTED_ORIGINS = [
    '.' + FRONTEND_DOMAIN,
    FRONTEND_DOMAIN,
]