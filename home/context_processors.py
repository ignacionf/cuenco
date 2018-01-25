from .models import Coleccion

def colecciones(request):
    return {
        'colecciones': Coleccion.objects.all().order_by("nombre")
    }
