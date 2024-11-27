from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import conexionserver
import eventos
import var


class Propiedades():
    def altaTipoPropiedad(self):
        try:
            tipo = var.dlgGestion.ui.txtGestTipoProp.text().title()
            registro = conexionserver.ConexionServer.altaTipoPropiedad(self,tipo)
            if registro:
                eventos.Eventos.cargarTipoPropiedad(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('Ya existe el tipo.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            var.dlgGestion.ui.txtGestTipoProp.setText('')
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)

    def bajaTipoPropiedad(self):
        try:
            tipo = var.dlgGestion.ui.txtGestTipoProp.text().title()
            registro = conexionserver.ConexionServer.bajaTipoPropiedad(self,tipo)
            if registro:
                eventos.Eventos.cargarTipoPropiedad(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('No existe el tipo.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
            var.dlgGestion.ui.txtGestTipoProp.setText('')
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    def altaPropiedad(self):
        nuevaProp = [var.ui.txtFechaProp.text(), var.ui.txtDirProp.text(),
                     var.ui.cmbProvProp.currentText(), var.ui.cmbMuniProp.currentText(),
                     var.ui.cmbTipoProp.currentText(), var.ui.spinHabProp.text(),
                     var.ui.spinBanosProp.text(), var.ui.txtSuperProp.text(),
                     var.ui.txtPrecioAlquilerProp.text(), var.ui.txtPrecioVentaProp.text(),
                     var.ui.txtCPProp.text(), var.ui.areatxtDescripProp.toPlainText(),
                     var.ui.txtNomeProp.text(), var.ui.txtMovilProp.text()]

        mensajes_error = [
            "Falta ingresar fecha de alta",
            "Falta ingresar dirección",
            "Falta seleccionar provincia",
            "Falta seleccionar municipio",
            "Falta seleccionar tipo de propiedad",
            "Falta ingresar número de habitaciones",
            "Falta ingresar número de baños",
            "Falta ingresar superficie",
            None,
            None,
            "Falta ingresar código postal",
            None,  # No validation for description
            "Falta ingresar nombre del propietario",
            "Falta ingresar móvil del propietario"
        ]

        for i, dato in enumerate(nuevaProp):
            if i in (11,9,8):  # Skip validation for description (index 11)
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
            tipooper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipooper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipooper.append(var.ui.chkVentaProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipooper.append(var.ui.chkIntercambioProp.text())
            nuevaProp.append("-".join(tipooper))

            if var.ui.rbtEstadoDisponibleProp.isChecked():
                nuevaProp.append(var.ui.rbtEstadoDisponibleProp.text())
            if var.ui.rbtEstadoAlquiladoProp.isChecked():
                nuevaProp.append(var.ui.rbtEstadoAlquiladoProp.text())
            if var.ui.rbtEstadoVendidoProp.isChecked():
                nuevaProp.append(var.ui.rbtEstadoVendidoProp.text())

            if conexionserver.ConexionServer.altaPropiedad(self,nuevaProp):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Aviso")
                mbox.setText("Se ha insertado la propiedad correctamente.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Propiedades.cargaTablaPropiedades(self, 0)
        except Exception as e:
            print(e)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText('Error al insertar la propiedad. Intente nuevamente.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()

    def cargaTablaPropiedades(self, contexto):
        try:
            listado = (conexionserver.ConexionServer.listadoPropiedades(self))
            var.ui.tabPropiedades.setRowCount(0)
            i = 0
            for registro in listado:
                if contexto == 1 and (
                        var.ui.cmbTipoProp.currentText() != registro[6] or var.ui.cmbMuniProp.currentText() != registro[
                    5]):
                    continue

                var.ui.tabPropiedades.setRowCount(i + 1)

                var.ui.tabPropiedades.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabPropiedades.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[5]))
                var.ui.tabPropiedades.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[6]))
                var.ui.tabPropiedades.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[7])))
                var.ui.tabPropiedades.setItem(i, 4, QtWidgets.QTableWidgetItem(str(registro[8])))
                if registro[10] == "":
                    registro[10] = "-"
                if registro[11] == "":
                    registro[11] = "-"
                var.ui.tabPropiedades.setItem(i, 5, QtWidgets.QTableWidgetItem(str(registro[10]) + " €"))
                var.ui.tabPropiedades.setItem(i, 6, QtWidgets.QTableWidgetItem(str(registro[11]) + " €"))
                var.ui.tabPropiedades.setItem(i, 7, QtWidgets.QTableWidgetItem(registro[14]))
                var.ui.tabPropiedades.setItem(i, 8, QtWidgets.QTableWidgetItem(registro[2]))

                var.ui.tabPropiedades.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabPropiedades.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                var.ui.tabPropiedades.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(i, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(i, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(i, 6).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(i, 7).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabPropiedades.item(i, 8).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1

            if var.ui.tabPropiedades.rowCount() == 0:
                var.ui.tabPropiedades.setRowCount(1)
                var.ui.tabPropiedades.setItem(0, 2, QtWidgets.QTableWidgetItem("No hay propiedades"))
                var.ui.tabPropiedades.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
                return

        except Exception as e:
            print("Error cargar tabPropiedades", e)

    def cargaPropiedad(self):
        try:
            fila = var.ui.tabPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            if (datos[0] == "No hay propiedades"):
                return
            registro = conexionserver.ConexionServer.datosOnePropiedad(self,str(datos[0]))

            listado = [var.ui.lblProp, var.ui.txtFechaProp,
                       var.ui.txtFechaBajaProp, var.ui.txtDirProp,
                       var.ui.cmbProvProp, var.ui.cmbMuniProp,
                       var.ui.cmbTipoProp, var.ui.spinHabProp, var.ui.spinBanosProp,
                       var.ui.txtSuperProp, var.ui.txtPrecioAlquilerProp, var.ui.txtPrecioVentaProp,
                       var.ui.txtCPProp, var.ui.areatxtDescripProp, var.ui.chkAlquilerProp,
                       var.ui.rbtEstadoDisponibleProp, var.ui.txtNomeProp, var.ui.txtMovilProp
                       ]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QCheckBox):
                    if ("Alquiler") in registro[i]:
                        var.ui.chkAlquilerProp.setChecked(True)
                    else:
                        var.ui.chkAlquilerProp.setChecked(False)
                    if ("Venta") in registro[i]:
                        var.ui.chkVentaProp.setChecked(True)
                    else:
                        var.ui.chkVentaProp.setChecked(False)
                    if ("Intercambio") in registro[i]:
                        var.ui.chkIntercambioProp.setChecked(True)
                    else:
                        var.ui.chkIntercambioProp.setChecked(False)
                elif isinstance(casilla, QtWidgets.QRadioButton):
                    if registro[i] == "Vendido":
                        var.ui.rbtEstadoVendidoProp.setChecked(True)
                    elif registro[i] == "Disponible":
                        var.ui.rbtEstadoDisponibleProp.setChecked(True)
                    else:
                        var.ui.rbtEstadoAlquiladoProp.setChecked(True)
                elif isinstance(casilla, QtWidgets.QSpinBox):
                    casilla.setValue(int(registro[i]))
                elif isinstance(casilla, QtWidgets.QTextEdit):
                    casilla.setPlainText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))

        except Exception as e:
            print("Error cargar Propiedad", e)

    def modifPropiedad(self):
        try:
            registro = [var.ui.lblProp.text(), var.ui.txtFechaProp.text(), var.ui.txtDirProp.text(),
                        var.ui.cmbProvProp.currentText(), var.ui.cmbMuniProp.currentText(),
                        var.ui.cmbTipoProp.currentText(), var.ui.spinHabProp.text(),
                        var.ui.spinBanosProp.text(), var.ui.txtSuperProp.text(),
                        var.ui.txtPrecioAlquilerProp.text(), var.ui.txtPrecioVentaProp.text(),
                        var.ui.txtCPProp.text(), var.ui.areatxtDescripProp.toPlainText(),
                        ]
            tipooper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipooper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipooper.append(var.ui.chkVentaProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipooper.append(var.ui.chkIntercambioProp.text())
            registro.append("-".join(tipooper))

            if var.ui.rbtEstadoDisponibleProp.isChecked():
                registro.append(var.ui.rbtEstadoDisponibleProp.text())
            if var.ui.rbtEstadoAlquiladoProp.isChecked():
                registro.append(var.ui.rbtEstadoAlquiladoProp.text())
            if var.ui.rbtEstadoVendidoProp.isChecked():
                registro.append(var.ui.rbtEstadoVendidoProp.text())
            registro.append(var.ui.txtNomeProp.text())
            registro.append(var.ui.txtMovilProp.text())

            if conexionserver.ConexionServer.modifPropiedad(self,registro):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setWindowTitle('Aviso')
                mbox.setText('Propiedad modificada correctamente')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Propiedades.cargaTablaPropiedades(1, 0)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al modificar la propiedad")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
                Propiedades.cargaTablaPropiedades(1, 0)

        except Exception as error:
            print("error modificar propiedad", error)

    def bajaPropiedad(self):
        try:
            fechas = Propiedades.checkFechas(self)
            disponible = var.ui.rbtEstadoDisponibleProp.isChecked()
            baja = conexionserver.ConexionServer.bajaPropiedad(self,
                    int(var.ui.lblProp.text()))
            if fechas and not disponible and baja:
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
                Propiedades.cargaTablaPropiedades(self, 0)
            elif not disponible:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("No puedes dar de baja una propiedad Disponible")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            elif fechas:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("No puedes dar de baja una propiedad con fecha de alta mayor a fecha de baja")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Aviso")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
                mbox.setText("Error al dar de baja el cliente")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
                mbox.exec()

        except Exception as error:
            print("Error en baja cliente: ", error)

    def historicoProp(self):
        try:
            if var.ui.chkHistoriaProp.isChecked():
                var.historico = 0
            else:
                var.historico = 1
            Propiedades.cargaTablaPropiedades(self, 0)

        except Exception as error:
            print("Error en historico propiedades: ", error)

    def checkFechas(self):
        baja = var.ui.txtFechaBajaProp.text()
        if baja == '' or baja == 'None':
            baja = datetime.now().strftime("%d/%m/%Y")
        alta = var.ui.txtFechaProp.text()
        formato = "%d/%m/%Y"

        date1 = datetime.strptime(baja, formato)
        date2 = datetime.strptime(alta, formato)
        return date1 > date2

    def checkVentaProp(self):
        if var.ui.txtPrecioVentaProp.text() != '':
            var.ui.chkVentaProp.setChecked(True)
        else:
            var.ui.chkVentaProp.setChecked(False)
            var.ui.chkVentaProp.setEnabled(False)

    def checkBajaProp(self):
        Propiedades.changeRadioProp(self, var.ui.txtFechaBajaProp.text() == '')

    def changeRadioProp(self, set):
        if not set:
            var.ui.rbtEstadoVendidoProp.setEnabled(True)
            var.ui.rbtEstadoAlquiladoProp.setEnabled(True)
            var.ui.rbtEstadoDisponibleProp.setChecked(False)
            var.ui.rbtEstadoAlquiladoProp.setChecked(True)
            var.ui.rbtEstadoDisponibleProp.setEnabled(False)
        else:
            var.ui.rbtEstadoVendidoProp.setEnabled(False)
            var.ui.rbtEstadoAlquiladoProp.setEnabled(False)
            var.ui.rbtEstadoDisponibleProp.setEnabled(True)
            var.ui.rbtEstadoDisponibleProp.setChecked(True)
            var.ui.rbtEstadoAlquiladoProp.setChecked(False)

    def checkAlquilerProp(self):
        if var.ui.txtPrecioAlquilerProp.text() != '':
            var.ui.chkAlquilerProp.setChecked(True)
        else:
            var.ui.chkAlquilerProp.setChecked(False)
            var.ui.chkAlquilerProp.setEnabled(False)