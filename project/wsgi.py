"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

import django
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

django.setup(set_prefix=False)
from django.conf import settings

application = get_wsgi_application()
if not settings.DEBUG:
    application = DjangoWhiteNoise(application)
