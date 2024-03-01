from django.urls import path
from Myapp import views
from django.conf import settings
from django.conf.urls.static import static

# from Myapp import correo

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar", views.buscar, name="buscar"),
    path("obtener_nombres_pdf", views.obtener_nombres_pdf, name="obtener_nombres_pdf"),
    path(
        "enviar_correo_django/<codigo>/",
        views.enviar_correo_django,
        name="enviar_correo_django",
    ),
    path(
        "buscar_pdf_similares", views.buscar_pdf_similares, name="buscar_pdf_similares"
    ),
]
