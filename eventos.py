import locale
import os.path
import re
import sys
import time
import zipfile
import shutil
from datetime import datetime

from PyQt6 import QtWidgets

import clientes
import conexion
import var

locale.setlocale(locale.LC_MONETARY, 'es_ES.UTF-8')
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Eventos():
    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowTitle('Salir')
        mbox.setText('Desea usted Salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def cargarProv(self):
        cmbProvCli = var.ui.cmbProvCli
        listaprov = conexion.Conexion.listaProv(self)
        cmbProvCli.clear()
        cmbProvCli.addItems(listaprov)

    @staticmethod
    def cargarMuniCli():
        var.ui.cmbMuniCli.clear()
        listado = conexion.Conexion.listaMunicipios(var.ui.cmbProvCli.currentText())
        var.ui.cmbMuniCli.addItems(listado)

    def checkDNI(dni):
        try:
            tabla = "TRWAGMYFPDXBNJZSQVHLCKE"
            dig_ext = "XYZ"
            reemp_dig_ext = {'X': '0', 'Y': '1', 'Z': '2'}
            numeros = "1234567890"
            if len(dni) == 9:
                dig_control = dni[8]
                dni = dni[:8]
                if dni[0] in dig_ext:
                    dni = dni.replace(dni[0], reemp_dig_ext[dni[0]])
                if len(dni) == len([n for n in dni if n in numeros]) and tabla[int(dni) % 23] == dig_control:
                    return True
                else:
                    return False
            else:
                return False
        except Exception as error:
            print("error en validar dni ", error)
            return False

    def abrirCalendar(op):
        try:
            var.panel = op
            var.uicalendar.show()
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.panel == var.ui.panPrincipal.currentIndex():
                var.ui.txtCalendarCli.setText(str(data))
            time.sleep(0.5)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(mail):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.match(regex, mail.lower())

    def resizeTablaClientes(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(header.count()):
                if i in (0,1,3,4):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i,QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_item = var.ui.tabClientes.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)

        except Exception as e:
            print("Error en resizeClientes",e)

    def crearBackup(self):
        try:
            copia = str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '_backup.zip'
            directorio, fichero = var.dlgabrir.getSaveFileName(None,"Guardar Copia Seguridad", copia ,".zip")
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero,"w")
                fichzip.write("bbdd.sqlite", os.path.basename("bbdd.sqlite"), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero,directorio)

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Backup')
                mbox.setText('Base de Datos Creada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

        except Exception as error:
            print("Error en crear backup: ", error)

    def restaurarBackup(self):
        try:
            filename = var.dlgabrir.getOpenFileName(None, "Restaurat Copia Seguridad", "", "*.zip;;All Files(*)")
            file = filename[0]
            if file:
                with zipfile.ZipFile(file, "r") as bbdd:
                    bbdd.extractall(pwd=None)
                bbdd.close()

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Backup')
                mbox.setText('Base de Datos Restaurada')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()

                conexion.Conexion.db_conexion(self)
                Eventos.cargarProv(self)
                clientes.Clientes.cargaTablaClientes(self)

        except Exception as e:
            print(e)
