from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("registro/", views.register, name="register"),
    path("analysis", views.analysis, name="analysis"),
    path("results", views.results, name="results"),
    path('error_result/<str:analysis_id>/<str:file_name>/<str:detected_error>', views.error_result, name='error_result'),
    path('update_html/<str:analysis_id>/<str:detected_error>', views.update_html, name='update_html'),
    path("settings", views.settings, name="settings"),
    path("account", views.account, name="account"),
    path('cambiar-contraseña/', views.cambiar_contraseña, name='cambioContra'),
    path('cambiar-contraseña/hecho/', views.cambiar_contraseña_hecho, name='cambioContraDone'),
    path('password_reset/', views.password_reset_request, name='password_reset_request'),
    path('set_new_password/', views.set_new_password, name='set_new_password'),
    path('user_analysis_history/', views.user_analysis_history, name='user_analysis_history'),
    path('eliminar_reporte/<int:reporte_id>/', views.eliminar_reporte, name='eliminar_reporte'),
    path('descargar/<str:file_name>/', views.descargar_contenido, name='descargar_contenido')
]