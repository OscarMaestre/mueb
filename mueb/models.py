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
    con_garaje      = models.BooleanField()
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
    
class Favorito(models.Model):
    enlace          = models.URLField(primary_key=True)
    habitaciones    = models.IntegerField()
    m2              = models.IntegerField()
    descr           = models.CharField ( max_length=240 )
    def __str__(self):
        return self.enlace
    class Meta:
        db_table="favoritos"
        
class PrecioFavorito(models.Model):
    inmueble    = models.ForeignKey ( Favorito )
    fecha       = models.DateField()
    precio      = models.IntegerField()
    class Meta:
        db_table="preciosfavoritos"