from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from .models import *
from django.db.models import Count
import requests
from django.contrib import messages
from django.conf import settings
from django.forms.utils import ErrorList
from django import forms
from django.core.mail import send_mail
from datetime import date
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = "home.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['novedades'] = Libro.objects.filter(fecha__lte=date.today()).order_by("-fecha")[:10]
        context['recomendados'] = Libro.objects.filter(recomendado=True).order_by("titulo")
        context['slider'] = Slider.objects.filter(activo=True).order_by("-created_at")
        context['articulos'] = Nota.objects.filter(publicado=True, libro__isnull=False).order_by("-fecha")[0:5]
        context['noticias'] = Nota.objects.filter(publicado=True, libro__isnull=True).order_by("-fecha")[0:5]
        return context

class DistribucionesView(ListView):
    template_name = "distribucion.html"
    model = Distribucion


class ColeccionesView(ListView):
    template_name = "libros.html"
    model = Libro
    paginate_by =10
    context_object_name = 'libros'

    def get_queryset(self):
        try:
            self.coleccion = Coleccion.objects.get(slug=self.kwargs['slug'])
            return self.model.objects.select_related().filter(coleccion=self.coleccion, fecha__lte=date.today())
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
            context['autores']=self.coleccion.autores.all()[0:6]
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
        autor = Q(libro__autores=context['object'])
        context['notas'] = Nota.objects.filter(publicado=True).filter(autor)
        return context

class PrensaView(ListView):
    template_name = "prensa.html"
    model = Nota
    context_object_name = 'notas'
    paginate_by =20 
    queryset = Nota.objects.select_related().filter(publicado=True).exclude(libros=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['div']=11
        context['destacados'] = self.model.objects.filter(publicado=True, destacado=True)[:10]
        #context['noticias'] = self.model.objects.select_related().filter(publicado=True, libro__isnull=True)
        return context

class NoticiasView(ListView):
    template_name = "prensa.html"
    model = Nota
    context_object_name = 'notas'
    paginate_by =20 
    queryset = Nota.objects.select_related().filter(publicado=True, libros=None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['div']=11
        if len(context['paginator'].object_list) < 20:
            context['div']=(len(context['paginator'].object_list)/2)+1
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
    paginate_by = 8
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "destacados"
        return context

class LibrosPreparacionView(ListView):
    template_name = "libros.html"
    model = Libro
    queryset = Libro.objects.filter(fecha__gte=date.today()).order_by("fecha")
    context_object_name = 'libros'
    paginate_by =10 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nombre'] = "preparacion"
        return context



class LibrosView(ListView):
    template_name = "libros.html"
    model = Libro
    queryset = Libro.objects.filter(fecha__lte=date.today())
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
        context['recomendados'] = self.get_queryset().filter(autores,fecha__lte=date.today()).exclude(id=context['object'].id)
        context['recomendados'] = context['recomendados'][0:10]

        context['notas'] = Nota.objects.filter(libro=context['object'])[0:10]
        context['xcolecciones']=context['object'].coleccion.all()
 
        return context

class ContactoView(CreateView):
    model = Contacto
    fields = ['nombre', 'email', 'texto']
#    template_name = "contacto.html"

    def form_valid(self, form):
        recaptcha_response = self.request.POST.get('g-recaptcha-response', 0)
        tipo = int(self.request.POST.get('tipo', None))
        data = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if tipo == 1:
            email = "web@elcuencodeplata.com"
        elif tipo == 2:
            email = "ventas@elcuencodeplata.com"
        elif tipo == 3:
            email = "elizabeth@elcuencodeplata.com"
        else:
            form._errors["recaptcha"] = ErrorList([ 'Error de Tipo' ])
            return self.form_invalid(form)

        send_mail("Contacto desde la Web de %s" % form.cleaned_data['nombre'],
            "Email: %s\n\nTexto:\n%s" % (form.cleaned_data['email'],form.cleaned_data['texto'],),
            'no-reply@elcuencodeplata.com',
            [email,],
            fail_silently=True)

        if result['success']:
            return super().form_valid(form)

        form._errors["recaptcha"] = ErrorList([ 'Debe completar reCAPTCHA ' ])
        return self.form_invalid(form)

    def get_success_url(self):
        return "/contacto/ok/"

class AjaxableResponseMixin:
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.is_ajax():
            data = {
                'status': 200,
            }
            return JsonResponse(data)
        else:
            return response

class NewsletterView(AjaxableResponseMixin, CreateView):
    model = Newletter
    fields = ['email',]

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return "/contacto/ok/"
