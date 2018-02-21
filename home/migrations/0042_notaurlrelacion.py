# Generated by Django 2.0.1 on 2018-02-21 15:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0041_auto_20180221_1532'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotaURLRelacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=500, verbose_name='Título Alternativo, sino usa el de la nota')),
                ('url', models.URLField(verbose_name='URL')),
                ('nota', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.Nota')),
            ],
        ),
    ]
