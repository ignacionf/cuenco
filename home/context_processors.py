from .models import Coleccion

def colecciones(request):
    return {
        'colecciones': Coleccion.objects.filter(orden__lt=9).order_by("orden")
    }
