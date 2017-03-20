# -*- coding: utf-8 -*-
'''
Created on 31/5/2016

@author: ADRIAN
'''

import os

import sys #librería estandar de python
sys.path.append(r"D:\LiClipse\plugins\org.python.pydev_3.9.2.201502042042\pysrc")

#import pydevd

dir_base=os.path.dirname(__file__)

from dweb import dweb

def crea_form_busqueda():
    """
    Crea el formulario de busqueda alfanumerica
    """
    #pydevd.settrace()
    nom_arch=dir_base+"/html_formularios/formulario_busqueda.html"
    formulario=dweb.leer_archivo(nom_arch)
    return formulario

def crea_form_balfa():
    """
    Crea el formulario de busqueda alfanumerica
    """
    #pydevd.settrace()
    nom_arch=dir_base+"/html_formularios/formulario_balfa.html"
    formulario=dweb.leer_archivo(nom_arch)
    return formulario

def crea_form_opinion():
    """
    Crea el formulario de opiniones
    """
    #pydevd.settrace()
    nom_arch=dir_base+"/html_formularios/formulario_opinion.html"
    formulario=dweb.leer_archivo(nom_arch)
    return formulario

def crea_form_stat_general():
    """
    Crea el formulario de estadisticas generales
    """
    #pydevd.settrace()
    nom_arch=dir_base+"/html_formularios/formulario_est_general.html"
    formulario=dweb.leer_archivo(nom_arch)
    return formulario

def crea_form_stat_prov():
    """
    Crea el formulario de estadisticas por provincia
    """
    #pydevd.settrace()
    nom_arch=dir_base+"/html_formularios/formulario_est_prov.html"
    formulario=dweb.leer_archivo(nom_arch)
    return formulario

def crea_form_stat_mtp():
    """
    Crea el formulario de estadisticas por mtp
    """
    #pydevd.settrace()
    nom_arch=dir_base+"/html_formularios/formulario_est_mtp.html"
    formulario=dweb.leer_archivo(nom_arch)
    return formulario
