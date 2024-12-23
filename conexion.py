import os
import sqlite3
from datetime import datetime

from PyQt6 import QtSql, QtWidgets

import var


class Conexion:
    '''

    método de una clase que no depende de una instancia específica de esa clase. 
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase. 
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    
    '''

    @staticmethod
    def db_conexion(self):
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    @staticmethod
    def listaProv(self):
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare('SELECT * FROM provincias')
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))

        return listaprov

    @staticmethod
    def listaMunicipios(provincia):
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as error:
            print("error lista muni: ", error)

    def altaCliente(self, nuevoCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO CLIENTES (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) "
                " VALUES (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevoCli[0]))
            query.bindValue(":altacli", str(nuevoCli[1]))
            query.bindValue(":apelcli", str(nuevoCli[2]))
            query.bindValue(":nomecli", str(nuevoCli[3]))
            query.bindValue(":emailcli", str(nuevoCli[4]))
            query.bindValue(":movilcli", str(nuevoCli[5]))
            query.bindValue(":dircli", str(nuevoCli[6]))
            query.bindValue(":provcli", str(nuevoCli[7]))
            query.bindValue(":municli", str(nuevoCli[8]))
            if query.exec():
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en alta cliente: ", error)

    def listadoClientes(self):
        try:
            listado = []
            if var.historico == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE bajacli is NULL ORDER BY apelcli, nomecli ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            elif var.historico == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error listado en conexion", e)

    def datosOneCliente(dni):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM CLIENTES WHERE dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos cliente: ", error)

    def modifCliente(registro):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0) > 0:
                    query.prepare("UPDATE clientes set altacli = :altacli, apelcli = :apelcli, nomecli = :nomecli, "
                                  " emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli = :provcli, "
                                  " municli = :municli, bajacli = :bajacli where dnicli = :dni")
                    query.bindValue(":dni", str(registro[0]))
                    query.bindValue(":altacli", str(registro[1]))
                    query.bindValue(":apelcli", str(registro[2]))
                    query.bindValue(":nomecli", str(registro[3]))
                    query.bindValue(":emailcli", str(registro[4]))
                    query.bindValue(":movilcli", str(registro[5]))
                    query.bindValue(":dircli", str(registro[6]))
                    query.bindValue(":provcli", str(registro[7]))
                    query.bindValue(":municli", str(registro[8]))
                    if registro[9] == "":
                        query.bindValue(":bajacli", None)
                    else:
                        query.bindValue(":bajacli", str(registro[9]))
                    query.exec()
                    return query.numRowsAffected() != 0
            return False
        except Exception as error:
            print("error modificar cliente", error)

    def bajaCliente(datos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE clientes set bajacli = :bajacli WHERE dnicli = :dnicli")
            query.bindValue(":bajacli", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":dnicli", str(datos[1]))
            query.exec()
            return query.numRowsAffected() != 0
        except Exception as error:
            print("Error en baja cliente: ", error)

    """
    -------------------- GESTION PROPIEDADES --------------------
    """

    def altaTipoPropiedad(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO tipoPropiedad (tipo) VALUES (:tipo)")
            query.bindValue(":tipo", tipo)
            return query.exec()
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)

    def bajaTipoPropiedad(tipo):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM tipoPropiedad WHERE tipo = :tipo")
            query.bindValue(":tipo", tipo)
            return query.exec()
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    def cargarTipoPropiedad(self):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo FROM tipoPropiedad")
            registro = []
            if query.exec():
                while query.next():
                    registro.append(query.value(0))
            return registro
        except Exception as error:
            print("Error en cargar tipo propiedad: ", error)

    def altaPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                " INSERT into PROPIEDADES (altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, "
                " superprop, prealquiprop, prevenprop, cpprop, obserprop, tipooper, estadoprop, nomeprop, movilprop) "
                " VALUES (:altaprop, :dirprop, :provprop, :muniprop, :tipoprop, :habprop, :banprop, :superprop, "
                " :prealquiprop, :prevenprop, :cpprop, :obserprop, :tipooper, :estadoprop, :nomeprop, :movilprop)")
            query.bindValue(":altaprop", str(propiedad[0]))
            query.bindValue(":dirprop", str(propiedad[1]))
            query.bindValue(":provprop", str(propiedad[2]))
            query.bindValue(":muniprop", str(propiedad[3]))
            query.bindValue(":tipoprop", str(propiedad[4]))
            query.bindValue(":habprop", int(propiedad[5]))
            query.bindValue(":banprop", int(propiedad[6]))
            query.bindValue(":superprop", float(propiedad[7]))
            query.bindValue(":prealquiprop", float(propiedad[8]))
            query.bindValue(":prevenprop", float(propiedad[9]))
            query.bindValue(":cpprop", str(propiedad[10]))
            query.bindValue(":obserprop", str(propiedad[11]))
            query.bindValue(":tipooper", str(propiedad[14]))
            query.bindValue(":estadoprop", str(propiedad[15]))
            query.bindValue(":nomeprop", str(propiedad[12]))
            query.bindValue(":movilprop", str(propiedad[13]))
            return query.exec()

        except Exception as e:
            print("error altaPropiedad en conexion", e)

    def listadoPropiedades(self):
        try:
            listado = []
            queryStr = ""
            if var.historico == 1:
                queryStr = "SELECT * FROM propiedades WHERE bajaprop is NULL ORDER BY muniprop ASC "

            elif var.historico == 0:
                queryStr = "SELECT * FROM propiedades ORDER BY muniprop ASC "

            query = QtSql.QSqlQuery()
            query.prepare(queryStr)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listado en conexion", e)

    def datosOnePropiedad(codigo):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos datosOnePropiedad: ", error)

    def bajaPropiedad(datos):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET bajaprop = :bajaprop WHERE codigo = :codigo")
            query.bindValue(":bajaprop", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":codigo", datos)
            return query.exec()
        except Exception as error:
            print("Error en baja propiedad: ", error)

    def modifPropiedad(propiedad):
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT count(*) FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", int(propiedad[0]))
            if query.exec() and query.next() and query.value(0) > 0:
                query.prepare(
                    "UPDATE propiedades SET altaprop = :altaprop, dirprop = :dirprop, provprop = :provprop, "
                    "muniprop = :muniprop, tipoprop = :tipoprop, habprop = :habprop, banprop = :banprop, "
                    "superprop = :superprop, prealquiprop = :prealquiprop, prevenprop = :prevenprop, cpprop = :cpprop, "
                    "obserprop = :obserprop, tipooper = :tipooper, estadoprop = :estadoprop, nomeprop = :nomeprop, "
                    "movilprop = :movilprop WHERE codigo = :codigo"
                )
                query.bindValue(":altaprop", str(propiedad[1]))
                query.bindValue(":dirprop", str(propiedad[2]))
                query.bindValue(":provprop", str(propiedad[3]))
                query.bindValue(":muniprop", str(propiedad[4]))
                query.bindValue(":tipoprop", str(propiedad[5]))
                query.bindValue(":habprop", int(propiedad[6]))
                query.bindValue(":banprop", int(propiedad[7]))
                query.bindValue(":superprop", float(propiedad[8]))
                query.bindValue(":prealquiprop", float(propiedad[9]))
                query.bindValue(":prevenprop", float(propiedad[10]))
                query.bindValue(":cpprop", str(propiedad[11]))
                query.bindValue(":obserprop", str(propiedad[12]))
                query.bindValue(":tipooper", str(propiedad[13]))
                query.bindValue(":estadoprop", str(propiedad[14]))
                query.bindValue(":nomeprop", str(propiedad[15]))
                query.bindValue(":movilprop", str(propiedad[16]))
                query.bindValue(":codigo", int(propiedad[0]))

                return query.exec()
            return False
        except Exception as error:
            print("Error modificar propiedad", error)