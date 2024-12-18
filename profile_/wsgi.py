"""
WSGI config for profile_ project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import pathlib
from pathlib import Path




from django.core.wsgi import get_wsgi_application

BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'profile_.settings')

application = get_wsgi_application()
