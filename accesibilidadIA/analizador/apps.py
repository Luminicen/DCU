from django.apps import AppConfig


class AnalizadorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'analizador'

class Settings(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'settings'

class Results(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'results'