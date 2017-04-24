#!/usr/bin/env python3
#coding=utf-8


from constantes import *
from datetime import timedelta
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

def generar_objeto_datos(etiqueta, lista_valores, color):
    valores_separados_por_comas=",".join ( lista_valores )
    objeto_datos="{"+OBJETO_DATOS.format ( etiqueta, valores_separados_por_comas, color ) +"}"
    return objeto_datos
    
def get_inmuebles_vendidos( ayer, hoy):
    sql=CONSULTA_VENDIDOS_AYER.format ( ayer, hoy )
    
contexto=dict()

fechas=Precio.objects.values_list("fecha").order_by("fecha").distinct()
v_fechas=[]
for f in fechas:
    
    fecha_a_insertar=f[0].strftime("%d-%m-%Y")
    #print (fecha_a_insertar)
    v_fechas.append ( "'"+fecha_a_insertar+"'" )

hoy=fechas[len(fechas)-1]
ayer=hoy[0]-timedelta(days=1)
lista_fechas=",".join(v_fechas)
#print (fechas[0])
#print (hoy)



FORMATO_MEDIAS="{0:7.0f}"

CONSULTA_PRECIO_MEDIO_POR_TIPO="""
Select tipo, avg(precio)
    from inmuebles, precios
    where inmuebles.codigo_pagina=precios.inmueble_id
        and precios.precio<=350000
        group by tipo order by tipo
"""

CONSULTA_PRECIO_MEDIO_POR_TIPO_Y_FECHA="""
Select fecha, avg(precio)
    from inmuebles, precios
    where inmuebles.codigo_pagina=precios.inmueble_id
        and precios.precio<=350000
        and tipo='{0}' and precio<>0
        group by fecha order by fecha
"""

CONSULTA_CANTIDAD_INMUEBLES_POR_FECHA="""
SELECT fecha, count(precio)
    from precios
    group by fecha
    order by fecha;
"""

CONSULTA_VENDIDOS_AYER="""
select enlace, descr, tipo, habitaciones, m2, otros, p1.precio, pagina, enlace
    from precios as p1, inmuebles
        where fecha="{0}"
            and
                p1.inmueble_id=inmuebles.codigo_pagina
            and
                p1.precio<>0
            and 
                p1.inmueble_id not in
                    (select inmueble_id from precios where fecha="{1}")
"""

pisos=get_objetos(CONSULTA_PRECIO_MEDIO_POR_TIPO)
pisos_por_tipo=[]
for p in pisos:
    valor=FORMATO_MEDIAS.format ( p[1] )
    pisos_por_tipo.append ( [p[0], valor ])
    
contexto["fecha_hoy"]=hoy[0].strftime("%d-%m-%Y")
contexto["fecha_ayer"]=ayer.strftime("%d-%m-%Y")
contexto["precios_medios_por_tipo"]=pisos_por_tipo


objetos_js_graficos=[]
indice_color=0
for t in TIPOS:
    filas=get_objetos ( CONSULTA_PRECIO_MEDIO_POR_TIPO_Y_FECHA.format(t) )
    valores=[]
    for f in filas:
        valores.append( FORMATO_MEDIAS.format (f[1]) )
    #print (valores)
    objeto_js = generar_objeto_datos ( t, valores, COLORES_TIPOS[indice_color] )
    objetos_js_graficos.append ( objeto_js )
    indice_color=indice_color+1
#print (objetos_js_graficos)
tuplas_valores_pisos=",".join( objetos_js_graficos )

inmuebles_por_dia=get_objetos ( CONSULTA_CANTIDAD_INMUEBLES_POR_FECHA )
lista_inmuebles=[]
for i in inmuebles_por_dia:
    lista_inmuebles.append ( str(i[1]) )
objeto_js_cantidad_inmuebles=generar_objeto_datos ( "Cantidad por dia", lista_inmuebles, "(0, 190, 0)" )


vendidos_ayer=get_objetos(CONSULTA_VENDIDOS_AYER.format (ayer.strftime("%Y-%m-%d"),hoy[0].strftime("%Y-%m-%d") ) )
aparecidos_hoy=get_objetos(CONSULTA_VENDIDOS_AYER.format (hoy[0].strftime("%Y-%m-%d"), ayer.strftime("%Y-%m-%d") ) )
contexto["valores_graficos"]=tuplas_valores_pisos
contexto["lista_fechas"]=lista_fechas
contexto["valores_graficos_inmuebles"]=objeto_js_cantidad_inmuebles
contexto["vendidos_ayer"]=vendidos_ayer
contexto["aparecidos_hoy"]=aparecidos_hoy
resultado=render_to_string("mueb/estadisticas.html", contexto)
print (resultado)