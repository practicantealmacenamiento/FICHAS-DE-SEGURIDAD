import os
from waitress import serve
from dj_static import Cling
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VisualizarFichasdeSeguridad.settings")

application = Cling(get_wsgi_application())

serve(application, host="0.0.0.0", port=8082)
