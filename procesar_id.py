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


def get_tipo(texto):
    for t in TIPOS:
        if texto.find ( t ) !=-1:
            return t
    return "DESC"

def procesar_pagina_al ( i, gf ):
    
    objetos=[]
    precios=[]
    nombre_fichero = SUBDIRECTORIO_HTML_AL + os.sep + FICHERO_BASE_AL.format ( i )
    print ("Abriendo "+nombre_fichero)
    fichero =open (nombre_fichero)
    sopa = BeautifulSoup ( fichero, "html.parser")
    items = sopa.find_all ( "div", "item")
    for item in items:
        info = item.find ( "div", "item-info-container")
        enlace = info.find ( "a", "item-link" )
        texto_enlace=enlace.string.strip()
        precio_visto = info.find("span", "item-price")
        id_inm=enlace["href"].replace ("/inmueble/", "")[:-1]
        url_in=URL_BASE_CORREGIDA+enlace["href"]
        print (url_in)
        detalles=info.find_all("span", "item-detail")
        habitaci=detalles[0].contents[0]
        try:
            habitaci=int(habitaci)
        except:
            habitaci=0
        try:
            superf=int(detalles[1].contents[0])
        except :
            superf=0
        tipo_inm=get_tipo ( texto_enlace )
        try:
            otro=detalles[2].contents[0].strip()
        except IndexError as e:
            otro=""
        if texto_enlace==None:
            print (info)
        print (  texto_enlace, precio_visto.contents[0],  habitaci, superf)
        c=Inmueble (
            pagina="al", habitaciones=habitaci,
            enlace=url_in, m2=superf, fecha_inclusion=hoy, codigo_pagina=id_inm,
            tipo=tipo_inm, descr=texto_enlace, otros=otro
        )
        objetos.append(c)
        euros=precio_visto.contents[0].replace(".", "")
        p=Precio (
            inmueble=c, precio=int(euros), fecha=hoy
        )
        precios.append (p)
        print (c)
        #gf.descargar_fichero ( url_in, SUBDIRECTORIO_HTML_AL + os.sep + "id_"+id_inm+".html")
    fichero.close()
    return (objetos, precios)

#total=4
gf=GestorFicheros()
lista_objetos=[]
lista_precios=[]
total=TOTAL_PAGINAS_AL
for i in range (1, total):
    print ("Procesando pag "+str(i))
    (objetos, precios)=procesar_pagina_al ( i, gf )
    lista_objetos=lista_objetos+objetos
    lista_precios=lista_precios+precios
    
with transaction.atomic():    
    for o in lista_objetos:
        print (o.descr, o.enlace)
        o.save()
        
with transaction.atomic():    
    for p in lista_precios:
        print (p.precio)
        p.save()
    