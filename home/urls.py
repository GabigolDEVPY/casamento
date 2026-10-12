from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.Home.as_view(), name="home"),
    path("confirmar-presenca/", views.confirmar_presenca, name="confirmar_presenca"),
    path("confirmar-presente/", views.confirmar_presente, name="confirmar_presente"),
]
