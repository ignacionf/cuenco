from django.db import models

from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField

from isbn_field import ISBNField

import datetime
import uuid

from django.utils.safestring import mark_safe

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
    imagen = VersatileImageField('Imagen', upload_to="imagenes/autor/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre', 'created_at']

    def __str__(self):
        return "%s %s" % (self.nombre, self.apellido)

    def imagen_html(self, size='90x90'):
        return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.crop[size].url, self))
    imagen_html.short_description = "Thumbnail"


class Coleccion(Model):
    nombre = models.CharField("Nombre", max_length=255)

    class Meta:
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"

    def __str__(self):
        return self.nombre

class Libro(Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    coleccion = models.ForeignKey(Coleccion, on_delete=models.CASCADE)
    titulo = models.CharField("Titulo", max_length=500)
    isbn = ISBNField("ISBN")
    texto = models.TextField("Texto")
    imagen = VersatileImageField('Foto', upload_to="libro/", blank=True, null=True)

    traductor = models.CharField("Traductor", max_length=500, blank=True, null=True)
    subtitulo = models.CharField("Sub Titulo", max_length=500, blank=True, null=True)
    recomendado = models.BooleanField("Recomendado", default=False)

    class Meta:
        verbose_name_plural = "Libros"

    def __str__(self):
        return "%s, %s" % (self.titulo, self.autor)

    def imagen_html_sized(self, size='90x120'):
        return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.thumbnail[size].url, self))
    imagen_html_sized.short_description = "Thumbnail"

    def imagen_html(self):
        return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.url, self))
    imagen_html.short_description = "Muestra de la imagen"

class Slider(Model):
    titulo = models.CharField("Titulo", max_length=500)
    imagen = VersatileImageField('Slider', upload_to="slider/", blank=True, null=True)
    activo = models.BooleanField("Activo", default=False)

    class Meta:
        verbose_name_plural = "Sliders"

    def __str__(self):
        return self.titulo

    def imagen_html_sized(self, size='300x40'):
        return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.thumbnail[size].url, self))
    imagen_html_sized.short_description = "Thumbnail"

    def imagen_html(self):
        return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.url, self))
    imagen_html.short_description = "Muestra de la imagen"


class Nota(Model):
    titulo = models.CharField("Título", max_length=500)
    texto = models.TextField("Texto")

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True, blank=True)
    fuente = models.URLField("Fuente", null=True, blank=True)
    firma = models.CharField("Firma", max_length=500, null=True, blank=True)
    medio = models.CharField("Medio", max_length=500, null=True, blank=True)
    subtitulo = models.CharField("Sub Título", max_length=500, null=True, blank=True)

    publicado = models.BooleanField("Publicado", default=True)

    class Meta:
        verbose_name_plural = "Notas"

    def __str__(self):
        return self.titulo
