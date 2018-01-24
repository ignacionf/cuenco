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

