#!/bin/bash

SUPER_USER_EMAIL=${SUPERUSER_EMAIL:-"adminidein@gmail.com"}
cd /app/

/opt/venv/bin/python manage.py migrate --noinput    
/opt/venv/bin/python manage.py createsuperuser --email $SUPER_USER_EMAIL --noinput || true