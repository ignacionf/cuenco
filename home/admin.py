from django.contrib import admin

from .models import *


@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("nombre", "apellido")
    list_filter = ("user",)
    list_display = ("__str__","imagen_html", "created_at", "user")
    readonly_fields = ['imagen_html']

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Coleccion)
class ColeccionAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("nombre",)}
    date_hierarchy = 'created_at'
    list_display = ("nombre", "slug", "activa", "orden", "created_at", "user")
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_fields = ("titulo", "isbn", "autor__nombre", "autor__apellido")
    list_filter = ("recomendado",  "coleccion", "user","autor",)
    list_display = ("titulo", "imagen_html_sized", "autor", "coleccion", "isbn", "recomendado", "created_at")
    readonly_fields = ['imagen_html']
    autocomplete_fields = ['autor']
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
    list_display = ("titulo", "medio", "destacado", "publicado", "created_at", "user")
    autocomplete_fields = ['libro']
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
