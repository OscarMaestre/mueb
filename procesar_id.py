#!/usr/bin/env python3
#coding=utf-8

import glob, os
from utilidades.ficheros.GestorFicheros import GestorFicheros
from utilidades.basedatos.Configurador import Configurador

from constantes import *
from bs4 import BeautifulSoup


configurador=Configurador("mu")
configurador.activar_configuracion("mu.settings")

from mueb.models import *
from datetime import date, datetime
from django.db import transaction
hoy=datetime.now()
URL_BASE_CORREGIDA=URL_BASE_AL[:-1]
TIPOS=["Piso", "Casa", "Chalet", "Dúplex", "Ático"]

def get_tipo(texto):
    for t in TIPOS:
        if texto.find ( t ) !=-1:
            return t
    return "DESC"

def procesar_pagina_al ( i, gf ):
    
    objetos=[]
    nombre_fichero = SUBDIRECTORIO_HTML_AL + os.sep + FICHERO_BASE_AL.format ( i )
    print ("Abriendo "+nombre_fichero)
    fichero =open (nombre_fichero)
    sopa = BeautifulSoup ( fichero, "html.parser")
    items = sopa.find_all ( "div", "item")
    for item in items:
        info = item.find ( "div", "item-info-container")
        enlace = info.find ( "a", "item-link" )
        texto_enlace=enlace.string.strip()
        precio = info.find("span", "item-price")
        id_inm=enlace["href"].replace ("/inmueble/", "")[:-1]
        url_in=URL_BASE_CORREGIDA+enlace["href"]
        print (url_in)
        detalles=info.find_all("span", "item-detail")
        habitaci=detalles[0].contents[0]
        try:
            superf=detalles[1].contents[0]
        except IndexError:
            superf=0
        tipo_inm=get_tipo ( texto_enlace )
        try:
            otro=detalles[2].contents[0].strip()
        except IndexError as e:
            otro=""
        if texto_enlace==None:
            print (info)
        print (  texto_enlace, precio.contents[0],  habitaci, superf)
        c=Inmueble (
            pagina="al", habitaciones=habitaci,
            enlace=url_in, m2=superf, fecha_inclusion=hoy, codigo_pagina=id_inm,
            tipo=tipo_inm, descr=texto_enlace, otros=otro
        )
        objetos.append(c)
        print (c)
        #gf.descargar_fichero ( url_in, SUBDIRECTORIO_HTML_AL + os.sep + "id_"+id_inm+".html")
    fichero.close()
    return objetos

#total=4
gf=GestorFicheros()
lista_objetos=[]
total=TOTAL_PAGINAS_AL
for i in range (1, total):
    print ("Procesando pag "+str(i))
    objetos=procesar_pagina_al ( i, gf )
    lista_objetos=lista_objetos+objetos

with transaction.atomic():    
    for o in lista_objetos:
        #print (o)
        o.save()
    