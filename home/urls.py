from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('autores/', AutoresView.as_view(), name='autores'),
    path('autor/<int:pk>', AutorView.as_view(), name='autor'),
    path('prensa/', PrensaView.as_view(), name='prensa'),
    path('noticias/', NoticiasView.as_view(), name='noticias'),
    path('prensa/<int:pk>', NotaView.as_view(), name='nota'),

    path('destacados/', LibrosDestacadosView.as_view(), name='libros_destacados'),
    path('libros/', LibrosView.as_view(), name='libros'),
    path('libro/<int:pk>', LibroView.as_view(), name='libro'),

    path('colecciones/', ColeccionesView.as_view(), name='colecciones'),
    path('colecciones/<str:slug>/', ColeccionesView.as_view(), name='colecciones'),

    path('la_editorial/', TemplateView.as_view(template_name="editorial.html"), name='editorial'),
    path('contacto/', ContactoView.as_view(), name='contacto'),
    path('contacto/ok/', TemplateView.as_view(template_name="contacto.ok.html"), name='contacto_ok'),

]
