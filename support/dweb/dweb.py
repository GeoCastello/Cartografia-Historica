# -*- encoding: utf-8 -*-
'''
Created on 6/4/2016

@author: ADRIAN
'''

def leer_archivo(nom_arch):
    """Recibe el nombre de un archivo y devuelve su contenido en un string
    Esta funcion no es robusta, no tiene control de errores
    Si el archivo no existe, fallara"""
    archivo=open(nom_arch, 'r') #La ruta desde el programa Principal
    contenido=archivo.read()
    archivo.close()
    return contenido

def reemplazar(cadena, diccionario):
    """Función que recibe una cadena y un diccionario. Devuelve una
    cadena donde
    ha sustiruido las claves de un dicionario contenidas en una
    cadena por los
    valores del diccionario.
    No se modifica la cadena original dentro de la función.
    original="El título es: {{titulo}}. El autor es: {{autor}}"
    diccionario:
    di=dict()
    di["{{titulo}}"]="The number of the beast"
    di["{{autor}}"]="Iron Maiden"
    Ejemplo de uso: reemplazar(original,di)
    Devuelve: El título es: The number of the beast. El autor es:
    Iron Maiden
    @type diccionaio: dict
    @param diccionario: diccionario clave:valor
    @type cadena: string
    53
    3.4 Práctica 5. Creación de una aplicación wsgi
    @param cadena: cadena a sustituir las claves por sus valores
    @return: una nueva cadena con los valores dentro, en vez de las
    claves"""
    a=cadena #hace una copia de la cadena para no modificar la original
    
    for key in diccionario.keys():
        key2='{{'+key+'}}'
        a=a.replace(key2, diccionario[key])
    return a

from urlparse import parse_qs #librería estándar de python
def devuelve_dict_get(environ):
    """
    Esta función devuelve un diccionario con los valores de una solicitud de
    un recurso empleando el metodo get.
    """
    qs = environ['QUERY_STRING']
    d=parse_qs(qs, True)#el parámetro opcional true conserva los valores en blanco
    #la llave estará pero vale ''
    return d

def devuelve_dict_post(environ):
    """
    Devuelve un diccionario clave:valor con los datos del formulario
    Las claves son strings. Los valores son listas de valores.
    Importante, una vez que se ha leído el el contenido post,
    ya no se puede volver a leer. Se quedará bloqueado el ordenador.
    Solo se puede llamar a esta función una vez por formulario.
    """
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    d = parse_qs(request_body)
    return d

