#!/usr/bin/env python3
#coding=utf-8

import os, sys
from time import sleep
from constantes import *

SEGS_ESPERA_ENTRE_PAGINAS = 3

gf=GestorFicheros()
gf.crear_directorio ( SUBDIRECTORIO_HTML_AL )

for i in range(1, TOTAL_PAGINAS_AL):
    url_descarga        = URL_PAGINAS_AL.format ( i )
    fichero_destino     = SUBDIRECTORIO_HTML_AL + os.sep + FICHERO_BASE_AL.format ( i )
    print ( url_descarga, fichero_destino )
    if not gf.existe_fichero( fichero_destino ):
        gf.descargar_fichero(url_descarga, fichero_destino)
        sleep ( SEGS_ESPERA_ENTRE_PAGINAS )