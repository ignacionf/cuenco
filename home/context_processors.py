from .models import Coleccion

def colecciones(request):
    return {
        'colecciones': Coleccion.objects.filter(activa=True).order_by("nombre")
    }
