from .models import Coleccion

def colecciones(request):
    return {
        'colecciones': Coleccion.objects.filter(activa=True, orden__lt=90).order_by("orden")
    }
