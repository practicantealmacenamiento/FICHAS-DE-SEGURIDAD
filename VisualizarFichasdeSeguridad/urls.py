from django.urls import path
from Myapp import views  # Ajsusta la importación según la estructura de tu proyecto
from Myapp import correo

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar", views.buscar, name="buscar"),
    path(
        "enviar_correo_django",
        correo.enviar_correo_django,
        name="enviar_correo_outlook",
    ),
]
