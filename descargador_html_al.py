#!/usr/bin/env python3
#coding=utf-8

import os, sys

from utilidades.ficheros.GestorFicheros import GestorFicheros
from constantes import *


gf=GestorFicheros()
gf.crear_directorio ( SUBDIRECTORIO_HTML_AL )

for i in range(1, TOTAL_PAGINAS_AL):
    url_descarga        = URL_BASE_AL.format ( i )
    fichero_destino     = SUBDIRECTORIO_HTML_AL + os.sep + FICHERO_BASE.format ( i )
    if not gf.existe_fichero( fichero_destino ):
        gf.descargar_fichero(url_descarga, fichero_destino)