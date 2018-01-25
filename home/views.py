from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from .models import *

class HomeView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novedades'] = Libro.objects.all().order_by("-created_at")[:10]
        context['recomendados'] = Libro.objects.filter(recomendado=True).order_by("titulo")
        context['slider'] = Slider.objects.filter(activo=True).order_by("-created_at")
        context['notas'] = Nota.objects.filter(publicado=True).order_by("-created_at")[0:10]
        return context

class ColeccionesView(ListView):
    template_name = "colecciones.html"
    model = Coleccion

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
    paginate_by =20 
    queryset = Nota.objects.filter(publicado=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destacados'] = self.queryset.filter(destacado=True)[:10]
        return context

from django.db.models import Q
class NotaView(DetailView):
    template_name = "nota.html"
    model = Nota
    queryset = Nota.objects.filter(publicado=True).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        libros = Q(libro=context['object'].libro)
        autor = Q(libro__autor=context['object'].libro.autor)
        medio = Q(medio=context['object'].medio)
        notas = self.queryset.filter(libros | autor | medio).exclude(pk=context['object'].id)
        context['notas'] = notas[0:5]
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
    queryset = Libro.objects.all().order_by("-created_at")
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
        autor = Q(autor=context['object'].autor)
        coleccion = Q(coleccion=context['object'].coleccion)
        context['recomendados'] = Libro.objects.filter(autor | coleccion).exclude(id=context['object'].id)
        context['recomendados'] = context['recomendados'][0:10]

        libros = Q(libro=context['object'])
        autor = Q(libro__autor=context['object'].autor)
        context['notas'] = Nota.objects.filter(libros | autor )[0:10]
 
        return context
