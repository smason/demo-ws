"""
WSGI config for ccws project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ccws.settings")

djangoapp = get_wsgi_application()

def application(env, start_response):
    def fake_response(status, headers, *args,**kwargs):
        print repr(status), repr(headers), repr(args), repr(kwargs)

    if env['PATH_INFO'] == '/subscribe':
        djangoapp(env, fake_response)
        return []

    return djangoapp(env, start_response)
