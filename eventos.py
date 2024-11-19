import csv
import json
import locale
import os.path
import re
import shutil
import sys
import time
import zipfile
from datetime import datetime
from xml.etree.ElementTree import indent

from PyQt6 import QtWidgets
from PyQt6.uic.Compiler.qtproxies import QtGui
from matplotlib.font_manager import json_dump

import clientes
import conexion
import propiedades
import var
from propiedades import Propiedades

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
        listaprov = conexion.Conexion.listaProv(self)
        cmbProvCli = var.ui.cmbProvCli
        cmbProvProp = var.ui.cmbProvProp
        cmbProvCli.clear()
        cmbProvCli.addItems(listaprov)
        cmbProvProp.clear()
        cmbProvProp.addItems(listaprov)

    @staticmethod
    def cargarMuniCli():
        var.ui.cmbMuniCli.clear()
        listado = conexion.Conexion.listaMunicipios(var.ui.cmbProvCli.currentText())
        var.ui.cmbMuniCli.addItems(listado)

    @staticmethod
    def cargarMuniProp():
        var.ui.cmbMuniProp.clear()
        listado = conexion.Conexion.listaMunicipios(var.ui.cmbProvProp.currentText())
        var.ui.cmbMuniProp.addItems(listado)

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

    def abrirCalendar(self,btn):
        try:
            var.btn = btn
            var.uicalendar.show()
            propiedades.Propiedades.changeRadioProp(self,True)
        except Exception as error:
            print("error en abrir calendar ", error)

    def cargaFecha(qDate):
        try:
            data = ('{:02d}/{:02d}/{:4d}'.format(qDate.day(), qDate.month(), qDate.year()))
            if var.btn == 0:
                var.ui.txtCalendarCli.setText(str(data))
            elif var.btn == 1:
                var.ui.txtBajaCli.setText(str(data))
            elif var.btn == 2:
                var.ui.txtFechaProp.setText(str(data))
            elif var.btn == 3:
                var.ui.txtFechaBajaProp.setText(str(data))
            time.sleep(0.5)
            var.uicalendar.hide()
            return data
        except Exception as error:
            print("error en cargar fecha: ", error)

    def validarMail(self, mail):
        regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w+$'
        return re.match(regex, mail.lower()) or mail == ""

    def resizeTablaClientes(self):
        try:
            header = var.ui.tabClientes.horizontalHeader()
            for i in range(header.count()):
                if i in (1, 2, 4, 5):
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_item = var.ui.tabClientes.horizontalHeaderItem(i)
                font = header_item.font()
                font.setBold(True)
                header_item.setFont(font)

        except Exception as e:
            print("Error en resizeClientes", e)

    def crearBackup(self):
        try:
            copia = str(datetime.now().strftime('%Y_%m_%d_%H_%M_%S')) + '_backup.zip'
            directorio, fichero = var.dlgabrir.getSaveFileName(None, "Guardar Copia Seguridad", copia, ".zip")
            if var.dlgabrir.accept and fichero:
                fichzip = zipfile.ZipFile(fichero, "w")
                fichzip.write("bbdd.sqlite", os.path.basename("bbdd.sqlite"), zipfile.ZIP_DEFLATED)
                fichzip.close()
                shutil.move(fichero, directorio)

                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle('Backup')
                mbox.setText('Backup Creado')
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

    def limpiarPanel(self):
        try:
            if var.ui.panPrincipal.currentIndex() == 0:
                listado = [var.ui.txtDniCli, var.ui.txtCalendarCli,
                           var.ui.txtApelCli, var.ui.txtNomCli,
                           var.ui.txtEmailCli, var.ui.txtMovilCli,
                           var.ui.txtDirCli, var.ui.cmbProvCli, var.ui.cmbMuniCli,
                           var.ui.txtBajaCli]

                for casilla in listado:
                    if isinstance(casilla, QtWidgets.QComboBox):
                        casilla.setCurrentText("")
                    elif isinstance(casilla, QtWidgets.QTextEdit):
                        casilla.setPlainText("")
                    else:
                        casilla.setText("")

                Eventos.cargarProv(self)
                var.ui.cmbMuniCli.clear()
                clientes.Clientes.cargaTablaClientes(self)
                propiedades.Propiedades.cargaTablaPropiedades(self, 0)

            elif var.ui.panPrincipal.currentIndex() == 1:
                listado = [var.ui.lblProp, var.ui.txtFechaProp,
                           var.ui.txtFechaBajaProp, var.ui.txtDirProp,
                           var.ui.cmbProvProp, var.ui.cmbMuniProp,
                           var.ui.cmbTipoProp, var.ui.spinHabProp, var.ui.spinBanosProp,
                           var.ui.txtSuperProp, var.ui.txtPrecioAlquilerProp, var.ui.txtPrecioVentaProp,
                           var.ui.txtCPProp, var.ui.areatxtDescripProp, var.ui.chkAlquilerProp,
                           var.ui.chkIntercambioProp, var.ui.chkVentaProp, var.ui.rbtEstadoDisponibleProp,
                           var.ui.rbtEstadoAlquiladoProp, var.ui.rbtEstadoVendidoProp, var.ui.txtNomeProp,
                           var.ui.txtMovilProp]

                for casilla in listado:
                    if isinstance(casilla, QtWidgets.QComboBox):
                        casilla.setCurrentText("")
                    elif isinstance(casilla, QtWidgets.QCheckBox):
                        casilla.setChecked(False)
                    elif isinstance(casilla, QtWidgets.QRadioButton):
                        var.ui.rbtEstadoDisponibleProp.setChecked(True)
                    elif isinstance(casilla, QtWidgets.QSpinBox):
                        casilla.setValue(0)
                    elif isinstance(casilla, QtWidgets.QTextEdit):
                        casilla.setPlainText("")
                    else:
                        casilla.setText("")

                Eventos.cargarProv(self)
                var.ui.cmbMuniCli.clear()
                clientes.Clientes.cargaTablaClientes(self)
                propiedades.Propiedades.cargaTablaPropiedades(self, 0)

        except Exception as error:
            print("Error en limpiar panel: ", error)

    def validarTelefono(telefono):
        try:
            regex = r'^[6-7]\d{8}$'
            if re.match(regex, telefono):
                return True
            else:
                return False
        except Exception as error:
            print("error en validar telefono: ", error)
            return False

    def abrirTipoProp(self):
        try:
            var.dlgGestion.show()
        except Exception as error:
            print("error en abrir tipo propiedades: ", error)

    def cargarTipoPropiedad(self):
        try:
            registro = conexion.Conexion.cargarTipoPropiedad(self)
            if registro:
                var.ui.cmbTipoProp.clear()
                var.ui.cmbTipoProp.addItems(registro)
        except Exception as error:
            print("Error en cargar tipo propiedad: ", error)

    def resizeTablaPropiedades(self):
        try:
            header = var.ui.tabPropiedades.horizontalHeader()
            for i in range(header.count()):
                if i == 1 or i == 2:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)
                else:
                    header.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.ResizeToContents)
                header_items = var.ui.tabPropiedades.horizontalHeaderItem(i)
                font = header_items.font()
                font.setBold(True)
                header_items.setFont(font)
        except Exception as e:
            print("error en resize tabla propiedades: ", e)

    def exportCSVProp(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "DatosPropiedades.csv")
            directorio,fichero = var.dlgabrir.getSaveFileName(None,"Exporta Datos en CSV", file,'.csv')
            if fichero:
                historicoGuardar = var.historico
                var.historico = 0
                registros = conexion.Conexion.listadoPropiedades(self)
                var.historico = historicoGuardar
                with open(fichero,"w",newline="",encoding="utf-8") as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(["Codigo","Alta","Baja","Direccion","Provincia","Municipio","Tipo"
                                     ,"Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra",
                                     "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"])
                    for registro in registros:
                        writer.writerow(registro)
                shutil.move(fichero,directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.ico"))
                mbox.setWindowTitle('Error')
                mbox.setText('Error en la exportacion de csv')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print(e)

    def exportJSONProp(self):
        try:
            fecha = datetime.today()
            fecha = fecha.strftime('%Y_%m_%d_%H_%M_%S')
            file = str(fecha + "DatosPropiedades.json")
            directorio,fichero = var.dlgabrir.getSaveFileName(None,"Exporta Datos en JSON", file,'.json')
            if fichero:
                keys = ["Codigo","Alta","Baja","Direccion","Provincia","Municipio","Tipo"
                                 ,"Nº Habitaciones", "Nº Baños", "Superficie", "Precio Alquiler", "Precio Compra",
                                 "Codigo Postal", "Observaciones", "Operacion", "Estado", "Propietario", "Movil"]
                historicoGuardar = var.historico
                var.historico = 0
                registros = conexion.Conexion.listadoPropiedades(self)
                var.historico = historicoGuardar
                listapropiedades = [dict(zip(keys,registro)) for registro in registros]
                with open(fichero,"w",newline="",encoding="utf-8") as jsonfile:
                    json.dump(listapropiedades, jsonfile, ensure_ascii=False, indent = 4)
                shutil.move(fichero,directorio)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowIcon(QtGui.QIcon("./img/logo.ico"))
                mbox.setWindowTitle('Error')
                mbox.setText('Error en la exportacion de json')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print(e)