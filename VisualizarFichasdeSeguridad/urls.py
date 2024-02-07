from django.urls import path
from Myapp import views  # Ajsusta la importación según la estructura de tu proyecto

urlpatterns = [
    path("", views.index, name="index"),
    path("buscar", views.buscar, name="buscar"),
]
