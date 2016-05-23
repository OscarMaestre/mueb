#!/usr/bin/env python3
#coding=utf-8

from utilidades.ficheros.GestorFicheros import GestorFicheros
import glob, platform


gf=GestorFicheros()

patrones=["al/*.html"]

for p in patrones:
    ficheros_a_borrar=glob.glob(p)
    for f in ficheros_a_borrar:
        gf.borrar_fichero ( f )
        
if platform.system()=="Linux":
    DESCARGADOR         =   "./descargador_html_al.py"
    PROCESAR_ID         =   "./procesar_id.py"
    CREAR_ESTADISTICAS  =   "./crear_estadisticas.py"
else:
    DESCARGADOR         =   "descargador_html_al.py"
    PROCESAR_ID         =   "procesar_id.py"
    CREAR_ESTADISTICAS  =   "crear_estadisticas.py"
    
    
gf.ejecutar_comando ( DESCARGADOR , "")
gf.ejecutar_comando ( PROCESAR_ID , "")
gf.ejecutar_comando ( CREAR_ESTADISTICAS , ">", "resultados.html")

