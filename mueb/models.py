from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Inmueble(models.Model):
    pagina          = models.CharField ( max_length = 30 )
    fecha_inclusion = models.DateField()
    enlace          = models.URLField()
    tipo            = models.CharField( max_length = 20 )
    habitaciones    = models.IntegerField()
    m2              = models.IntegerField()
    otros           = models.CharField( max_length = 30)
    def __str__(self):
        return "Inm"
class Precio ( models.Model ):
    inmueble    = models.ForeignKey ( Inmueble )
    fecha       = models.DateField()
    precio      = models.IntegerField()
    