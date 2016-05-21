from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Inmueble(models.Model):
    pagina          = models.CharField ( max_length = 30 )
    fecha_inclusion = models.DateField()
    enlace          = models.URLField()
    descr           = models.CharField ( max_length=240 )
    codigo_pagina   = models.CharField( max_length=40, db_index=True, primary_key=True)
    tipo            = models.CharField( max_length = 20 )
    habitaciones    = models.IntegerField()
    m2              = models.IntegerField()
    otros           = models.CharField( max_length = 30)
    class Meta:
        db_table="inmuebles"
    def __str__(self):
        return "Inm"
class Precio ( models.Model ):
    inmueble    = models.ForeignKey ( Inmueble )
    fecha       = models.DateField()
    precio      = models.IntegerField()
    class Meta:
        db_table="precios"
    