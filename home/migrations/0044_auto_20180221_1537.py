# Generated by Django 2.0.1 on 2018-02-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0043_auto_20180221_1534'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notarelacion',
            name='titulo',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Título Alternativo, sino usa el de la nota'),
        ),
    ]
