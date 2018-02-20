from django.contrib import admin

from .models import *
from .actions import export_as_csv_action



@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("nombre", "apellido")
    list_filter = ("user",)
    list_display = ("__str__","imagen_html", "created_at", "user")
    readonly_fields = ['imagen_html']
    actions = [export_as_csv_action("CSV Export", fields=["id", "nombre", "apellido", ])]

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Coleccion)
class ColeccionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    date_hierarchy = 'created_at'
    list_display = ("nombre", "slug", "activa", "orden", "created_at", "user")
    actions = [export_as_csv_action("CSV Export", fields=["id", "nombre", "slug", "activa", "orden" ])]
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("titulo", "isbn")#, "autor__nombre", "autor__apellido")
    list_filter = ("recomendado", "disponible", "coleccion", "user",)
    list_display = ("titulo", "imagen_html_sized", "get_autores", "isbn", "recomendado", "disponible", "fecha", "updated_at")
    readonly_fields = ['imagen_html']
    autocomplete_fields = ['autores']
    actions = [export_as_csv_action("CSV Export", fields=["id", "titulo", "prologo",
                "traductor", "subtitulo", "paginas", "formato", "edicion", "carrito",
                "autores", "isbn", "recomendado", "fecha"])]

    fieldsets = (
        (None, {
            "fields": ('titulo', 'autores', 'coleccion', 'isbn', 'texto') 
        }),
        ("Campos opcionales", {
            "fields": ('fecha', 'descripcion', 'subtitulo', 'carrito', 'recomendado', 'disponible') 
        }),
        ("campos variables", {
            "fields": (('campo1', 'prologo'), ('campo2', 'traductor'), ('campo3', 'campo3contenido')) 
        }),
        ("datos del libro", {
            "fields": ('isbn', 'paginas', 'formato', 'edicion') 
        }),
        ("Archivos", {
            "fields": ('imagen', 'pdf',) 
        }),
    )

    def get_autores(self, obj):
        return " ".join([str(a) for a in obj.autores.all()])

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("titulo",)
    list_filter = ("activo",  "user",)
    list_display = ("titulo", "imagen_html_sized", "activo", "created_at", "user")
    readonly_fields = ['imagen_html']
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

import re
@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("titulo","subtitulo", "libro__titulo", "texto")
    list_filter = ("publicado", "destacado", "user",)
    list_display = ("titulo", "medio", "destacado", "publicado", "fecha", "user")
    autocomplete_fields = ['libro']
    actions = [export_as_csv_action("Exportar CSV", fields=["id", "titulo","firma", "medio", "publicado", "destacado", "fecha" ])]

    fieldsets = (
        (None, {
            "fields": ('titulo', 'subtitulo', 'texto',) 
        }),
        ("Campos opcionales", {
            "fields": ('fecha', 'libro', 'fuente', 'firma', 'medio') 
        }),
        ("Metadatos", {
            "fields": ('destacado', 'publicado',) 
        }),
    )


    def save_model(self, request, obj, form, change):
        flags = re.IGNORECASE | re.MULTILINE
        obj.texto = re.sub(r'<div\s*([^>]+)>', '<p>', obj.texto, flags=flags)
        obj.texto = re.sub(r'</div>', '</p>', obj.texto, flags=flags)

        obj.subtitulo = re.sub(r'<div\s*([^>]+)>', '<p>', obj.subtitulo, flags=flags)
        obj.subtitulo = re.sub(r'</div>', '</p>', obj.subtitulo, flags=flags)

        obj.user = request.user
        obj.save()

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("nombre","email", "texto")
    list_filter = ("revisado", "contactado",)
    list_display = ("nombre", "email", "revisado", "contactado", "created_at" )

@admin.register(Distribucion)
class DistribucionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("nombre","pais")
    list_filter = ("publicado",)
    list_display = ("nombre", "email", "direccion", "telefono", "pais" )
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()


@admin.register(Newletter)
class NewsAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("email",)
    list_filter = ("revisado",)
    list_display = ("email", "revisado", "created_at", )

