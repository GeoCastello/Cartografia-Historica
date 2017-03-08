# -*- coding: utf-8 -*-
'''
Created on 31/5/2016

@author: ADRIAN
'''

from plantillas import plantillas
from dweb import dweb
import psycopg2
import psycopg2.extensions
psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
import sys
import json
import time
sys.path.append(r"D:\LiClipse\plugins\org.python.pydev_3.9.2.201502042042\pysrc")
#import pydevd

class procesar_formularios():
    """
    Clase que procesa los formularios recibidos
    """

    #variables de la clase
    environ=None
    nombre_form=None
    dpost=None

    def __init__(self, environ):
        """
        Constructor. Recibe el parámetro environ e inicializa las variables
        de la clase
        """
        #pydevd.settrace()
        self.environ=environ
        self.dpost=dweb.devuelve_dict_post(environ)
        self.nombre_form=self.dpost["nombre-form"][0]

    def procesa_formulario(self):
        """
        Estudia que formulario ha sido enviado y realiza la acción necesaria
        """
        #pydevd.settrace()
        if self.nombre_form=="formulario_busqueda":
            #aquí no esta si la sesión ya se ha iniciado
            self.conexion()
            html=self.procesa_form_busqueda()

        elif self.nombre_form=="formulario_alfa":
            self.conexion()
            html=self.procesa_form_balfa()

        elif self.nombre_form=="formulario_opinion":
            self.conexion()
            html=self.procesa_form_opinion()

        elif self.nombre_form=="click_tabla":
            self.conexion()
            html=self.procesa_click_tabla()

        elif self.nombre_form=="click_mapa":
            self.conexion()
            html=self.procesa_click_mapa()


        else:
            tit="No se ha programado nada para el formulario {}".format(self.nombre_form)
            html=plantillas.crea_seccion_principal(tit)

        return html

    def procesa_form_busqueda(self):
        self.type=self.dpost["type-form"][0]


        ##PROCESO PARA C_AUTONOMA------------------------------------------------------------------------------------------------------
        if self.type=="c_autonoma":
            accion='Zoom a Comunidad Autónoma'
            #pydevd.settrace()
            where="WHERE "
            if "com_aut" in self.dpost.keys():
                if self.dpost["com_aut"][0]!='none':
                    self.com_aut=self.dpost["com_aut"][0]
                    where+=" UPPER(nameunit) =  UPPER('"+ str(self.com_aut)+"')"
                    sql= 'SELECT ST_AsGeoJSON(ST_Extent(geom)) from cch.autonomias '+where+";"
                    self.cursor.execute(sql)
                    result=self.cursor.fetchall()
                    if result!=[]:
                        extension=result[0][0]
                        self.inserta_registro(accion, sql)
                    else:
                        extension='null'
                    json_resp=json.dumps({"seccion":"c_autonoma", "extension": extension})
                    html=json_resp
                else:
                    self.com_aut="vacio"
            else:
                self.com_aut="vacio"



        ##PROCESO PARA PROV------------------------------------------------------------------------------------------------------
        elif self.type=="prov":
            accion='Zoom a Provincia'
            where="WHERE "
            if "provincia" in self.dpost.keys():
                if self.dpost["provincia"][0]!='none':
                    self.provincia=self.dpost["provincia"][0]
                    where+=" UPPER(nameunit) = UPPER('"+ str(self.provincia)+"')"
                    sql= 'SELECT ST_AsGeoJSON(ST_Extent(geom)) from cch.provincias '+where+";"
                    self.cursor.execute(sql)
                    result=self.cursor.fetchall()
                    if result!=[]:
                        extension=result[0][0]
                        self.inserta_registro(accion, sql)
                    else:
                        extension='null'
                    extension=result[0][0]
                    json_resp=json.dumps({"seccion":"prov", "extension": extension})
                    html=json_resp
                else:
                    self.provincia="vacio"
            else:
                self.provincia="vacio"


        ##PROCESO PARA SEND y SEARCH------------------------------------------------------------------------------------------------------
        elif self.type=="send" or self.type=="search":
            where="WHERE "
            if "com_aut" in self.dpost.keys():
                if self.dpost["com_aut"][0]!='none':
                    self.com_aut=self.dpost["com_aut"][0]
                else:
                    self.com_aut="vacio"
            else:
                self.com_aut="vacio"

            if "provincia" in self.dpost.keys():
                if self.dpost["provincia"][0]!='none':
                    self.provincia=self.dpost["provincia"][0]
                else:
                    self.provincia="vacio"
            else:
                self.provincia="vacio"

            if self.dpost["tipo_doc"][0]!='none':
                self.tipo_doc=self.dpost["tipo_doc"][0]
                if where=="WHERE ":
                    where+=" UPPER(tipo_de_documento) = UPPER('"+self.tipo_doc+"') "
                else:
                    where+=" AND UPPER(tipo_de_documento) = UPPER('"+self.tipo_doc+"') "
            else:
                self.tipo_doc="vacio"

            #PROCESO PARA SEND-------------------------------------------------------------------------------------------------------
            if self.type=="send":
                accion='Búsqueda de cartografía histórica'
                limite='none'
                variables= "c_ine, nombre_mun, tipo_de_documento, tipo_de_soporte, formato_digital, anyo_ejecucion, escala, numero_hojas"
                if self.dpost["municipio_final"][0]!='none':
                    self.municipio_final=self.dpost["municipio_final"][0]
                    if where=="WHERE ":
                        where+=" UPPER(nombre_mun) = UPPER('"+self.municipio_final+"') "
                    else:
                        where+=" AND UPPER(nombre_mun) = UPPER('"+self.municipio_final+"') "
                else:
                    self.municipio_final="vacio"
                if where=="WHERE ":
                    limite="No se ha introducido ningún municipio en la búsqueda, por lo tanto, solamente se muestran los primeros 100 resultados de las tablas urbana y rústica."
                    where="LIMIT 100 "
                else:
                    where2=where
                    limite="La búsqueda realizada es muy genérica, por lo tanto, solamente se muestran los primeros 1000 resultados de la búsqueda."
                    where+= "LIMIT 1000 "

                sql_rustica="SELECT "+ variables +" FROM cch.rustica "+where+";"
                sql_urbana="SELECT "+ variables +" FROM cch.urbana "+where+";"
                self.cursor.execute(sql_rustica)
                lista_rus=self.cursor.fetchall()
                self.cursor.execute(sql_urbana)
                lista_urb=self.cursor.fetchall()
                if where!="LIMIT 100 ":
                    if len(lista_rus)<1000 and len(lista_urb)<1000:
                        limite="none"
                self.inserta_registro(accion+' de rústica', sql_rustica)
                self.inserta_registro(accion+' de urbana', sql_urbana)
                tabla_rus=plantillas.crea_table(lista_rus)
                tabla_urb=plantillas.crea_table(lista_urb)
                html_seccion=plantillas.crea_seccion_tablas(tabla_rus, tabla_urb)
                if where=="LIMIT 100 ":
                    where=""
                else:
                    where=where2
                accion='Zoom a Municipios'
                sql="SELECT c_ine FROM cch.rustica "+where+" UNION DISTINCT SELECT c_ine FROM cch.urbana "+where+";"
                self.cursor.execute(sql)
                list=self.cursor.fetchall()
                if list!=[]:
                    sql_extension= self.sql_extension(list)
                    self.cursor.execute(sql_extension)
                    result=self.cursor.fetchall()
                    extension=result[0][0]
                    self.inserta_registro(accion, sql_extension)
                else:
                    extension="null"
                json_resp=json.dumps({"seccion":"#tablas", "limite": limite, "html": html_seccion, "extension": extension})
                html=json_resp

            #PROCESO PARA SEARCH------------------------------------------------------------------------------------------------------
            elif self.type=="search":
                accion='Búsqueda de municipios'
                if "municipio" in self.dpost.keys():
                    self.municipio=self.dpost["municipio"][0]
                    if where=="WHERE ":
                        where+=" UPPER(nombre_mun) LIKE UPPER('%"+self.municipio+"%') "
                    else:
                        where+=" AND UPPER(nombre_mun) LIKE UPPER('%"+self.municipio+"%') "
                else:
                    self.municipio="vacio"
                if where=="WHERE ":
                    where=""
                sql="SELECT nombre_mun FROM cch.rustica "+where+" UNION DISTINCT SELECT nombre_mun FROM cch.urbana "+where+";"
                self.cursor.execute(sql)
                lista=self.cursor.fetchall()
                self.inserta_registro(accion, sql)
                html_seccion=plantillas.crea_muni(lista)
                json_resp=json.dumps({"seccion":"#municipio_final", "html": html_seccion, "extension": "null"})
                html=json_resp

        return html

    def procesa_form_balfa(self):
        self.type=self.dpost["type-form"][0]

        ##PROCESO PARA SEND y SEARCH------------------------------------------------------------------------------------------------------
        if self.type=="send" or self.type=="search":
            where="WHERE "
            if "tipo_urbana" in self.dpost.keys():
                self.urbana=True
            else:
                self.urbana=False

            if "tipo_rustica" in self.dpost.keys():
                self.rustica=True
            else:
                self.rustica=False

            if "formato_digital" in self.dpost.keys() and "formato_papel" not in self.dpost.keys():
                self.digital=True
                self.papel=False
                if where=="WHERE ":
                    where+=" UPPER(formato_digital) = UPPER('Sí') "
                else:
                    where+=" AND UPPER(formato_digital) = UPPER('Sí') "

            elif "formato_digital" not in self.dpost.keys() and "formato_papel" in self.dpost.keys():
                self.digital=False
                self.papel=True
                if where=="WHERE ":
                    where+=" (formato_digital IS NULL or UPPER(formato_digital) ='NO')"
                else:
                    where+=" AND (formato_digital IS NULL or UPPER(formato_digital) ='NO')"

            elif "formato_digital" not in self.dpost.keys() and "formato_papel"not in self.dpost.keys():
                self.digital=False
                self.papel=False
            else:
                self.digital=True
                self.papel=True

            if self.dpost["tipo_doc"][0]!='none':
                self.tipo_doc=self.dpost["tipo_doc"][0]
                if where=="WHERE ":
                    where+=" UPPER(tipo_de_documento) = UPPER('"+self.tipo_doc+"') "
                else:
                    where+=" AND UPPER(tipo_de_documento) = UPPER('"+self.tipo_doc+"') "
            else:
                self.tipo_doc="vacio"


            #PROCESO PARA SEARCH-------------------------------------------------------------------------------------------------------
            if self.type=="search":
                accion='Búsqueda de municipios'
                if "municipio" in self.dpost.keys():
                    self.municipio=self.dpost["municipio"][0]
                    if where=="WHERE ":
                        where+=" UPPER(nombre_mun) LIKE UPPER('%"+self.municipio+"%') "
                    else:
                        where+=" AND UPPER(nombre_mun) LIKE UPPER('%"+self.municipio+"%') "
                else:
                    self.municipio="vacio"
                if where=="WHERE ":
                    where=""
                if self.rustica and not self.urbana:
                    sql="SELECT DISTINCT nombre_mun FROM cch.rustica "+where+";"
                elif self.urbana and not self.rustica:
                    sql="SELECT DISTINCT nombre_mun FROM cch.urbana "+where+";"
                elif not self.rustica and not self.urbana:
                    sql="SELECT nombre_mun FROM cch.rustica "+where+" UNION DISTINCT SELECT nombre_mun FROM cch.urbana "+where+";"
                else:
                    sql="SELECT nombre_mun FROM cch.rustica "+where+" UNION DISTINCT SELECT nombre_mun FROM cch.urbana "+where+";"
                self.cursor.execute(sql)
                lista=self.cursor.fetchall()
                self.inserta_registro(accion, sql)
                html_seccion=plantillas.crea_muni(lista)
                json_resp=json.dumps({"seccion":"#municipio_final", "html": html_seccion, "extension": "null"})
                html=json_resp

            #PROCESO PARA SEND-------------------------------------------------------------------------------------------------------
            elif self.type=="send":
                accion='Búsqueda de cartografía histórica'
                limite="none"
                variables= "c_ine, nombre_mun, tipo_de_documento, tipo_de_soporte, formato_digital, anyo_ejecucion, escala, numero_hojas"
                if self.dpost["municipio_final"][0]!='none':
                    self.municipio_final=self.dpost["municipio_final"][0]
                    if where=="WHERE ":
                        where+=" UPPER(nombre_mun) = UPPER('"+self.municipio_final+"') "
                    else:
                        where+=" AND UPPER(nombre_mun) = UPPER('"+self.municipio_final+"') "
                else:
                    self.municipio_final="vacio"
                if where=="WHERE ":
                    limite="No se ha introducido ningún critero de búsqueda, por lo tanto, solamente se muestran los primeros 100 resultados"
                    if self.rustica and not self.urbana:
                        limite+=" de la tabla de rustíca."
                    elif self.urbana and not self.rustica:
                        limite+=" de la tabla de urbana."
                    else:
                        limite+=" de las tablas urbana y rústica."
                    where="LIMIT 100 "
                else:
                    where2=where
                    limite="La búsqueda realizada es muy genérica, por lo tanto, solamente se muestran los primeros 1000 resultados de la búsqueda."
                    where+= "LIMIT 1000 "

                if self.rustica and not self.urbana:
                    sql_rustica="SELECT "+ variables +" FROM cch.rustica "+where+";"
                    self.cursor.execute(sql_rustica)
                    lista_rus=self.cursor.fetchall()
                    self.inserta_registro(accion+' de rústica', sql_rustica)
                    if where!="LIMIT 100 ":
                        if len(lista_rus)<1000:
                            limite="none"
                    tabla_rus=plantillas.crea_table(lista_rus)
                    html_seccion=plantillas.crea_seccion_tablas(tabla_rus, None)
                    sql="SELECT DISTINCT c_ine FROM cch.rustica "+where+";"
                elif self.urbana and not self.rustica:
                    sql_urbana="SELECT "+ variables +" FROM cch.urbana "+where+";"
                    self.cursor.execute(sql_urbana)
                    lista_urb=self.cursor.fetchall()
                    self.inserta_registro(accion+' de urbana', sql_urbana)
                    if where!="LIMIT 100 ":
                        if len(lista_urb)<1000:
                            limite="none"
                    tabla_urb=plantillas.crea_table(lista_urb)
                    html_seccion=plantillas.crea_seccion_tablas(None, tabla_urb)
                    sql="SELECT DISTINCT c_ine FROM cch.urbana "+where+";"
                else:
                    sql_rustica="SELECT "+ variables +" FROM cch.rustica "+where+";"
                    sql_urbana="SELECT "+ variables +" FROM cch.urbana "+where+";"
                    self.cursor.execute(sql_rustica)
                    lista_rus=self.cursor.fetchall()
                    self.inserta_registro(accion+' de rústica', sql_rustica)
                    self.cursor.execute(sql_urbana)
                    lista_urb=self.cursor.fetchall()
                    self.inserta_registro(accion+' de urbana', sql_urbana)
                    if where!="LIMIT 100 ":
                        if len(lista_rus)<1000 and len(lista_urb)<1000:
                            limite="none"
                    tabla_rus=plantillas.crea_table(lista_rus)
                    tabla_urb=plantillas.crea_table(lista_urb)
                    html_seccion=plantillas.crea_seccion_tablas(tabla_rus, tabla_urb)
                    if where=="LIMIT 100 ":
                        where=""
                    else:
                        where=where2
                    sql="SELECT c_ine FROM cch.rustica "+where+" UNION DISTINCT SELECT c_ine FROM cch.urbana "+where+";"

                self.cursor.execute(sql)
                list=self.cursor.fetchall()
                if list!=[]:
                    sql_extension= self.sql_extension(list)
                    self.cursor.execute(sql_extension)
                    result=self.cursor.fetchall()
                    accion='Zoom a Municipios'
                    self.inserta_registro(accion, sql_extension)
                    extension=result[0][0]
                else:
                    extension="null"
                json_resp=json.dumps({"seccion":"#tablas", "limite": limite, "html": html_seccion, "extension": extension})
                html=json_resp
        return html

    def procesa_form_opinion(self):
        if "nombre" in self.dpost.keys():
            nombre=self.dpost["nombre"][0]
        else:
            nombre="Anónimo"
        if "apellido" in self.dpost.keys():
            apellidos=self.dpost["apellido"][0]
        else:
            apellidos="Anónimo"
        titulacion=self.dpost["tipo_titulacion"][0]
        trabajo=self.dpost["tipo_trabajo"][0]
        opinion=self.dpost["utilidad"][0]
        if "mejoras" in self.dpost.keys():
            mejoras=self.dpost["mejoras"][0]
        else:
            mejoras="Sin sugerencias"
        sql_ins="INSERT INTO  soporte.opinion (ip, fecha, nombre, apellidos, titulacion, trabajo, opinion, mejoras) VALUES ('"+self.environ['REMOTE_ADDR']+"', to_timestamp('"+time.strftime('%c')+"','MM/DD/YY HH24:MI:SS'), '"+nombre+"', '"+apellidos+"', '"+titulacion+"', '"+trabajo+"', '"+opinion+"', '"+mejoras+"');"
        self.cursor.execute(sql_ins)
        self.conn.commit()
        json_resp=json.dumps({"seccion":"#reg_opinion", "mensaje": "Tu opinión ha sido enviada correctamente", "extension": "null"})
        html=json_resp
        return html

    def procesa_click_tabla(self):
        accion='Zoom a Municipios'
        cod_ine=self.dpost["result"][0]
        where="WHERE ine = '"+ str(cod_ine)+"'"
        sql= 'SELECT ST_AsGeoJSON(ST_Extent(geom)) from cch.municipios '+where+";"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        if result!=[]:
            self.inserta_registro(accion, sql)
            extension=result[0][0]
        else:
            extension='null'
        json_resp=json.dumps({"seccion":"click_tabla", "extension": extension})
        html=json_resp
        return html

    def procesa_click_mapa(self):
        accion='Selección de Municipio'
        lat=self.dpost["lat"][0]
        lon=self.dpost["lon"][0]
        where="WHERE St_intersects(geom, ST_GeometryFromText('POINT ("+str(lon)+" "+str(lat)+")', 4258))"
        sql= 'SELECT ine from cch.municipios '+where+";"
        self.cursor.execute(sql)
        result=self.cursor.fetchall()
        if result!=[]:
            self.inserta_registro(accion, sql)
            accion='Búsqueda de cartografía histórica'
            cod_ine=result[0][0]
            variables= "c_ine, nombre_mun, tipo_de_documento, tipo_de_soporte, formato_digital, anyo_ejecucion, escala, numero_hojas"
            where="WHERE c_ine ="+ str(cod_ine)
            sql_rustica="SELECT "+ variables +" FROM cch.rustica "+where+";"
            sql_urbana="SELECT "+ variables +" FROM cch.urbana "+where+";"
            self.cursor.execute(sql_rustica)
            lista_rus=self.cursor.fetchall()
            self.inserta_registro(accion+' de rústica', sql_rustica)
            self.cursor.execute(sql_urbana)
            lista_urb=self.cursor.fetchall()
            self.inserta_registro(accion+' de urbana', sql_urbana)
            tabla_rus=plantillas.crea_table(lista_rus)
            tabla_urb=plantillas.crea_table(lista_urb)
            html_seccion=plantillas.crea_seccion_tablas(tabla_rus, tabla_urb)
            where="WHERE ine = '"+ str(cod_ine)+"'"
            sql= 'SELECT ST_AsGeoJSON(ST_Extent(geom)) from cch.municipios '+where+";"
            self.cursor.execute(sql)
            result=self.cursor.fetchall()
            if result!=[]:
                self.inserta_registro('Zoom a Municipios', sql)
                extension=result[0][0]
            else:
                extension='null'
            json_resp=json.dumps({"seccion":"#tablas", "html": html_seccion, "extension": extension})
            html=json_resp
        else:
            json_resp=json.dumps({"seccion":"Error", "extension": "null"})
            html=json_resp
        return html

    def conexion(self):
        self.database='cch'
        self.user='postgres'
        self.password='postgres'
        self.host='localhost'
        self.port=5432
        self.conn=psycopg2.connect(database=self.database, user=self.user, password=self.password, host=self.host, port=self.port)
        self.cursor=self.conn.cursor()

    def inserta_registro(self, accion, sql):
        cons_ins="INSERT INTO  soporte.rec_activ (ip, fecha, accion, sql, tipo_form) VALUES ('"+self.environ['REMOTE_ADDR']+"', to_timestamp('"+time.strftime('%c')+"','MM/DD/YY HH24:MI:SS'), '"+accion+"', '"+sql.replace("'","''")+"', '"+self.nombre_form+"');"
        self.cursor.execute(cons_ins)
        self.conn.commit()

    def sql_extension(self, lista):
        where="WHERE "
        for element in lista:
            if where =="WHERE ":
                where+=" ine="+str(element[0]).replace("None", "NULL")+" "
            else:
                where+=" OR ine="+str(element[0]).replace("None", "NULL")+" "
        return 'SELECT ST_AsGeoJSON(ST_Extent(geom)) from cch.municipios '+where+";"