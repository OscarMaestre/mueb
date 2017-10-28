#!/usr/bin/env python3
#coding=utf-8

import glob, os, sys, re


from constantes import *
from bs4 import BeautifulSoup, Comment

re_caracteristicas="ctl00_content1_gridphotos_rptGridPhotos"
expr_regular_caracteristicas=re.compile(re_caracteristicas)
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

def get_num_habitaciones ( div ):
    print ("Obteniendo num habs")
    try:
        cad_num=div.span.string
    except:
        return 0
    trozos=cad_num.split(" ")
    #print (trozos[0])
    return int(trozos[0])

def get_superficie(div):
    spans=div.find_all("span", "re-Card-feature")
    try:
        span_sup=spans[-1]
    except:
        return 0
    #print (span_sup)
    trozos=span_sup.string.split(" ")
    return int(trozos[0])

def obtener_id_inmueble(url):
    print("Obteniendo enlace:"+url)
    trozos=url.split("?RowGrid")
    url=trozos[0]
    identificador=url[-9:]
    print("ID:"+identificador)
    return identificador

def procesar_pagina_to_2 ( i, gf ):
    objetos=[]
    precios=[]
    nombre_fichero = SUBDIRECTORIO_HTML_TO + os.sep + FICHERO_BASE_TO.format ( i )
    #print ("Abriendo "+nombre_fichero)
    fichero =open (nombre_fichero, encoding="utf-8")
    sopa = BeautifulSoup ( fichero, "html.parser")
    
    items = sopa.find_all ( "div", "re-Card-link")
    print ("Encontre:"+str(len(items)))
    for item in items:
        print(item)
        enlace_descripcion=item.find ( "a", "re-Card-title")

        texto_enlace=enlace_descripcion.contents[4]
        print ("Descripcion:"+texto_enlace)
        #Recuperamos el precio
        
        contenedor_precio_visto = item.find("span", "re-Card-price")
        try:
            precio_visto=contenedor_precio_visto.contents[0].contents[1]
        except :
            precio_visto="0"
        print(precio_visto)
        
        #print (precio_visto)
        caracteristicas=item.find("div", "re-Card-wrapperFeatures")
        #print(caracteristicas)
        tipo_inm=get_tipo(caracteristicas)
        
        habitaci=get_num_habitaciones(caracteristicas)
        
        superf=get_superficie(caracteristicas)
        print (tipo_inm, ">>>hab>>>", habitaci, ">>>>", superf)
        
        enlace_ampl=item.find("a", "re-Card-title")
        url_in=enlace_ampl["href"]
        id_inm=obtener_id_inmueble(url_in)
        #print (url_in)
        otro=""
        garaje_incl=False
        c=Inmueble (
            pagina="to", habitaciones=habitaci,
            enlace=url_in, m2=superf, fecha_inclusion=hoy, codigo_pagina=id_inm,
            tipo=tipo_inm, descr=texto_enlace, otros=otro , con_garaje=garaje_incl
        )
        objetos.append(c)
        euros=precio_visto.replace(".", "")
        p=Precio (
            inmueble=c, precio=int(euros), fecha=hoy
        )
        precios.append (p)
        #print (c)
        #gf.descargar_fichero ( url_in, SUBDIRECTORIO_HTML_TO + os.sep + "id_"+id_inm+".html")
    fichero.close()
    #print ("Pagina cerrada")
    return (objetos, precios)

def procesar_pagina_to ( i, gf ):
    objetos=[]
    precios=[]
    nombre_fichero = SUBDIRECTORIO_HTML_TO + os.sep + FICHERO_BASE_TO.format ( i )
    #print ("Abriendo "+nombre_fichero)
    fichero =open (nombre_fichero, encoding="utf-8")
    sopa = BeautifulSoup ( fichero, "html.parser")
    
    items = sopa.find_all ( "a", "re-Card-link")
    print ("Encontre:"+str(len(items)))
    for item in items:
        
        enlace_descripcion=item.find ( "h4", "re-Card-title")

        texto_enlace=enlace_descripcion.string
        print ("Descripcion:"+texto_enlace)
        #Recuperamos el precio
        
        contenedor_precio_visto = item.find("span", "re-Card-price")
        try:
            precio_visto=contenedor_precio_visto.contents[0].contents[1]
        except :
            precio_visto="0"
        print("Precio:"+precio_visto)
        
        #print (precio_visto)
        caracteristicas=item.find("div", "re-Card-wrapperFeatures")
        #print(caracteristicas)
        tipo_inm=get_tipo(caracteristicas)
        
        habitaci=get_num_habitaciones(caracteristicas)
        
        superf=get_superficie(caracteristicas)
        print (tipo_inm, ">>>hab>>>", habitaci, ">>>>", superf)
        
        enlace_ampl=item.find("a", "re-Card-title") 
        url_in=item["href"]
        
        id_inm=obtener_id_inmueble(url_in)
        print ("Id inmuebles:"+id_inm)
        #print (url_in)
        otro=""
        garaje_incl=False
        c=Inmueble (
            pagina="to", habitaciones=habitaci,
            enlace=url_in, m2=superf, fecha_inclusion=hoy, codigo_pagina=id_inm,
            tipo=tipo_inm, descr=texto_enlace, otros=otro , con_garaje=garaje_incl
        )
        objetos.append(c)
        euros=precio_visto.replace(".", "")
        p=Precio (
            inmueble=c, precio=int(euros), fecha=hoy
        )
        precios.append (p)
        #print (c)
        #gf.descargar_fichero ( url_in, SUBDIRECTORIO_HTML_TO + os.sep + "id_"+id_inm+".html")
    fichero.close()
    #print ("Pagina cerrada")
    return (objetos, precios)


#total=4
gf=GestorFicheros()
lista_objetos=[]
lista_precios=[]
total=TOTAL_PAGINAS_TO
#total=2
for i in range (1, total):
    print ("Procesando pag "+str(i))
    (objetos, precios)=procesar_pagina_to ( i, gf )
    lista_objetos=lista_objetos+objetos
    lista_precios=lista_precios+precios

with transaction.atomic():    
    for o in lista_objetos:
        print (o.descr, o.enlace)
        o.save()
        
with transaction.atomic():    
    for p in lista_precios:
        #print (p.precio)
        p.save()
