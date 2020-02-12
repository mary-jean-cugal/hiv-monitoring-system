"""
WSGI config for aidsecure project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
import sys
#path = "/home/dlao/hiv-monitoring-system/venv/lib/python3.5/site-packages"
#if path not in sys.path:
#    sys.path.insert(0, path)

#from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aidsecure.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
