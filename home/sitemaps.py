from django.contrib.sitemaps import Sitemap
from .models import *

class AutorSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Autor.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class LibroSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Libro.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class ColeccionSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Coleccion.objects.all()

    def lastmod(self, obj):
        return obj.created_at

class NotaSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Nota.objects.filter(publicado=True)

    def lastmod(self, obj):
        return obj.created_at
