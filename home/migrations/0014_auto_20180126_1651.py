# Generated by Django 2.0.1 on 2018-01-26 16:51

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20180126_1644'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coleccion',
            name='texto',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='texto',
            field=tinymce.models.HTMLField(verbose_name='Texto'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='subtitulo',
            field=tinymce.models.HTMLField(blank=True, null=True, verbose_name='Subtitulo'),
        ),
        migrations.AlterField(
            model_name='nota',
            name='texto',
            field=tinymce.models.HTMLField(verbose_name='Texto'),
        ),
    ]
