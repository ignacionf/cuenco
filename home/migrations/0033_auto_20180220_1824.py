# Generated by Django 2.0.1 on 2018-02-20 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0032_auto_20180219_1930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newletter',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
    ]
