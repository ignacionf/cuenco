from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('autores/', AutoresView.as_view(), name='autores'),
    path('autor/<int:pk>', AutorView.as_view(), name='autor'),
    path('autor/<int:pk>/<str:slug>/', AutorView.as_view(), name='autor'),
    path('en_los_medios/', PrensaView.as_view(), name='prensa'),
    path('noticias/', NoticiasView.as_view(), name='noticias'),
    path('en_los_medios/<int:pk>', NotaView.as_view(), name='nota'),

    path('recomendados/', LibrosDestacadosView.as_view(), name='libros_destacados'),
    path('libros/', LibrosView.as_view(), name='libros'),
    path('libros/en_preparacion/', LibrosPreparacionView.as_view(), name='preparacion'),
    path('libro/<int:pk>', LibroView.as_view(), name='libro'),
    path('libro/<int:pk>/<str:slug>/', LibroView.as_view(), name='libro'),

    path('distribucion/', DistribucionesView.as_view(), name='distribucion'),

    path('colecciones/', ColeccionesView.as_view(), name='colecciones'),
    path('colecciones/<str:slug>/', ColeccionesView.as_view(), name='colecciones'),

    path('la_editorial/', TemplateView.as_view(template_name="editorial.html"), name='editorial'),
    path('librerias/', TemplateView.as_view(template_name="librerias.html"), name='librerias'),
    path('contacto/', ContactoView.as_view(template_name='contacto.html'), name='contacto'),
    path('contacto/ventas/', ContactoView.as_view(template_name='contacto.ventas.html'), name='contacto.ventas'),
    path('contacto/derechos/', ContactoView.as_view(template_name='contacto.derechos.html'), name='contacto.derechos'),
    path('contacto/ok/', TemplateView.as_view(template_name="contacto.ok.html"), name='contacto_ok'),
    path('newsletter/', NewsletterView.as_view(), name='newsletter_add'),

]
