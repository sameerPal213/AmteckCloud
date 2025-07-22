"""
WSGI config for am_nexus project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os, sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/home/ateam/am-nexus/am_nexus') #Project path

sys.path.append('/home/ateam/am-nexus/env') #venv path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'am_nexus.settings')

application = get_wsgi_application()
