#!/usr/bin/env python3
#coding=utf-8

import glob, os, sys
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
URL_BASE_CORREGIDA=URL_BASE_TO[:-1]


def get_tipo(texto):
    for t in TIPOS:
        if texto.find ( t ) !=-1:
            return t
    return "DESC"

def procesar_pagina_to ( i, gf ):
    
    objetos=[]
    precios=[]
    nombre_fichero = SUBDIRECTORIO_HTML_TO + os.sep + FICHERO_BASE_TO.format ( i )
    print ("Abriendo "+nombre_fichero)
    fichero =open (nombre_fichero)
    sopa = BeautifulSoup ( fichero, "html.parser")
    
    items = sopa.find_all ( "div", "o-card_content")
    for item in items:
        enlace_descripcion=item.find ( "span", "location")
        texto_enlace=enlace_descripcion.string.strip()
        print (texto_enlace)
        precio_visto = item.find("span", "property-card_price").string.strip()[:-2]
        if precio_visto.find("consult")!=-1:
            precio_visto="0"
        print (precio_visto)
        continue
        
        hermano_precio_visto=precio_visto.next_sibling.next_sibling
        garaje_incl=False
        if hermano_precio_visto!=None:
            texto=hermano_precio_visto.string
            if texto=="Garaje incluido":
                garaje_incl=True
                print (texto)
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
            tipo=tipo_inm, descr=texto_enlace, otros=otro, con_garaje=garaje_incl
        )
        objetos.append(c)
        euros=precio_visto.contents[0].replace(".", "")
        p=Precio (
            inmueble=c, precio=int(euros), fecha=hoy
        )
        precios.append (p)
        #print (c)
        #gf.descargar_fichero ( url_in, SUBDIRECTORIO_HTML_TO + os.sep + "id_"+id_inm+".html")
    fichero.close()
    return (objetos, precios)

#total=4
gf=GestorFicheros()
lista_objetos=[]
lista_precios=[]
total=TOTAL_PAGINAS_TO
for i in range (1, total):
    print ("Procesando pag "+str(i))
    (objetos, precios)=procesar_pagina_to ( i, gf )
    lista_objetos=lista_objetos+objetos
    lista_precios=lista_precios+precios
sys.exit()    
with transaction.atomic():    
    for o in lista_objetos:
        print (o.descr, o.enlace)
        o.save()
        
with transaction.atomic():    
    for p in lista_precios:
        print (p.precio)
        p.save()
