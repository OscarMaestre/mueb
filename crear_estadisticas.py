#!/usr/bin/env python3
#coding=utf-8


from constantes import *
from utilidades.basedatos.Configurador import Configurador
configurador=Configurador("mu")
configurador.activar_configuracion("mu.settings")

from mueb.models import *
from django.db import connection
from django.template.loader import render_to_string


def get_objetos(consulta_sql):
    cursor = connection.cursor()
    cursor.execute(consulta_sql)
    filas = cursor.fetchall()
    return (filas)

def generar_objeto_datos(etiqueta, lista_valores):
    valores_separados_por_comas=",".join ( lista_valores )
    objeto_datos="{"+OBJETO_DATOS.format ( etiqueta, valores_separados_por_comas ) +"}"
    return objeto_datos
    
contexto=dict()

fechas=Precio.objects.values_list("fecha").order_by("fecha").distinct()

hoy=fechas[len(fechas)-1]

#print (fechas[0])
#print (hoy)


FORMATO_MEDIAS="{0:7.0f}"

CONSULTA_PRECIO_MEDIO_POR_TIPO="""
Select tipo, avg(precio)
    from inmuebles, precios
    where inmuebles.codigo_pagina=precios.inmueble_id
        group by tipo order by tipo
"""

CONSULTA_PRECIO_MEDIO_POR_TIPO_Y_FECHA="""
Select fecha, avg(precio)
    from inmuebles, precios
    where inmuebles.codigo_pagina=precios.inmueble_id
        and tipo='{0}'
        group by fecha order by fecha
"""

pisos=get_objetos(CONSULTA_PRECIO_MEDIO_POR_TIPO)
pisos_por_tipo=[]
for p in pisos:
    valor=FORMATO_MEDIAS.format ( p[1] )
    pisos_por_tipo.append ( [p[0], valor ])
    
contexto["fecha_hoy"]=hoy[0].strftime("%d-%m-%Y")
contexto["precios_medios_por_tipo"]=pisos_por_tipo


objetos_js_graficos=[]
for t in TIPOS:
    filas=get_objetos ( CONSULTA_PRECIO_MEDIO_POR_TIPO_Y_FECHA.format(t) )
    valores=[]
    for f in filas:
        valores.append( FORMATO_MEDIAS.format (f[1]) )
    #print (valores)
    objeto_js = generar_objeto_datos ( t, valores )
    objetos_js_graficos.append ( objeto_js )
#print (objetos_js_graficos)
tuplas_valores_pisos=",".join( objetos_js_graficos )

contexto["valores_graficos"]=tuplas_valores_pisos
resultado=render_to_string("mueb/estadisticas.html", contexto)
print (resultado)