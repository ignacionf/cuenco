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

class PrensaView(ListView):
    template_name = "prensa.html"
    model = Nota

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['destacados'] = self.model.objects.filter(destacado=True).order_by("-created_at")[:10]
        return context

class NotaView(DetailView):
    template_name = "nota.html"
    model = Nota


