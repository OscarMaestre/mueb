# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-21 18:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mueb', '0003_favorito_preciofavorito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favorito',
            name='id',
        ),
        migrations.AlterField(
            model_name='favorito',
            name='enlace',
            field=models.URLField(primary_key=True, serialize=False),
        ),
    ]
