# Generated by Django 2.0.1 on 2018-01-25 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_auto_20180125_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='coleccion',
            name='activa',
            field=models.BooleanField(default=True, verbose_name='Activa'),
        ),
    ]
