# -*- coding: utf-8 -*-

from dweb import dweb
from plantillas import plantillas, formularios

def procesa_opcion_menu(environ):
    """
    Estudia qué opción del menú se ha elegido y genera la página adecuada.
    La primera vez devuelve la página completa. El resto de veces solo
    devuelve la sección principal, que debe ser insertada en el documento
    mediante Ajax.
    """

    titulo=""
    d=dweb.devuelve_dict_get(environ)
    aplicacion=d.get('aplicacion',[''])[0] #Devuelve [''] si no está la llave
    #lo cual significa que es la primera vez que entra

    if aplicacion=="":
        """
        Devuelve la página completa, mostrando el mapa.
        """
        home=plantillas.crea_home()
        html=plantillas.crea_pagina_completa(True, None, home)

    elif  aplicacion=="inicio":
        """
        Le ha vuelto a dar a inicio, por lo que se genera la página con
        el mapa
        """
        home=plantillas.crea_home()
        html=plantillas.crea_seccion_principal(home)

    elif aplicacion=="bgrafica":
        """
        Muestra el mapa y busqueda grafica
        """
        busqueda=formularios.crea_form_busqueda()
        html=plantillas.crea_seccion_principal(busqueda)

    elif aplicacion=="balfa":
        """
        Busqueda alfanumerica
        """
        balfa=formularios.crea_form_balfa()
        html=plantillas.crea_seccion_principal(balfa)

    elif aplicacion=="estadisticas":
        estadisticas=formularios.crea_form_stat_general()
        html=plantillas.crea_seccion_principal(estadisticas)
        
    elif aplicacion=="est_glob":
        stat_general=formularios.crea_form_stat_general()
        html=plantillas.crea_seccion_principal(stat_general)
    
    elif aplicacion=="est_prov":
        stat_prov=formularios.crea_form_stat_prov()
        html=plantillas.crea_seccion_principal(stat_prov)
    
    elif aplicacion=="est_mtp":
        stat_mtp=formularios.crea_form_stat_mtp()
        html=plantillas.crea_seccion_principal(stat_mtp)

    elif aplicacion=="opinion":
        opinion=formularios.crea_form_opinion()
        html=plantillas.crea_seccion_principal(opinion)

    elif aplicacion=="contacto":
        contacto=plantillas.crea_contacto()
        html=plantillas.crea_seccion_principal(contacto)

    elif aplicacion=="ayuda":
        ayuda=plantillas.crea_ayuda()
        html=plantillas.crea_seccion_principal(ayuda)

    else:
        html=plantillas.crea_seccion_principal("Opción incorrecta")

    return html
