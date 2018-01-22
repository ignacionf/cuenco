from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('autores/', AutoresView.as_view(), name='autores'),
    path('autor/<int:pk>', AutorView.as_view(), name='autor'),
]
