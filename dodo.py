#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.GestorFicheros import GestorFicheros
import glob, platform, sys, os

from datetime import date

hoy=date.today()
fecha_hoy=hoy.strftime("%Y%m%d")
print (fecha_hoy)


gf=GestorFicheros()

patrones=["al/*.html", "to/*.html"]

for p in patrones:
    ficheros_a_borrar=glob.glob(p)
    for f in ficheros_a_borrar:
        gf.borrar_fichero ( f )
        
FICHERO_RESULTADO="resultados" + os.sep +"resultados_{0}.html".format(fecha_hoy)

if platform.system()=="Linux":
    DESCARGADOR_AL      =   "./descargador_html_al.py"
    DESCARGADOR_TO      =   "./descargador_html_to.py"
    PROCESAR_ID_AL      =   "./procesar_id.py"
    PROCESAR_ID_TO      =   "./procesar_to.py"
    CREAR_ESTADISTICAS  =   "./crear_estadisticas.py"
else:
    DESCARGADOR_AL      =   "descargador_html_al.py"
    DESCARGADOR_TO      =   "descargador_html_to.py"
    PROCESAR_ID_AL      =   "procesar_id.py"
    PROCESAR_ID_TO      =   "procesar_to.py"
    CREAR_ESTADISTICAS  =   "crear_estadisticas.py"
    
    
gf.ejecutar_comando ( DESCARGADOR_AL , "")
gf.ejecutar_comando ( DESCARGADOR_TO , "")
gf.ejecutar_comando ( PROCESAR_ID_AL , "")
gf.ejecutar_comando ( PROCESAR_ID_TO , "")
gf.ejecutar_comando ( CREAR_ESTADISTICAS , ">", FICHERO_RESULTADO)

