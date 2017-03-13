# -*- coding: utf-8 -*-

from dweb import dweb
from py import var_globales
import os

dir_base=os.path.dirname(__file__) #Ruta absoluta del archivo actual

def crea_head():
    """
    Inicio del documento y crea el head
    """
    nom_arch=dir_base+"/html_secciones/head.html"
    cabecera=dweb.leer_archivo(nom_arch)    
    return cabecera


def crea_header_ppal():
    """
    Empieza el body y crea el menú de navegación Principal
    """   
    nom_arch=dir_base+"/html_secciones/header_ppal.html"
    header_ppal=dweb.leer_archivo(nom_arch)    
    return header_ppal


def crea_aside():
    """
    Crea el menú lateral derecho
    """   
    nom_arch=dir_base+"/html_secciones/aside.html"
    aside=dweb.leer_archivo(nom_arch)    
    return aside


def comienza_seccion_principal():
    """
    Crea el inicio de la sección principal
    """ 
    html="""
    <section id="seccion" class="seccion">
    """    
    return html


def crea_mapa():
    """Crea el mapa
    """
    nom_arch=dir_base+"/html_secciones/seccion_mapa.html"
    seccion_mapa=dweb.leer_archivo(nom_arch)    
    return seccion_mapa


def crea_home():
    """Crea el home
    """
    nom_arch=dir_base+"/html_secciones/seccion_home.html"
    seccion_home=dweb.leer_archivo(nom_arch)   
    return seccion_home


def crea_contacto():
    """Crea contacto
    """
    nom_arch=dir_base+"/html_secciones/seccion_contacto.html"
    seccion_contacto=dweb.leer_archivo(nom_arch)
    seccion_contacto2=dweb.reemplazar(cadena=seccion_contacto, diccionario=var_globales.dev_glob())  
    return seccion_contacto2


def crea_ayuda():
    """Crea ayuda
    """
    nom_arch=dir_base+"/html_secciones/seccion_ayuda.html"
    seccion_ayuda=dweb.leer_archivo(nom_arch)  
    return seccion_ayuda


def termina_seccion_principal():
    """Cierra la sección Principal
    """
    html="""
    </section>
    """
    return html


def crea_seccion_rustica():
    """
    Crea la sección dedicada a las tablas de rustica
    """
    nom_arch=dir_base+"/html_secciones/seccion_rustica.html"
    seccion_rustica=dweb.leer_archivo(nom_arch)  
    return seccion_rustica


def crea_seccion_urbana():
    """
    Crea la sección dedicada a las tablas de urbana
    """
    nom_arch=dir_base+"/html_secciones/seccion_urbana.html"
    seccion_urbana=dweb.leer_archivo(nom_arch) 
    return seccion_urbana


def crea_seccion_tablas(tabla_rus=None, tabla_urb=None):
    """
    Crea la sección de las tablas
    """
    seccion_tablas="<section id='tablas' class='tablas'>"
    if tabla_rus!=None:
        dic_rus={}
        dic_rus["TABLA_RUS"]=tabla_rus
        rustica=dweb.reemplazar(crea_seccion_rustica(), dic_rus)
        seccion_tablas+=rustica
    if tabla_urb!=None:
        dic_urb={}
        dic_urb["TABLA_URB"]=tabla_urb
        urbana=dweb.reemplazar(crea_seccion_urbana(), dic_urb) 
        seccion_tablas+=urbana
    seccion_tablas+="</section>"
    return seccion_tablas
        
        
def crea_footer_ppal():
    """
    Crea el footer, cierra el body y el documento
    """
    nom_arch=dir_base+"/html_secciones/footer_ppal.html"
    footer_ppal=dweb.leer_archivo(nom_arch)
    return footer_ppal


def crea_pagina_completa(dib_mapa=False, funcion_creacion=None, html_ins=None):
    """
    Crea una página web con todas sus partes y permite cambiar el
    contenido de la sección principal de dos formas:
    Llamando a una función, si se proporciona el parámetro función_creación,
    o insertando código html, si se proporciona el parámetro html_ins.
    Si se proporciona html_ins, funcion_creacion debe ser None.
    Parámetros:
    titulo: Diccionario clave valor. {'titulo_principal':'nuevo título'}
    dib_mapa: si es true se crea el div que contendrá el mapa de openlayers.
    funcion_creacion: función que ejecutandola devuelve código html a insertar
    en la sección principal.
    html_ins: código html a insertar en la sección principal.
    """
    #pydevd.settrace() 
    head=dweb.reemplazar(cadena=crea_head(), diccionario=var_globales.dev_glob())
    header_ppal=crea_header_ppal()
    comienzo_sec_ppal=comienza_seccion_principal()
    if dib_mapa:
        mapa=crea_mapa()
    else:
        mapa=""     
    if funcion_creacion!=None:
        nueva_seccion=funcion_creacion()
    else:
        nueva_seccion=""     
    if html_ins!=None:
        nueva_seccion=nueva_seccion+html_ins
    fin_sec_ppal=termina_seccion_principal()
    aside=crea_aside()
    seccion_tablas="""
    <section id='tablas' class='tablas' style="display:none;"></section>
    """
    footer_ppal=dweb.reemplazar(cadena=crea_footer_ppal(), diccionario=var_globales.dev_glob())
    html=head+header_ppal+mapa+comienzo_sec_ppal+nueva_seccion+fin_sec_ppal+aside+seccion_tablas+footer_ppal
    return html
    
    
def crea_seccion_principal(mas_contenido_html=None):
    """
    Crea la seccion principal. Recibe:
        *Un string con el títuo de la sección
        *Si mapa es true crea el mapa
        *html que es insertado directamente en caso de no ser none.
    """  
    html=comienza_seccion_principal()
    if mas_contenido_html!=None:
        html=html+"\n"+mas_contenido_html  
    html=html+"\n"+termina_seccion_principal()
    return html


def crea_muni(lista):
    
    if not lista==[]:
        html='<select id="municipio_final" name="municipio_final" class="correct" required>\n<option value="none">Todos los municipios</option>\n'
        for ele in lista:
            html+='<option value="'+str(ele[0])+'">'+str(ele[0])+'</option>\n'
        html+="</select>\n"
    else:
        html='<select id="municipio_final" name="municipio_final" class="error" required>\n<option value="error">No existen coincidencias en la BDD</option>\n</select>\n'  
    return html


def crea_table(lista):
    tabla="<table>\n"
    tabla+="""
    <thead>\n
    <th>Municipio</th>\n
    <th>Tipo de documento</th>\n
    <th>Soporte</th>\n
    <th>Digital</th>\n
    <th>Año de realización</th>\n
    <th>Escala</th>\n
    <th>Nº de hojas</th>\n
    </thead>\n
    <tbody>\n
    """
    for valor in lista:
        tabla+='<tr onclick=click_tabla("'+str(valor[0])+'")>\n'
        for i in range(1, len(valor)):
            tabla+="<td>"+str(valor[i])+"</td>\n"
        tabla+="</tr>\n"
    tabla+="</tbody>\n</table>"
    return tabla
   
    