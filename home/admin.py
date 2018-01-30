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
    search_fields = ("titulo", "isbn", "autor__nombre", "autor__apellido")
    list_filter = ("recomendado",  "coleccion", "user","autor",)
    list_display = ("titulo", "imagen_html_sized", "autor", "isbn", "recomendado", "fecha")
    readonly_fields = ['imagen_html']
    autocomplete_fields = ['autor']
    actions = [export_as_csv_action("CSV Export", fields=["id", "titulo", "prologo",
                "traductor", "subtitulo", "paginas", "formato", "edicion", "carrito",
                "autor", "isbn", "recomendado", "fecha"])]

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

@admin.register(Nota)
class NotaAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("titulo","subtitulo", "libro", "texto")
    list_filter = ("publicado", "destacado", "user",)
    list_display = ("titulo", "medio", "destacado", "publicado", "fecha", "user")
    autocomplete_fields = ['libro']
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("nombre","email", "texto")
    list_filter = ("revisado", "contactado",)
    list_display = ("nombre", "email", "revisado", "contactado", "created_at" )
