import sqlite3

from PyQt6 import QtWidgets, QtGui, QtCore

import clientes
import conexion
import eventos
import var


class Clientes:

    def altaCliente(self):
        nuevoCli = [var.ui.txtDniCli.text(), var.ui.txtCalendarCli.text(),
                    var.ui.txtApelCli.text(), var.ui.txtNomCli.text(),
                    var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                    var.ui.txtDirCli.text(),
                    var.ui.cmbProvCli.currentText(),
                    var.ui.cmbMuniCli.currentText()]
        mensajes_error = [
            "Falta ingresar DNI",
            "Falta ingresar fecha de alta",
            "Falta ingresar apellido",
            "Falta ingresar nombre",
            None,
            "Falta ingresar móvil",
            "Falta ingresar dirección",
            "Falta seleccionar provincia",
            "Falta seleccionar municipio"
        ]

        for i, dato in enumerate(nuevoCli):
            if i == 4:  # Saltamos la validación para el email (índice 4)
                continue
            if dato == '':
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en los datos")
                mbox.setText(mensajes_error[i])
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return
        try:
            if conexion.Conexion.altaCliente(self, nuevoCli):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Aviso")
                mbox.setText("Se ha insertado el cliente correctamente.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Clientes.cargaTablaClientes(self)
        except Exception as e:
            print(e)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText('Error al insertar el cliente. Intente nuevamente.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()

    def checkDni(dni):
        try:
            dni = str(dni).upper()
            var.ui.txtDniCli.setText(str(dni))
            if eventos.Eventos.checkDNI(dni):
                var.ui.txtDniCli.setStyleSheet('background-color: rgb(255,255,220);')
            else:
                var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniCli.setText('DNI Invalido')
                var.ui.txtDniCli.setFocus()
        except Exception as error:
            print("Error en validar dni ", error)

    def checkEmail(mail):
        try:
            if eventos.Eventos.validarMail(str(var.ui.txtEmailCli.text())):
                var.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailCli.setText(mail.lower())

            else:
                var.ui.txtEmailCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailCli.setText("correo no válido")
                var.ui.txtEmailCli.setFocus()
        except sqlite3.IntegrityError as e:
            print("Error, ya existe el dni: ", e)
        except Exception as error:
            print("error check cliente", error)

    def cargaTablaClientes(self):
        try:
            listado = conexion.Conexion.listadoClientes(self)
            var.ui.tabClientes.setRowCount(0)
            i = 0
            pagina = []
            paginas = []
            for cliente in listado:
                if i > 14:
                    i = 0
                    paginas.append(pagina)
                    pagina = []
                else:
                    pagina.append(cliente)
                    i += 1

            if pagina != []:
                paginas.append(pagina)

            var.ui.btnSiguienteCli.setDisabled(True)
            var.ui.btnAnteriorCli.setDisabled(True)

            if len(paginas) < var.paginaCli + 1:
                if var.paginaCli == 0:
                    return Clientes.setTablaVaciaCli(self)
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Aviso")
                mbox.setText("No puedes estar en una pagina vacia")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                var.paginaCli -= 1
                Clientes.cargaTablaClientes(self)
                return

            if len(paginas)  >=  var.paginaCli +2:
                var.ui.btnSiguienteCli.setDisabled(False)


            if var.paginaCli > 0:
                var.ui.btnAnteriorCli.setDisabled(False)


            clientes = paginas[var.paginaCli]

            for i, registro in enumerate(clientes):
                var.ui.tabClientes.setRowCount(i + 1)

                var.ui.tabClientes.setItem(i, 0, QtWidgets.QTableWidgetItem(registro[0]))
                var.ui.tabClientes.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tabClientes.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[3]))
                var.ui.tabClientes.setItem(i, 3, QtWidgets.QTableWidgetItem(registro[5]))
                var.ui.tabClientes.setItem(i, 4, QtWidgets.QTableWidgetItem(registro[7]))
                var.ui.tabClientes.setItem(i, 5, QtWidgets.QTableWidgetItem(registro[8]))
                var.ui.tabClientes.setItem(i, 6, QtWidgets.QTableWidgetItem(registro[9]))

                var.ui.tabClientes.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabClientes.item(i, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(i, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabClientes.item(i, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
            if var.ui.tabClientes.rowCount() == 0:
                Clientes.setTablaVaciaCli(self)

        except Exception as e:
            print("Error cargar Clientes", e)

    def setTablaVaciaCli(self):
        var.ui.tabClientes.setRowCount(0)
        var.ui.tabClientes.setRowCount(1)
        var.ui.tabClientes.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay Clientes"))
        var.ui.tabClientes.item(0, 2).setTextAlignment(
            QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        return

    def cargaCliente(self):
        try:
            fila = var.ui.tabClientes.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOneCliente(str(datos[0]))

            listado = [var.ui.txtDniCli, var.ui.txtCalendarCli,
                       var.ui.txtApelCli, var.ui.txtNomCli,
                       var.ui.txtEmailCli, var.ui.txtMovilCli,
                       var.ui.txtDirCli, var.ui.cmbProvCli,
                       var.ui.cmbMuniCli, var.ui.txtBajaCli]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(registro[i])
                else:
                    casilla.setText(registro[i])

        except Exception as e:
            print("Error cargar Clientes", e)

    def cargaClienteDni(self):
        try:
            dni = var.ui.txtDniCli.text()
            registro = conexion.Conexion.datosOneCliente(dni)
            if not registro:
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Aviso")
                mbox.setText("No se ha encontrado el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

            listado = [var.ui.txtDniCli, var.ui.txtCalendarCli,
                       var.ui.txtApelCli, var.ui.txtNomCli,
                       var.ui.txtEmailCli, var.ui.txtMovilCli,
                       var.ui.txtDirCli, var.ui.cmbProvCli,
                       var.ui.cmbMuniCli, var.ui.txtBajaCli]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(registro[i])
                else:
                    casilla.setText(registro[i])

        except Exception as e:
            print("Error cargar Clientes por dni", e)

    def modifCliente(self):
        try:
            registro = [var.ui.txtDniCli.text(), var.ui.txtCalendarCli.text(),
                        var.ui.txtApelCli.text(), var.ui.txtNomCli.text(),
                        var.ui.txtEmailCli.text(), var.ui.txtMovilCli.text(),
                        var.ui.txtDirCli.text(),
                        var.ui.cmbProvCli.currentText(),
                        var.ui.cmbMuniCli.currentText(),
                        var.ui.txtBajaCli.text()]
            mensajes_error = [
                "Falta ingresar DNI",
                "Falta ingresar fecha de alta",
                "Falta ingresar apellido",
                "Falta ingresar nombre",
                None,
                "Falta ingresar móvil",
                "Falta ingresar dirección",
                "Falta seleccionar provincia",
                "Falta seleccionar municipio"
            ]

            for i, dato in enumerate(registro):
                if i == 4:  # Saltamos la validación para el email (índice 4)
                    continue
                if dato == '':
                    mbox = QtWidgets.QMessageBox()
                    mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    mbox.setWindowTitle("Error en los datos")
                    mbox.setText(mensajes_error[i])
                    mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    mbox.exec()
                    return
            if conexion.Conexion.modifCliente(registro):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Cliente modificado correctamente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al modificadar el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            clientes.Clientes.cargaTablaClientes(self)
        except Exception as error:
            print("error modificar cliente", error)

    def bajaCliente(self):
        try:
            datos = [var.ui.txtBajaCli.text(), var.ui.txtDniCli.text()]
            if conexion.Conexion.bajaCliente(datos):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Cliente dado de baja correctamente')
                mbox.setStandardButtons(
                    QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al dar de baja el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            Clientes.cargaTablaClientes(self)

        except Exception as error:
            print("Error en baja cliente: ", error)

    @staticmethod
    def checkTelefono(telefono):
        try:
            if eventos.Eventos.validarTelefono(telefono):
                var.ui.txtMovilCli.setStyleSheet('background-color: rgb(255, 255, 255);')
            else:
                var.ui.txtMovilCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtMovilCli.setText("telefono no válido")
                var.ui.txtMovilCli.setFocus()

        except Exception as error:
            print("error check cliente", error)

    @staticmethod
    def historicoCli(self):
        try:
            if var.ui.chkHistoriaCli.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            var.paginaCli = 0
            Clientes.cargaTablaClientes(self)

        except Exception as error:
            print("Error en historico cliente: ", error)