# Generated by Django 2.0.1 on 2018-01-29 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_auto_20180126_1651'),
    ]

    operations = [
        migrations.AddField(
            model_name='slider',
            name='destino',
            field=models.URLField(blank=True, null=True, verbose_name='URL Destino'),
        ),
        migrations.AlterField(
            model_name='autor',
            name='nombre',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre'),
        ),
    ]
