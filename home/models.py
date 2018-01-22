from django.db import models

from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField

from isbn_field import ISBNField

import datetime
import uuid

class Model(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True
        ordering = ['created_at',]

class Autor(Model):
    nombre = models.CharField("Nombre", max_length=255)
    apellido = models.CharField("Apellido", max_length=255)
    texto = models.TextField("Texto")
    imagen = VersatileImageField('Foto', upload_to="autor/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Autores"


class Coleccion(Model):
    nombre = models.CharField("Nombre", max_length=255)

    class Meta:
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"

class Libro(Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    titulo = models.CharField("Titulo", max_length=500)
    isbn = ISBNField("ISBN")
    texto = models.TextField("Texto")
    imagen = VersatileImageField('Foto', upload_to="autor/", blank=True, null=True)

    traductor = models.CharField("Traductor", max_length=500, blank=True, null=True)
    subtitulo = models.CharField("Sub Titulo", max_length=500, blank=True, null=True)

    class Meta:
        verbose_name_plural = "Libros"
