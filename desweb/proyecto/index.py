# -*- coding: utf-8 -*-

#Con las aplicaciones WSGI no funcionan las rutas relativas,
#Para que funcione hay que especificar la ruta absoluta.
import sys, os

dir_base=os.path.dirname(__file__)
sys.path.append(dir_base) #Añade a la variable path de python el directorio
#de este fichero, así ya se pueden argar módulos y archivos de esta carpeta.

from py import procesa_opcion_menu
from py import procesa_formulario

sys.path.append(r"D:\LiClipse\plugins\org.python.pydev_3.9.2.201502042042\pysrc")
#import pydevd

def application(environ, start_response):
    #Código html dinámico
    #pydevd.settrace()
    #html=procesa_opcion_menu.procesa_opcion_menu(environ)
    
    if environ['REQUEST_METHOD']=='POST':
        #pydevd.settrace()
        opf=procesa_formulario.procesar_formularios(environ)
        html=opf.procesa_formulario()
    else:
        html=procesa_opcion_menu.procesa_opcion_menu(environ)
        
    
    #Envío al servidor. Siempre igual.
    status = '200 OK'
    response_headers = [('Content-Type', 'text/html'),('ContentLength', str(len(html)))]
    start_response(status, response_headers)
    return [str(html)]