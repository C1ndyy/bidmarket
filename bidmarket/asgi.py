"""
ASGI config for bidmarket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.bidmarket.asgi import get_asgi_application
import bidmarket.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bidmarket.settings')

application = get_asgi_application()
