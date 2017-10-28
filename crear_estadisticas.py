#!/usr/bin/env python3
#coding=utf-8


from constantes import *
from datetime import timedelta
configurador=Configurador("mu")
configurador.activar_configuracion("mu.settings")
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import sqlite3
from math import sqrt
from mueb.models import *
from django.db import connection
from django.template.loader import render_to_string
from django.db.transaction import atomic
from procesar_favoritos import *

script="""
<script type="text/javascript">
        var datos = {{
            labels: [{0}],
            datasets: [
                {{
                    label: "Valores",
                    fill: false,
                    lineTension: 0,
                    backgroundColor: "rgba(142, 11, 11, 1)",
                    borderColor: "rgba(142, 11, 11, 1)",
                    borderCapStyle: "butt",
                    borderDash: [],
                    borderDashOffset: 0.0,
                    borderJoinStyle: "miter",
                    pointBorderColor: "rgba(75,192,192,1)",
                    pointBackgroundColor: "#fff",
                    pointBorderWidth: 1,
                    pointHoverRadius: 5,
                    pointHoverBackgroundColor: "rgba(75,192,192,1)",
                    pointHoverBorderColor: "rgba(220,220,220,1)",
                    pointHoverBorderWidth: 2,
                    pointRadius: 10,
                    pointHitRadius: 20,
                
                    data:[{1}]    
                }}
            ]
            
        }};
        
        ctx=document.getElementById('{2}')
        var myLineChart = new Chart(ctx, {{
            type: 'line',
            data: datos
        }});
        
    </script>
"""

canvas='<canvas id="{0}" width="800" height="400"></canvas>'


def calcular_desviacion_por_tipo(tipo, media):
    CONSULTA="""
        select precio from precios, inmuebles
            where precios.inmueble_id=inmuebles.codigo_pagina
            and precio<=350000 and
            tipo='{0}'
    """
    vector_enteros=get_vector_enteros(CONSULTA.format(tipo))
    suma_desviaciones=0
    for precio in vector_enteros:
        desviacion=precio-int(media)
        desviacion_cuadrado=desviacion * desviacion
        suma_desviaciones+= desviacion_cuadrado
        #print(precio, media, desviacion, desviacion_cuadrado)
    desviacion_media=sqrt(suma_desviaciones/(len(vector_enteros)-1))
    #print("Desviacion media:"+str(desviacion_media))
    return desviacion_media

def copy_database(source_connection, dest_dbname=':memory:'):
    '''Return a connection to a new copy of an existing database.                        
       Raises an sqlite3.OperationalError if the destination already exists.             
    '''
    script = ''.join(source_connection.iterdump())
    dest_conn = sqlite3.connect(dest_dbname)
    dest_conn.executescript(script)
    return dest_conn

def generar_grafico(nombre_archivo, fechas_etiquetas, precios_inmueblesdatos):
    etiquetas=range(len(precios_inmueblesdatos))
    plt.plot( etiquetas, precios_inmueblesdatos)
    plt.savefig(nombre_archivo)
    plt.clf()

def get_estadistica_por_inmueble(conexion_memoria=None):
    sql_codigos_inmuebles="select codigo_pagina, pagina, descr, tipo, habitaciones, m2, otros, con_garaje, fecha_inclusion, rowid from inmuebles"
    sql_precios_del_inmueble="select precio from precios where inmueble_id={0} order by fecha asc"
    sql_fechas_precios_del_inmueble="select fecha from precios where inmueble_id={0} order by fecha asc"
    lista_inmuebles=[]
    filas=get_objetos(sql_codigos_inmuebles)
    for f in filas:
        #print(f)
        codigo_pagina   =f[0]
        pagina          =f[1]
        descr           =f[2]
        habitaciones    =f[4]
        m2              =f[5]
        con_garaje      =f[6]
        #nombre_archivo  =SUBDIRECTORIO_RESULTADOS + os.sep + str(f[9])+".png"
        fechas          =get_vector_objetos(sql_fechas_precios_del_inmueble.format(codigo_pagina))
        precios         =get_vector_enteros( sql_precios_del_inmueble.format ( codigo_pagina ) )
        
        lista_fechas    =generar_serie_datos(fechas, con_comillas=True)
        lista_precios   =generar_serie_datos(precios, con_comillas=True)
        #generar_grafico (nombre_archivo, lista_fechas, precios)
        
            
        
        
        #tupla=[codigo_pagina, pagina, descr, habitaciones,m2, con_garaje,nombre_archivo]
        tupla=[codigo_pagina, pagina, descr, habitaciones,m2, con_garaje]
        
        lista_inmuebles.append ( tupla )
    return lista_inmuebles
        

def get_objetos(consulta_sql):
    global conexion_global_memoria
    #print("Ejecutando:"+consulta_sql)
    cursor=conexion_global_memoria.cursor()
    #cursor = connection.cursor()
    cursor.execute(consulta_sql)
    filas = cursor.fetchall()
    return (filas)

def get_vector_objetos(consulta_sql, columna=0):
    objetos=get_objetos(consulta_sql)
    vector=[]
    for objeto in objetos:
        vector.append(str(objeto[columna]))
    return vector

def get_vector_enteros(consulta_sql, columna=0):
    objetos=get_objetos(consulta_sql)
    vector=[]
    for objeto in objetos:
        vector.append(int(objeto[columna]))
    return vector

def generar_serie_datos(lista_valores, con_comillas=False):
    if con_comillas:
        nueva_lista_valores=["'{0}'".format(valor) for valor in lista_valores]
        valores_separados_por_comas=",".join ( nueva_lista_valores )
        return valores_separados_por_comas
    else:
        valores_separados_por_comas=",".join ( lista_valores )
        return valores_separados_por_comas
    
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

conexion_global_fichero_db=sqlite3.connect("db.sqlite3")
conexion_global_memoria=copy_database(conexion_global_fichero_db)
#print(conexion_global_memoria)


pisos=get_objetos(CONSULTA_PRECIO_MEDIO_POR_TIPO)
pisos_por_tipo=[]
for p in pisos:
    media_del_precio=FORMATO_MEDIAS.format ( p[1] )
    desviacion_media=calcular_desviacion_por_tipo(p[0], media_del_precio)
    pisos_por_tipo.append ( [p[0], media_del_precio,
                             FORMATO_MEDIAS.format(desviacion_media) ])
    
CONSULTA_PISOS_POR_HABS="""
Select  avg(precio)
    from inmuebles, precios
    where inmuebles.codigo_pagina=precios.inmueble_id
        and precios.precio<=350000
        and habitaciones={0}
        and tipo='Piso'
"""

habitaciones=[2, 3]
for hab in habitaciones:
    pisos=get_objetos(CONSULTA_PISOS_POR_HABS.format(hab))
    
    media_precio_pisos=FORMATO_MEDIAS.format(pisos[0][0])
    desviacion_media=calcular_desviacion_por_tipo("Piso", media_precio_pisos)
    pisos_por_tipo.append(["Piso de "+str(hab), media_precio_pisos, FORMATO_MEDIAS.format(desviacion_media)])
    
#sys.exit(-1)
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


contexto["valores_graficos"]=tuplas_valores_pisos
contexto["lista_fechas"]=lista_fechas
contexto["valores_graficos_inmuebles"]=objeto_js_cantidad_inmuebles
contexto["estadistica_por_inmueble"]=get_estadistica_por_inmueble()
resultado=render_to_string("mueb/estadisticas.html", contexto)




print (resultado)