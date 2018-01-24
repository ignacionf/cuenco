from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('autores/', AutoresView.as_view(), name='autores'),
    path('prensa/', PrensaView.as_view(), name='prensa'),
    path('prensa/<int:pk>', NotaView.as_view(), name='nota'),
    path('autor/<int:pk>', AutorView.as_view(), name='autor'),
]
