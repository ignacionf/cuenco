# Generated by Django 2.0.1 on 2018-02-09 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0026_auto_20180207_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='coleccion',
            name='autores',
            field=models.ManyToManyField(related_name='coleccion_autores', to='home.Autor'),
        ),
    ]
