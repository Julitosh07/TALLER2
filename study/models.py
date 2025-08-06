from django.db import models
from examenes.models import Category, Subject
from django.contrib.auth.models import User

# Create your models here.

class Subtema(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='subtemas')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} ({self.subject.nombre})"

class MaterialEstudio(models.Model):
    subtema = models.ForeignKey(Subtema, on_delete=models.CASCADE, related_name='materiales')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    explicacion = models.TextField(blank=True)
    tipo = models.CharField(max_length=50, choices=[
        ('video', 'Video'),
        ('pdf', 'PDF'),
        ('articulo', 'Artículo'),
    ])
    enlace = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

class UserMaterialEstudio(models.Model):
    materiales = models.ForeignKey(MaterialEstudio, on_delete=models.CASCADE, related_name='materiales')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuarios')
    visto = models.BooleanField(default=False)