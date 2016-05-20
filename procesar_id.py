#!/usr/bin/env python3
#coding=utf-8

import glob, os
from utilidades.ficheros.GestorFicheros import GestorFicheros

from constantes import *
from bs4 import BeautifulSoup
from mueb import models

URL_BASE_CORREGIDA=URL_BASE_AL[:-1]
TIPOS=["Piso", "Casa", "Chalet", "Dúplex", "Ático"]
def procesar_pagina_al ( i, gf ):
    objetos=[]
    nombre_fichero = SUBDIRECTORIO_HTML_AL + os.sep + FICHERO_BASE_AL.format ( i )
    fichero =open (nombre_fichero)
    sopa = BeautifulSoup ( fichero, "html.parser")
    items = sopa.find_all ( "div", "item")
    for item in items:
        info = item.find ( "div", "item-info-container")
        enlace = info.find ( "a", "item-link" )
        texto_enlace=enlace.string
        precio = info.find("span", "item-price")
        id_inm=enlace["href"].replace ("/inmueble/", "")[:-1]
        url_in=URL_BASE_CORREGIDA+enlace["href"]
        detalles=info.find_all("span", "item-detail")
        habitaci=detalles[0].contents[0]
        m2=detalles[1].contents[0]
        try:
            otro=detalles[2].contents[0]
        except IndexError as e:
            otro=""
        if texto_enlace==None:
            print (info)
        print ( texto_enlace, precio.contents[0],  habitaciones, m2)
        c=Inmueble (
            pagina="al", habitaciones=habitaci
        )
        objetos.append(c)
        #gf.descargar_fichero ( url_in, SUBDIRECTORIO_HTML_AL + os.sep + "id_"+id_inm+".html")
    fichero.close()
    return objetos

total=4
gf=GestorFicheros()
lista_objetos=[]
#total=TOTAL_PAGINAS_AL
for i in range (1, total):
    objetos=procesar_pagina_al ( i, gf )
    lista_objetos=lista_objetos+objetos
for o in lista_objetos:
    print (o)