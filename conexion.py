import os
import sys

from PyQt6 import QtSql, QtWidgets
from PyQt6.uic.Compiler.qtproxies import QtGui


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
            query.prepare("SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as error:
            print("error lista muni: ", error)


    def altaCliente(nuevoCli):
        try:
            query = QtSql.QSqlQuery()
            query.prepare('INSERT INTO clientes (dnicli, altacli, apelcli, nomeCli, emailcli, movilcli, dircli, provcli, municli)'
                          ' VALUES (:dnicli, :altacli, :apelcli, :nomeCli, :emailcli, :movilcli, :dircli, :provcli, :municli)')
            query.bindValue(":dnicli", str(nuevoCli[0]))
            query.bindValue(":altacli", str(nuevoCli[1]))
            query.bindValue(":apelcli", str(nuevoCli[2]))
            query.bindValue(":nomeCli", str(nuevoCli[3]))
            query.bindValue(":emailcli", str(nuevoCli[4]))
            query.bindValue(":movilcli", str(nuevoCli[5]))
            query.bindValue(":dircli", str(nuevoCli[6]))
            query.bindValue(":provcli", str(nuevoCli[7]))
            query.bindValue(":municli", str(nuevoCli[8]))
            if query.exec():
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Cliente dado de alta correctamente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            else:
                print(nuevoCli)
                QtWidgets.QMessageBox.critical(None, 'Error', 'Error al dar de alta el cliente',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
        except Exception as error:
            print("Error en alta cliente: ", error)