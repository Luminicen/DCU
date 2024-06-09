from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/", views.register, name="register"),
    path("analysis", views.analysis, name="analysis"),
    path("results", views.results, name="results"),
    path("settings", views.settings, name="settings"),
]