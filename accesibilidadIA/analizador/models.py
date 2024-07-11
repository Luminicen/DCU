from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Reporte(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=255)
    usuario = models.ForeignKey(User,on_delete=models.DO_NOTHING)

    def __str__(self):
        return "Reporde de " + self.nombre
class ConfiguracionUsuario(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.DO_NOTHING)
    tamaño_letra = models.SmallIntegerField()
    tema = models.IntegerField()
