# Generated by Django 2.0.1 on 2018-02-07 18:24

from django.db import migrations
import isbn_field.fields
import isbn_field.validators


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0025_distribucion_web'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='distribucion',
            options={'ordering': ['orden', 'nombre', '-created_at'], 'verbose_name': 'Distribución', 'verbose_name_plural': 'Distribuciones'},
        ),
        migrations.AlterField(
            model_name='libro',
            name='isbn',
            field=isbn_field.fields.ISBNField(blank=True, max_length=28, null=True, validators=[isbn_field.validators.ISBNValidator], verbose_name='ISBN'),
        ),
    ]
