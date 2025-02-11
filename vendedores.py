from datetime import datetime
from multiprocessing.resource_tracker import register

from PyQt6 import QtWidgets, QtGui, QtCore, QtSql

import conexion
import eventos
import var

from datetime import datetime


class Vendedores():

    def altaVendedor(self):
        nuevoVen = [var.ui.txtNombreVen.text(), var.ui.txtDniVen.text(),
                     var.ui.cmbProvVen.currentText(), var.ui.txtMovilVen.text(),
                     var.ui.txtFechaVen.text(), var.ui.txtEmailVen.text()]

        mensajes_error = [
            "Falta ingresar el Nombre",
            "Falta ingresar el DNI",
            "Falta seleccionar provincia",
            "Falta ingresar el movil",
            None,
            None
        ]

        for i, dato in enumerate(nuevoVen):
            if dato == '' and i < 4:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en los datos")
                mbox.setText(mensajes_error[i])
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

        try:
            existeDNI = conexion.Conexion.datosOneVendedorDNI(self, nuevoVen[1])
            if existeDNI:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('Error al insertar el Vendedor. DNI Repetido.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            elif conexion.Conexion.altaVen(self,nuevoVen):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Aviso")
                mbox.setText("Se ha insertado el vendedor correctamente.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Vendedores.cargaTablaVendedores(self, 0)
        except Exception as e:
            print(e)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText('Error al insertar el Vendedor. Intente nuevamente.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()

    def cargaTablaVendedores(self, contexto):
        try:
            listado = conexion.Conexion.listadoVendedores(self)

            propiedades = listado
            var.ui.tabVendedores.setRowCount(0)

            i = 0

            for registro in propiedades:
                if contexto == 1 and var.ui.txtMovilVen.text() != registro[5]:
                    continue

                var.ui.tabVendedores.setRowCount(i + 1)

                var.ui.tabVendedores.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabVendedores.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tabVendedores.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[5]))
                var.ui.tabVendedores.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[7])))

                var.ui.tabVendedores.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVendedores.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabVendedores.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabVendedores.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1

            if var.ui.tabVendedores.rowCount() == 0:
                return Vendedores.setTablaVaciaVen(self)

        except Exception as e:
            print("Error cargar tabVendedores", e)

    def setTablaVaciaVen(self):
        var.ui.tabVendedores.setRowCount(1)
        var.ui.tabVendedores.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay vendedores"))
        var.ui.tabVendedores.item(0, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        return

    def cargaVendedor(self):
        try:
            fila = var.ui.tabVendedores.selectedItems()
            datos = [dato.text() for dato in fila]
            if(datos[0] == "No hay Vendedores"):
                return
            registro = conexion.Conexion.datosOneVendedor(str(datos[0]))

            listado = [var.ui.lblVen, var.ui.txtDniVen,
                       var.ui.txtNombreVen, var.ui.txtFechaVen,
                       var.ui.txtFechaBajaVen, var.ui.txtMovilVen,
                       var.ui.txtEmailVen, var.ui.cmbProvVen]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLabel):
                    casilla.setText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLineEdit):
                    casilla.setText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))
            var.ui.txtIdVendedorFac.setText(str(registro[0]))
            var.ui.txtVendedorAlq.setText(str(registro[0]))

        except Exception as e:
            print("Error cargar Vendedor", e)

    def cargaVendedorMovil(self):
        try:
            movil = var.ui.txtMovilVen.text()
            if movil == "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText(
                    "Error al buscar el Vendedor, Tienes que poner un movil")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                return

            registro = conexion.Conexion.datosOneVendedorMovil(self,str(movil))
            if not registro:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText(
                    "Error al buscar el Vendedor, No existe este Movil")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                return

            listado = [var.ui.lblVen, var.ui.txtDniVen,
                       var.ui.txtNombreVen, var.ui.txtFechaVen,
                       var.ui.txtFechaBajaVen, var.ui.txtMovilVen,
                       var.ui.txtEmailVen, var.ui.cmbProvVen]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLabel):
                    casilla.setText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLineEdit):
                    casilla.setText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))

            Vendedores.cargaTablaVendedores(self,1)

        except Exception as e:
            print("Error cargar Vendedor", e)


    def modifVen(self):
        try:
            nuevoVen = [var.ui.lblVen.text(),var.ui.txtNombreVen.text(), var.ui.txtDniVen.text(),
                        var.ui.cmbProvVen.currentText(), var.ui.txtMovilVen.text(),
                        var.ui.txtFechaVen.text(), var.ui.txtEmailVen.text()]
            if nuevoVen[0] == "":
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al modificar el Vendedor, Tienes que seleccionar el codigo de un Vendedor con la tabla")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

            elif not conexion.Conexion.datosOneVendedorDNI(self, nuevoVen[2]):
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al modificar el Vendedor, Tiene que existir el DNI")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

            elif conexion.Conexion.modifVen(nuevoVen):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Vendedor modificado correctamente')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al modificar el Vendedor")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

            Vendedores.cargaTablaVendedores(self, 0)

        except Exception as error:
            print("error modificar vendedor", error)


    def bajaVendedor(self):
        try:
            if conexion.Conexion.bajaVendedor(int(var.ui.lblVen.text())):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Vendedor dado de baja correctamente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Vendedores.cargaTablaVendedores(self, 0)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al dar de baja el vendedor")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

        except Exception as error:
            print("Error en baja vendedor: ", error)


    def historicoVen(self):
        try:
            if var.ui.chkHistoricoVen.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            var.paginaVen = 0
            Vendedores.cargaTablaVendedores(self, 0)

        except Exception as error:
            print("Error en historico propiedades: ", error)


    def checkDni(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniVen.setText(str(dni))
            if eventos.Eventos.checkDNI(dni):
                var.ui.txtDniVen.setStyleSheet('background-color: rgb(255,255,220);')
            else:
                var.ui.txtDniVen.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniVen.setText('DNI Invalido')
                var.ui.txtDniVen.setFocus()
        except Exception as error:
            print("Error en validar dni ", error)

    def checkEmail(self,mail):
        try:
            if eventos.Eventos.validarMail(self,str(var.ui.txtEmailVen.text())):
                var.ui.txtEmailVen.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailVen.setText(mail.lower())

            else:
                var.ui.txtEmailVen.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailVen.setText("correo no válido")
                var.ui.txtEmailVen.setFocus()
        except Exception as error:
            print("error check vendedor", error)

    @staticmethod
    def checkTelefono(telefono):
        try:
            if eventos.Eventos.validarTelefono(telefono):
                var.ui.txtMovilVen.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilVen.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilVen.setText("telefono no válido")
                var.ui.txtMovilVen.setFocus()

        except Exception as error:
            print("error check vendedor", error)