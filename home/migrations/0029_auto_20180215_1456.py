# Generated by Django 2.0.1 on 2018-02-15 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0028_auto_20180214_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='campo1',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Seleccione uno'), (1, 'Traducción de:'), (2, 'Prólogo de:'), (3, 'Edición de:'), (4, 'Compilación de:'), (5, 'Traducción y notas:'), (6, 'Prólogo y traducción de:'), (7, 'Prólogo, traducción y notas de:'), (8, 'Edición y traducción de:'), (9, 'Edición, traducción y prólogo de:'), (10, 'Compilación y traducción de:'), (11, 'Posfacio de:'), (12, 'Ilustraciones de:')], default=0, verbose_name='Campo 1'),
        ),
        migrations.AddField(
            model_name='libro',
            name='campo2',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Seleccione uno'), (1, 'Traducción de:'), (2, 'Prólogo de:'), (3, 'Edición de:'), (4, 'Compilación de:'), (5, 'Traducción y notas:'), (6, 'Prólogo y traducción de:'), (7, 'Prólogo, traducción y notas de:'), (8, 'Edición y traducción de:'), (9, 'Edición, traducción y prólogo de:'), (10, 'Compilación y traducción de:'), (11, 'Posfacio de:'), (12, 'Ilustraciones de:')], default=0, verbose_name='Campo 2'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='prologo',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Contenido Campo 1'),
        ),
        migrations.AlterField(
            model_name='libro',
            name='traductor',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Contenido Campo 2'),
        ),
    ]
