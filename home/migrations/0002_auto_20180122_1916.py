# Generated by Django 2.0.1 on 2018-01-22 19:16

from django.db import migrations
import versatileimagefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='autor',
            options={'verbose_name_plural': 'Autores'},
        ),
        migrations.AlterModelOptions(
            name='coleccion',
            options={'verbose_name': 'Colección', 'verbose_name_plural': 'Colecciones'},
        ),
        migrations.AlterModelOptions(
            name='libro',
            options={'verbose_name_plural': 'Libros'},
        ),
        migrations.AlterField(
            model_name='autor',
            name='imagen',
            field=versatileimagefield.fields.VersatileImageField(blank=True, null=True, upload_to='imagenes/autor/', verbose_name='Imagen'),
        ),
    ]
