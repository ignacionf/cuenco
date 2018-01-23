from django.contrib import admin

from .models import *

@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_display = ("nombre", "apellido")
    list_filter = ("user",)
    list_display = ("id","nombre", "apellido", "imagen", "created_at", "user")

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Coleccion)
class ColeccionAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ("nombre", "created_at", "user")
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    search_display = ("nombre", "titulo", "isbn")
    list_filter = ("recomendado",  "coleccion", "user","autor",)
    list_display = ("titulo", "autor", "coleccion", "subtitulo", "isbn", "recomendado", "created_at", "user")
    def save_model(self, request, obj, form, change):
        obj.user = request.user
        obj.save()
