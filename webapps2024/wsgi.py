"""
WSGI config for webapps2024 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
# from timestamp_service.views import start_timestamp_server

# start_timestamp_server()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapps2024.settings')

application = get_wsgi_application()
