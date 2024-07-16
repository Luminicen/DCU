from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/", views.register, name="register"),
    path("analysis", views.analysis, name="analysis"),
    path("analysis/upload_html", views.upload_html, name="upload_html"),
    path("analysis/preferences", views.preferences, name="preferences"),
    path("analysis/preview", views.preview, name="preview"),
    path("results", views.results, name="results"),
    path("settings", views.settings, name="settings"),
]