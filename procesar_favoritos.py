#!/usr/bin/env python3
#coding=utf-8

from GestorFicheros import GestorFicheros
from bs4 import BeautifulSoup
from constantes import *
configurador=Configurador("mu")
configurador.activar_configuracion("mu.settings")
from mueb.models import *
from datetime import date

def procesar_favoritos():
    hoy=date.today()
    
    gf=GestorFicheros()
    favoritos_to=[
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/aire-acondicionado-calefaccion-parking-ascensor-amueblado-virgen-de-la-estrella-138854026?RowGrid=6&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/calefaccion-parking-trastero-zona-comunitaria-ascensor-piscina-no-amueblado-severo-ochoa-141465827?RowGrid=25&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/calefaccion-parking-ascensor-no-amueblado-delicias-141522114?RowGrid=13&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/aire-acondicionado-calefaccion-parking-ascensor-mata-11-142074099?RowGrid=15&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/jardin-terraza-trastero-ascensor-parking-centro-el-pilar-142900378?RowGrid=22&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/aire-acondicionado-calefaccion-parking-terraza-trastero-ascensor-plaza-de-los-escultores-rausell-y-llorens-143050962?RowGrid=23&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/trastero-zona-comunitaria-ascensor-parking-piscina-no-amueblado-centro-el-pilar-138606587?RowGrid=25&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/calefaccion-parking-ascensor-la-mata-11-139647571?RowGrid=27&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/aire-acondicionado-calefaccion-parking-jardin-zona-comunitaria-ascensor-piscina-universidad-143254499?RowGrid=3&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/aire-acondicionado-calefaccion-parking-ascensor-piscina-cardenal-lorenzana-143050212?RowGrid=4&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/calefaccion-terraza-zona-comunitaria-ascensor-amueblado-parking-television-virgen-de-la-estrella-9-129844703?RowGrid=5&tti=1&opi=300"
        ,
        "https://www.fotocasa.es/vivienda/ciudad-real-capital/aire-acondicionado-calefaccion-parking-trastero-ascensor-parking-marianistas-ave-140957458?RowGrid=15&tti=1&opi=300"
        
        ]
    temp="t.html"
    for f in favoritos_to:
        gf.descargar_fichero(f, temp)
        fichero=open(temp, "r")
        bs=BeautifulSoup(fichero, "lxml")
        
        objeto = Favorito.objects.filter(enlace=f)
        if (len(objeto)==0):
            #print("No Existe")
            span_habitaciones=bs.find("span", {"id":"litRooms"})
            cad_habitaciones=span_habitaciones.b.text
            num_habitaciones=int(cad_habitaciones)
            
            span_superficie=bs.find("span", {"id":"litSurface"})
            if span_superficie==None:
                cad_superficie="0"
            else:
                cad_superficie=span_superficie.b.text
            
            num_superficie=int(cad_superficie)
            
            
            texto_descripcion=bs.find("h1", "property-title")
            
            txt=texto_descripcion.text.strip()
            objeto=Favorito(enlace=f, m2=num_superficie, descr=txt, habitaciones=num_habitaciones)
            objeto.save()
        else:
            objeto=objeto[0]
            #print(objeto)
        
        span_precio=bs.find("span", {"id":"priceContainer"})
        texto_precio=span_precio.text.replace(".", "")
        texto_precio=texto_precio.strip()
        texto_precio=texto_precio.replace("€", "")
        num_precio=int(texto_precio)
        #print(num_precio)
        precio_favorito=PrecioFavorito(inmueble=objeto, fecha=hoy, precio=num_precio)
        precio_favorito.save()
        fichero.close()
        
if __name__ == '__main__':
    
    procesar_favoritos()