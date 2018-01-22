from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.html import strip_tags
from home.models import Autor
from django.core.files import File
from django.contrib.auth.models import User

import csv
import os

class Command(BaseCommand):
    help = 'crea los autores'

    def handle(self, *args, **options):
        #raise CommandError('Poll "%s" does not exist' % poll_id)
        #self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))

        user = User.objects.get(pk=1)
        Autor.objects.all().delete()
        with open(os.path.join(settings.BASE_DIR, 'OLD_DB/autores.csv'),'r') as f:
            reader = csv.reader(f, delimiter="|", quotechar='"')
            datos = list(reader)

        for i in datos:
            try:
                nombre= i[1].split(",")[1]
            except: 
                nombre= i[1]

            try:
                imagen = File(open(os.path.join(settings.BASE_DIR, "media/imagenes/autores/", i[3]), 'rb'))
            except FileNotFoundError:
                imagen = None
            a=Autor(nombre=nombre,
                texto=strip_tags(i[2]),
                apellido=i[4],
                imagen=imagen,
                user=user)
            a.id= int(i[0])
            a.save()
