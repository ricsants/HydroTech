"""
WSGI config for production with Gunicorn.

To run:
gunicorn app.wsgi:application --workers 4 --bind 0.0.0.0:8000
"""

import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'))
