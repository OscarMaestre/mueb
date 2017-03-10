#!/usr/bin/env python3
# coding=utf-8

import os
import platform
import requests
import jinja2
from subprocess import call

class GestorFicheros(object):
    """Simplica las operaciones con ficheros"""
    def __init__(self):
        self.BORRAR=""
        self.COPIAR=""
        self.CONCAT=""
        self.MOVER=""
        if platform.system()=="Linux":
            self.BORRAR="rm "
            self.COPIAR="cp "
            self.CONCAT="cat "
            self.MOVER="mv "
            self.FICHERO_CONFIGURACION_EMAIL="/home/usuario/repos/configuracion_envio_email.txt"
            self.FICHERO_CONFIGURACION_EMAIL_AFILIADOS="/home/usuario/repos/configuracion_envio_email_afiliados.txt"
            self.FICHERO_DESTINATARIOS_EMAIL="/home/usuario/repos/destinatarios.txt"
        else:
            self.BORRAR="del "
            self.COPIAR="copy "
            self.CONCAT="type "
            self.MOVER="move "
            self.FICHERO_CONFIGURACION_EMAIL="C:\\repos\\configuracion_envio_email.txt"
            self.FICHERO_CONFIGURACION_EMAIL_AFILIADOS="C:\\repos\\configuracion_envio_email_afiliados.txt"
            self.FICHERO_DESTINATARIOS_EMAIL="C:\\repos\\destinatarios.txt"
            
    def anadir_a_fichero(self, texto, nombre_fichero):
        with open (nombre_fichero, "a") as f:
            f.write(texto)
    def escribir_en_fichero(self, texto, nombre_fichero):
        with open (nombre_fichero, "w") as f:
            f.write(texto)
            
    def leer_linea_fichero(self, num_linea, nombre_fichero):
        """Devuelve una linea de un fichero.
        
            Argumentos:
            
                num_linea -- Numero de línea a leer
                
                nombre_fichero -- Cadena con la ruta del fichero a leer
        """
        with open (nombre_fichero, "r") as f:
            lineas=f.readlines()
            return lineas[num_linea].strip()
        
    def leer_fichero(self, nombre_fichero):
        """Leer todo un fichero
        
            Argumentos:
            
                nombre_fichero -- nombre del fichero a leer
            
            Devuelve:
            
                cadena -- una cadena con todo el fichero completo
        """
        with open (nombre_fichero, "r") as f:
            lineas=f.readlines()
        texto=""
        for l in lineas:
            texto+=l
        return texto
    
    
    def reemplazar_espacios(self, nombre):
        temp=nombre.replace(" ", "_")
        temp=temp.replace("(", "_")
        temp=temp.replace(")", "_")
        #print ("Nombre viejo {0}, nombre nuevo {1}".format(nombre, temp))
        return temp

    def aplicar_comando (self, comando, fichero, *args):
        cmd=comando + " "+fichero
        for a in args:
            cmd+=" " + a
        print("Ejecutando "+cmd)
        call(cmd, shell=True)
    
    def ejecutar_comando (self, comando, fichero, *args):
        """
        Ejecuta un comando
        
        Argumentos:
        
            comando -- nombre del comando a ejecutar (sin ./)
            
            fichero -- parametro obligatorio, poner "" si es necesario
            
            args -- resto de parámetros
            
        """
        self.aplicar_comando(comando, fichero, *args)
        
    def escapar_fichero_con_espacios(self, nombre_fichero):
        nombre_fichero="\""+nombre_fichero+"\""
        return nombre_fichero
    
    def copiar_fichero(self, nombre_origen, nombre_destino):
        self.aplicar_comando(self.COPIAR, nombre_origen, nombre_destino)
        
    def borrar_fichero(self, nombre_fichero):
        self.aplicar_comando(self.BORRAR, nombre_fichero)
        
    def concatenar_fichero(self, fichero1, fichero2):
        self.aplicar_comando(self.CONCAT, fichero1, " >> ", fichero2)
        
    def obtener_ficheros(self, patron):
        return glob.glob(patron)
    
    def crear_directorio(self, ruta_completa):
        try:
            os.mkdir(ruta_completa)
        except FileExistsError:
            return 
    def get_lineas_fichero(self, nombre_fichero):
        """Leer las lineas de un fichero
        
            Argumentos:
            
                nombre_fichero -- nombre del fichero a leer
                
            Devuelve:
            
                lista -- una lista con todas las lineas del fichero sin fin de linea (se usa strip)
        """
        lineas_sin_fin_de_linea=[]
        with open(nombre_fichero, "r") as f:
            lineas=f.readlines()
            f.close()
        for l in lineas:
            lineas_sin_fin_de_linea.append ( l.strip() )
        return lineas_sin_fin_de_linea
    
    def mover_fichero(self, fichero, dir_destino):
        fichero=self.escapar_fichero_con_espacios(fichero)
        dir_destino=self.escapar_fichero_con_espacios(dir_destino)
        self.aplicar_comando ( self.MOVER, fichero , dir_destino)
        
    def renombrar_fichero_con_espacios(self, fichero):
        nuevo_nombre=self.escapar_fichero_con_espacios(fichero)
        self.mover_fichero (fichero, nuevo_nombre)
        return nuevo_nombre
    def existe_fichero(self, nombre_fichero):
        """
        
        Nos dice si un fichero existe o no
        
        Argumentos:
        
            nombre_fichero -- Nombre del fichero a comprobar
            
        Devuelve
        
            True -- si el fichero existe
            
            False -- si el fichero no existe
        """
        
        if os.path.isfile(nombre_fichero):
            return True
        return False
    
    def renombrar_fichero(self, nombre_viejo, nombre_nuevo):
        if nombre_nuevo==nombre_viejo:
            #print("No hace falta renombrar:"+nombre_viejo)
            return 
        self.aplicar_comando(self.MOVER, "\""+nombre_viejo+"\"", nombre_nuevo)
        
    def enviar_texto_a_comando(self, texto, comando):
        if platform.system()=="Linux":
            comando_envio="echo '{0}'".format(texto)
        else:
            comando_envio="echo {0}".format(texto)
            
        self.aplicar_comando ( comando_envio, "|", comando)
    
    def extraer_esquema(self, archivo_bd, nombre_tabla, archivo_sql_resultado, anadir=False):
        texto=".schema {0}".format ( nombre_tabla )
        if anadir:
            comando="sqlite3 {0} >> {1}".format(archivo_bd, archivo_sql_resultado)
        else:
            comando="sqlite3 {0} > {1}".format(archivo_bd, archivo_sql_resultado)
        self.enviar_texto_a_comando( texto, comando)
        
    def extraer_datos_tabla(self, archivo_bd, nombre_tabla, archivo_sql_resultado,anadir=True):
        texto=r".mode insert {0}\nselect * from {0};".format(
            nombre_tabla
        )
        if anadir:
            comando="sqlite3 {0}>>{1}".format ( archivo_bd ,archivo_sql_resultado)
        else:
            comando="sqlite3 {0}>{1}".format ( archivo_bd ,archivo_sql_resultado)
        self.enviar_texto_a_comando ( texto, comando)
    
    def exportar_tabla(self, archivo_bd, nombre_tabla,
                       archivo_sql_resultado, bd_destinataria=None,
                       borrar_fichero_sql_intermedio=True):
        self.anadir_a_fichero("BEGIN TRANSACTION;", archivo_sql_resultado)
        self.extraer_esquema ( archivo_bd, nombre_tabla, archivo_sql_resultado,anadir=True )
        self.extraer_datos_tabla ( archivo_bd, nombre_tabla, archivo_sql_resultado )
        self.anadir_a_fichero("COMMIT TRANSACTION;", archivo_sql_resultado)
        if bd_destinataria!=None:
            self.ejecutar_comando ( self.CONCAT, archivo_sql_resultado, "|", "sqlite3 " + bd_destinataria)
        if borrar_fichero_sql_intermedio:
            self.borrar_fichero ( archivo_sql_resultado )

    def exportar_lista_tablas (self, archivo_bd, lista_tablas, archivo_sql_resultado):
        self.borrar_fichero ( archivo_sql_resultado )
        for t in lista_tablas:
            self.anadir_a_fichero("BEGIN TRANSACTION;", archivo_sql_resultado)
            self.exportar_tabla ( archivo_bd, t, archivo_sql_resultado)
            self.anadir_a_fichero("COMMIT TRANSACTION;", archivo_sql_resultado)
    
        
    def descargar_fichero(self, url, nombre_fichero_destino):
        peticion = requests.get ( url )
        descriptor=open (nombre_fichero_destino, "w")
        descriptor.write ( peticion.text )
        descriptor.close()
    def rellenar_fichero_plantilla(self, fichero_plantilla, diccionario,  fichero_salida=None):
        
        texto_plantilla=self.leer_fichero(fichero_plantilla)
        plantilla=jinja2.Template(texto_plantilla)
        plantilla_rellena=plantilla.render( diccionario )
        if fichero_salida!=None:
            self.escribir_en_fichero ( plantilla_rellena, fichero_salida)
        return plantilla_rellena
        