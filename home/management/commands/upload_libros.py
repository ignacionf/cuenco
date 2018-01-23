from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.html import strip_tags
from home.models import *
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
        Libro.objects.all().delete()
        with open(os.path.join(settings.BASE_DIR, 'OLD_DB/libros.csv'),'r') as f:
            reader = csv.reader(f, delimiter="|", quotechar='"')
            datos = list(reader)

        for i in datos:
            try:
                imagen = File(open(os.path.join(settings.BASE_DIR, "media/imagenes/libros/", i[6]), 'rb'))
            except FileNotFoundError:
                imagen = None

            autor = Autor.objects.get(pk=int(i[1]))
            coleccion = Coleccion.objects.get(pk=int(i[9]))
            traductor = i[4] if i[4] != 'NULL' else None
            subtitulo = i[8] if i[8] != 'NULL' else None
            a=Libro(autor=autor,
                coleccion=coleccion,
                texto=strip_tags(i[5]),
                titulo=i[7],
                isbn=i[2],
                traductor=traductor,
                subtitulo=subtitulo,
                imagen=imagen,
                user=user)
            a.id = int(i[0])
            a.save()

            a.imagen="imagenes/libros/%s" % i[6]
            a.save()
