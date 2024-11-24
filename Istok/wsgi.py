"""
WSGI config for Istok project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Istok.settings')

application = get_wsgi_application()

# #### https://noumenal.es/notes/til/django/csrf-trusted-origins/
# django_app = get_wsgi_application()
#
#
# def https_app(environ, start_response):
#     environ["wsgi.url_scheme"] = "https"
#     return django_app(environ, start_response)
#
#
# application = https_app
