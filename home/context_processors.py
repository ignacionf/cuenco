from .models import Coleccion, Autor, Libro
from django.core.cache import cache

from django.conf import settings

def colecciones(request):
    return {
        'colecciones': Coleccion.objects.filter(orden__lt=9).order_by("orden"),
        "DEBUG": settings.DEBUG,
    }

def keywords(request):

    keywords = cache.get("el_cuenco_keywords")
    if not keywords:
        keywords = ", ".join([str(x.apellido) for x in Autor.objects.all().order_by("apellido")])
        keywords = keywords + ", ".join([str(x) for x in Libro.objects.all().order_by("titulo")])
        cache.set("el_cuenco_keywords", keywords, 6000)

    return {
        'keywords': keywords
    }
