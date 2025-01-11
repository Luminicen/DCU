from django.db import models
from django.contrib.auth.models import User
from django.db.models.functions import Now
# Create your models here.
# devolver la lista directamente con la API Django

class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    codigo  = models.FileField(upload_to='archivos_analisis/')
    usuario = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    fileName = models.CharField(max_length=255, null=True)
    analysisTime = models.DateTimeField(db_default=Now())

    def __str__(self):
        return "Reporde de " + self.nombre

class ConfiguracionUsuario(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    tamaño_letra = models.SmallIntegerField()
    tema = models.IntegerField()