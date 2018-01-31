from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import *
from django.db.models import Count

class HomeView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novedades'] = Libro.objects.all().order_by("-created_at")[:10]
        context['recomendados'] = Libro.objects.filter(recomendado=True).order_by("titulo")
        context['slider'] = Slider.objects.filter(activo=True).order_by("-created_at")
        context['articulos'] = Nota.objects.filter(publicado=True, libro__isnull=False).order_by("-created_at")[0:5]
        context['noticias'] = Nota.objects.filter(publicado=True, libro__isnull=True).order_by("-created_at")[0:5]
        return context

class ColeccionesView(ListView):
    template_name = "libros.html"
    model = Libro
    paginate_by =10
    context_object_name = 'libros'

    def get_queryset(self):
        try:
            self.coleccion = Coleccion.objects.get(slug=self.kwargs['slug'])
            return self.model.objects.select_related().filter(coleccion=self.coleccion)
        except KeyError:
            self.template_name="colecciones.html"
        except Coleccion.DoesNotExist:
            self.template_name="colecciones.html"
    
        self.paginate_by=9999
        return Coleccion.objects.select_related().filter(activa=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['coleccion']=self.coleccion
            autores_ids=sorted(list(self.get_queryset().values("autores").annotate(cantidad=Count('autores')).order_by("autores")),
                     key=lambda k: k['cantidad'], reverse=True)[0:6]
    
            context['autores']=[Autor.objects.get(pk=x['autores']) for x in autores_ids]
            context['autores_len']=len(context['autores'])
        except AttributeError: 
            pass
        return context

class AutoresView(ListView):
    template_name = "autores.html"
    model = Autor

class AutorView(DetailView):
    template_name = "autor.html"
    model = Autor

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        autor = Q(libro__autor=context['object'])
        context['notas'] = Nota.objects.filter(publicado=True).filter(autor)
        return context

class PrensaView(ListView):
    template_name = "prensa.html"
    model = Nota
    context_object_name = 'notas'
    paginate_by =10 
    queryset = Nota.objects.select_related().filter(publicado=True, libro__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destacados'] = self.model.objects.filter(publicado=True, destacado=True)[:10]
        context['noticias'] = self.model.objects.select_related().filter(publicado=True, libro__isnull=True)
        return context

from django.db.models import Q
class NotaView(DetailView):
    template_name = "nota.html"
    model = Nota
    queryset = Nota.objects.filter(publicado=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #libros = Q(libro=context['object'].libro)
        #autor = Q(libro__autor=context['object'].libro.autor)
        #medio = Q(medio=context['object'].medio)
        #notas = self.queryset.filter(libros | autor | medio).exclude(pk=context['object'].id)
        if context['object']:
            notas = self.queryset.filter(libro=context['object'].libro).exclude(pk=context['object'].id)
            context['notas'] = notas[0:5]
        else:
            context['notas'] = []
        return context

class LibrosDestacadosView(ListView):
    template_name = "recomendados.html"
    model = Libro
    queryset = Libro.objects.filter(recomendado=True)
    context_object_name = 'libros'
    paginate_by =10 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "destacados"
        return context


class LibrosView(ListView):
    template_name = "libros.html"
    model = Libro
    queryset = Libro.objects.all()
    context_object_name = 'libros'
    paginate_by =10 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "novedades"
        return context


class LibroView(DetailView):
    template_name = "libro.html"
    model = Libro
    queryset = Libro.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        autores = Q()
        for a in context['object'].autores.all():
            autores.add(Q(autores=a), Q.OR)
        context['recomendados'] = self.get_queryset().filter(autores).exclude(id=context['object'].id)
        context['recomendados'] = context['recomendados'][0:10]

        context['notas'] = Nota.objects.filter(libro=context['object'])[0:10]
        context['xcolecciones']=context['object'].coleccion.all()
 
        return context

class ContactoView(CreateView):
    model = Contacto
    fields = ['nombre', 'email', 'texto']
    template_name = "contacto.html"

    def get_success_url(self):
        return "/contacto/ok/"
