# Generated by Django 2.0.1 on 2018-01-29 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20180129_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha publicación'),
        ),
        migrations.AddField(
            model_name='nota',
            name='fecha',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha publicación'),
        ),
    ]
