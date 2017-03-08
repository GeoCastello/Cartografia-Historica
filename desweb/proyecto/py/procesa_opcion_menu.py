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
        seccion=plantillas.crea_seccion_principal(home)

        html=seccion

    elif aplicacion=="bgrafica":
        """
        Datos de los pozos sin el mapa
        """

        busqueda=formularios.crea_form_busqueda()
        seccion=plantillas.crea_seccion_principal(busqueda)

        html=seccion


    elif aplicacion=="balfa":
        """
        Datos de los tubos sin el mapa
        """

        balfa=formularios.crea_form_balfa()
        seccion=plantillas.crea_seccion_principal(balfa)

        html=seccion

    elif aplicacion=="opinion":

        opinion=formularios.crea_form_opinion()
        seccion=plantillas.crea_seccion_principal(opinion)

        html=seccion

    else:
        html=plantillas.crea_seccion_principal("Opción incorrecta")

    return html






















