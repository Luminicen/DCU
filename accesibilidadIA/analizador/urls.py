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
    path('error_result/<str:file_name>/<str:detected_error>', views.error_result, name='error_result'),
    path('update_html/<str:file_name>/', views.update_html, name='update_html'),
    path("settings", views.settings, name="settings"),
]