# Generated by Django 2.0.1 on 2018-02-21 15:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0040_notarelacion_notaurlrelacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notaurlrelacion',
            name='user',
        ),
        migrations.AlterModelOptions(
            name='notarelacion',
            options={},
        ),
        migrations.RemoveField(
            model_name='notarelacion',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='notarelacion',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='notarelacion',
            name='user',
        ),
        migrations.DeleteModel(
            name='NotaURLRelacion',
        ),
    ]
