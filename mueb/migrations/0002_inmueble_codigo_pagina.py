# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-05-21 08:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mueb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inmueble',
            name='codigo_pagina',
            field=models.CharField(db_index=True, default='', max_length=40),
            preserve_default=False,
        ),
    ]
