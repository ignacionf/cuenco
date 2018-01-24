from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.html import strip_tags
from home.models import *
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime
from django.utils.safestring import mark_safe
from django.utils.timezone import make_aware
from django.utils.html import strip_tags

import csv
import os
import re

class Command(BaseCommand):
    help = 'crea las notas'

    def removetag(self, value):
        flags = re.IGNORECASE | re.MULTILINE
#        html = re.sub(r'<font\s*([^>]+)>', '', value, flags=flags)
#        html = re.sub(r'<\/font>', '', html, flags=flags)
        html = re.sub(r'<br>', "\n", value, flags=flags)
        html = re.sub(r'\\', '', html, flags=flags)
        return mark_safe(strip_tags(html))
        

    def handle(self, *args, **options):

        user = User.objects.get(pk=1)
        Nota.objects.all().delete()

        with open(os.path.join(settings.BASE_DIR, 'OLD_DB/notas.csv'),'r') as f:
            reader = csv.reader(f, delimiter="|", quotechar='"')
            datos = list(reader)

        for i in datos:
            o = {'id': int(i[0]),
                'medio': i[1],
                'fecha': make_aware(parse_datetime(i[2])),
                'titulo': self.removetag(i[3]),
                'subtitulo': self.removetag(i[4]) if i[4] != "NULL" else None,
                'texto': self.removetag(i[5]),
                'firma': i[6] if i[6] != "NULL" else None,
                'fuente': i[7] if i[7] != "NULL" else None,
                'libro': Libro.objects.get(pk=int(i[8])) if i[8] != "NULL" else None,
                }

            print(o['id'])
            n=Nota(medio=o['medio'],
                titulo=o['titulo'],
                subtitulo=o['subtitulo'],
                texto=o['texto'],
                firma=o['firma'],
                fuente=o['fuente'],
                libro=o['libro'], user=user)
            n.id=o['id']
            n.save()
            n.created_at=o['fecha']
            n.save()
