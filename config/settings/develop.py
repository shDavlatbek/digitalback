from .base import *
# from corsheaders.defaults import default_headers

DEBUG = True

ALLOWED_HOSTS = ['*']

# STATIC_URL = 'https://cdn-test.e-bmsm.uz/static/'
# MEDIA_URL  = 'https://cdn-test.e-bmsm.uz/media/'


CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CSRF_TRUSTED_ORIGINS = env.list('CSRF_TRUSTED_ORIGINS')
CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']

IMGPROXY_BASE_URL = env.str('IMGPROXY_BASE_URL', 'http://localhost:6008')
# CORS_ALLOW_HEADERS = list(default_headers) + ["School"]
IMGPROXY_KEY='9f3c1a7b8e2d4c6f0b1e9a3d5f7c2a4e8b6d0f3a1c9e7b5d2f4a6c8e1b3d5f7a9c2e4b6d8f0a1c3e5b7d9f2a4c6e8b0d'
IMGPROXY_SALT='c4a9e1d7b2f83c6e5a0d9b1f4e7c2a6d8f3b0e1c9a7d5f2b6c4e8a1d3f9b7c0e2a5d6f8c1b3e9a0d4c7f2e6b8a1d3c'