
import os
from django.core.wsgi import get_wsgi_application

# Establece la configuración predeterminada de Django para el proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')

# Obtén la aplicación WSGI de Django
application = get_wsgi_application()
