from .models import Coleccion, Autor, Libro
from django.core.cache import cache

def colecciones(request):
    return {
        'colecciones': Coleccion.objects.filter(orden__lt=9).order_by("orden")
    }

def keywords(request):

    keywords = cache.get("el_cuenco_keywords")
    if not keywords:
        print("-----------------------------------------")
        keywords = ", ".join([str(x) for x in Autor.objects.all().order_by("apellido")])
        keywords = keywords + ", ".join([str(x) for x in Libro.objects.all().order_by("titulo")])
        cache.set("el_cuenco_keywords", keywords, 6000)

    return {
        'keywords': keywords
    }
