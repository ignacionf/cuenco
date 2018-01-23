from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.html import strip_tags
from home.models import Coleccion
from django.contrib.auth.models import User

import csv
import os

class Command(BaseCommand):
    help = 'crea los colecciones'

    def handle(self, *args, **options):

        user = User.objects.get(pk=1)
        Coleccion.objects.all().delete()
        with open(os.path.join(settings.BASE_DIR, 'OLD_DB/colecciones.csv'),'r') as f:
            reader = csv.reader(f, delimiter="|", quotechar='"')
            datos = list(reader)

        for i in datos:
            c=Coleccion(nombre=i[1], user=user)
            c.id = int(i[0])
            c.save()
