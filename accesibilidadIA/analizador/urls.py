from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/", views.register, name="register"),
    path("analysis", views.analysis, name="analysis"),
    path("results", views.results, name="results"),
    path('error_result/<str:analysis_id>/<str:file_name>/<str:detected_error>', views.error_result, name='error_result'),
    path('update_html/<str:file_name>/', views.update_html, name='update_html'),
    path("settings", views.settings, name="settings"),
    path('user_analysis_history/', views.user_analysis_history, name='user_analysis_history')
]