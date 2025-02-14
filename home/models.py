from django.db import models
from django.utils.text import slugify

from django.contrib.auth.models import User
from versatileimagefield.fields import VersatileImageField
from tinymce import models as tinymce_models
from django.urls import reverse 
from taggit.managers import TaggableManager

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
        ordering = ['-created_at',]

class Autor(Model):
    nombre = models.CharField("Nombre", max_length=255, blank=True, null=True)
    apellido = models.CharField("Apellido", max_length=255)
    texto = tinymce_models.HTMLField("Texto")
    imagen = VersatileImageField('Imagen', upload_to="imagenes/autor/", blank=True, null=True)

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name_plural = "Autores"
        ordering = ['apellido', 'nombre', 'created_at']

    def __str__(self):
        if self.nombre:
            return "%s %s" % (self.nombre, self.apellido)
        return self.apellido

    def get_absolute_url(self):
        return reverse("autor", args=[self.id, slugify(str(self))])

    @property
    def libros(self):
        return self.autores_de_libros.filter(fecha__lte=datetime.date.today())

    def imagen_html(self, size='90x90'):
        try:
            return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.crop[size].url, self))
        except:
            pass
        return ""
    imagen_html.short_description = "Thumbnail"


class Coleccion(Model):
    nombre = models.CharField("Nombre", max_length=255)
    texto = tinymce_models.HTMLField("Texto", blank=True, null=True)
    slug = models.SlugField("Slug (uso en la web)", max_length=255, blank=True, null=True)
    activa = models.BooleanField("Activa", default=True)
    orden = models.PositiveSmallIntegerField("Orden", default=99)
    imagen = VersatileImageField('Imagen', upload_to="imagenes/coleccion/", blank=True, null=True)

    autores = models.ManyToManyField(Autor, related_name="coleccion_autores")

    class Meta:
        verbose_name = "Colección"
        verbose_name_plural = "Colecciones"
        ordering = ['orden',"activa"]

    def __str__(self):
        return self.nombre

    def get_10_libros(self):
        return self.libro_set.all()[0:10]

    def get_absolute_url(self):
        return reverse("colecciones", args=[self.slug])


FORMATOS = (
    ("15,5x23", "155mm*230mm"),
    ("14x21", "140mm*210mm"),
    ("13x21", "130mm*210mm"),
    ("12x21", "120mm*210mm"),
    ("11,8x18", "118mm*180mm"),
    )

EDICIONES = ((x, "%s°" %x) for x in range(1,51)) 

from random import randint
def libro_filename(instance, filename):
    ext = filename.split(".")[-1]
    if instance.isbn:
        name=instance.isbn
    else:
        name=slugify(instance.titulo)

    return 'libros/{0}/{1}/{2}.{3}'.format(instance.id, randint(1000, 9999), name, ext)

CAMPOS = (
    (0,'Seleccione uno'),
    (1,'Traducción de:'),
    (2,'Prólogo de:'),
    (3,'Edición de:'),
    (4,'Compilación de:'),
    (5,'Traducción y notas:'),
    (6,'Prólogo y traducción de:'),
    (7,'Prólogo, traducción y notas de:'),
    (8,'Edición y traducción de:'),
    (9,'Edición, traducción y prólogo de:'),
    (10,'Compilación y traducción de:'),
    (11,'Posfacio de:'),
    (12,'Ilustraciones de:'),
)

class Libro(Model):
    autores = models.ManyToManyField(Autor, related_name="autores_de_libros")
    coleccion = models.ManyToManyField(Coleccion)
    titulo = models.CharField("Titulo", max_length=500)
    isbn = ISBNField("ISBN", blank=True, null=True)
    texto = tinymce_models.HTMLField("Texto")
    indice = tinymce_models.HTMLField("Indice", blank=True, null=True)

    imagen = VersatileImageField('Foto', upload_to=libro_filename, blank=True, null=True)
    fecha = models.DateField("Fecha publicación", null=True, blank=True)

    campo1 = models.PositiveSmallIntegerField("Campo 1", default=2, choices=CAMPOS)
    prologo = models.CharField("Contenido Campo 1", max_length=500, blank=True, null=True)
    campo2 = models.PositiveSmallIntegerField("Campo 2", default=1, choices=CAMPOS)
    traductor = models.CharField("Contenido Campo 2", max_length=500, blank=True, null=True)
    campo3 = models.PositiveSmallIntegerField("Campo 3", default=1, choices=CAMPOS)
    campo3contenido = models.CharField("Contenido Campo 3", max_length=500, blank=True, null=True)

    descripcion = models.CharField("Descripción (250 chars)", max_length=250, blank=True, null=True)
    subtitulo = models.CharField("Sub Titulo", max_length=500, blank=True, null=True)
    recomendado = models.BooleanField("Recomendado", default=False)
    disponible = models.BooleanField("Disponible", default=True)

    paginas = models.PositiveIntegerField("Páginas", blank=True, null=True)
    formato = models.CharField("Formato", max_length=20, choices=FORMATOS, blank=True, null=True)
    edicion = models.PositiveSmallIntegerField("Edición", choices=EDICIONES, blank=True, null=True)
    carrito = models.URLField("URL Carrito de compras", null=True, blank=True)
    pdf = models.FileField("PDF", upload_to='uploads/pdf/', null=True, blank=True)

    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name_plural = "Libros"
        ordering = ['-fecha','-id',]

    def get_absolute_url(self):
        return reverse("libro", args=[self.id, slugify(self.titulo)])

    def get_autores(self):
        return " ".join([str(a) for a in self.autores.all()])

    def get_colecciones(self):
        return " ".join([str(a) for a in self.coleccion.all()])

    def __str__(self):
        return self.titulo

    @property
    def fISBN(self):
        i = self.isbn
        try:
            if len(i) > 10:
                return "%s-%s-%s-%s-%s" %(i[0:3], i[3:6],i[6:10], i[10:12],i[12])
            else:
                return "%s-%s-%s-%s" %(i[0], i[1:3],i[3:9],i[9])
        except (IndexError, TypeError):
            return i

    def imagen_html_sized(self, size='90x120'):
        try:
            return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.thumbnail[size].url, self))
        except:
            pass
        return ""
    imagen_html_sized.short_description = "Thumbnail"

    def imagen_html(self):
        try:
            return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.url, self))
        except:
            pass
        return ""
    imagen_html.short_description = "Muestra de la imagen"

class Slider(Model):
    titulo = models.CharField("Titulo", max_length=500)
    imagen = VersatileImageField('Slider', upload_to="slider/", blank=True, null=True)
    activo = models.BooleanField("Activo", default=False)
    destino = models.URLField("URL Destino", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Sliders"

    def __str__(self):
        return self.titulo

    def imagen_html_sized(self, size='300x40'):
        try:
            return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.thumbnail[size].url, self))
        except:
            pass
        return ""
    imagen_html_sized.short_description = "Thumbnail"

    def imagen_html(self):
        try:
            return mark_safe("<img src='%s' alt='%s' />" % (self.imagen.url, self))
        except:
            pass
        return ""
    imagen_html.short_description = "Muestra de la imagen"


class Nota(Model):
    titulo = models.CharField("Título", max_length=500)
    texto = tinymce_models.HTMLField("Texto")

    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, null=True, blank=True)
    libros = models.ManyToManyField(Libro, blank=True, related_name="libros_nota")
    autores = models.ManyToManyField(Autor, blank=True)
    tags = TaggableManager(blank=True)

    fuente = models.URLField("Fuente", null=True, blank=True)
    firma = models.CharField("Firma", max_length=500, null=True, blank=True)
    medio = models.CharField("Medio", max_length=500, null=True, blank=True)
    subtitulo= tinymce_models.HTMLField("Volanta", null=True, blank=True)

    destacado = models.BooleanField("Destacado", default=False)
    publicado = models.BooleanField("Publicado", default=True)

    fecha = models.DateField("Fecha publicación", null=True, blank=True)

    class Meta:
        verbose_name_plural = "Notas"
        ordering = ['-fecha','-created_at',]

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("nota", args=[self.id])

    def get_libros(self):
        return " | ".join([str(x) for x in self.libros.all()])

    def get_notas_relacionadas(self):
        return [{'titulo': x.titulo, 'nota': x.nota1.all().first()} for x in self.notarelacion_set.all()]

    def get_notas_relacionadas_urls(self):
        return [x for x in self.notaurlrelacion_set.all()]

class NotaRelacion(models.Model):
    titulo = models.CharField("Título Alternativo, sino usa el de la nota", max_length=500, null=True, blank=True)
    nota1 = models.ManyToManyField(Nota, related_name="nota_relacionada")
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)

class NotaURLRelacion(models.Model):
    titulo = models.CharField("Título", max_length=500)
    medio = models.CharField("Medio y/o Autor", max_length=500, null=True, blank=True)
    url = models.URLField("URL")
    nota = models.ForeignKey(Nota, on_delete=models.CASCADE)

class Newletter(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    email = models.EmailField("Email", unique=True)
    revisado = models.BooleanField("Revisado", default=False)

class Contacto(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    nombre = models.CharField("Nombre y Apellido", max_length=500)
    texto = tinymce_models.HTMLField("Texto")

    email = models.EmailField("Email")

    revisado = models.BooleanField("Revisado", default=False)
    contactado = models.BooleanField("Contactado", default=False)
    fecha = models.DateField("Fecha Contacto", null=True, blank=True)

    def __str__(self):
        return self.email

class Distribucion(Model):
    nombre = models.CharField("Nombre", max_length=200)

    pais = models.CharField("País", max_length=50, null=True, blank=True)
    direccion = models.CharField("Dirección", max_length=500, null=True, blank=True)
    telefono = models.CharField("Teléfono", max_length=100, null=True, blank=True)
    web = models.CharField("Página web", max_length=200, null=True, blank=True)
    email = models.EmailField("E-Mail", null=True, blank=True)

    aclaracion = models.CharField("Aclaración", max_length=200, null=True, blank=True)

    publicado = models.BooleanField("Publicado", default=True)
    orden = models.PositiveSmallIntegerField("Orden", default=99)

    class Meta:
        verbose_name_plural = "Distribuciones"
        verbose_name = "Distribución"
        ordering = ['orden','nombre', '-created_at',]

    def get_email_display(self):
        return self.email.replace("@"," [at] ")

    def __str__(self):
        return self.nombre


