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
        return context

class AutoresView(ListView):
    template_name = "autores.html"
    model = Autor

class AutorView(DetailView):
    template_name = "autor.html"
    model = Autor
