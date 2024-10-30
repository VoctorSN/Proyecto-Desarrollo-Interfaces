
from PyQt6 import QtWidgets, QtGui, QtCore, QtSql
from matplotlib.pyplot import connect

import conexion
import eventos
import var


class Propiedades():
    def altaTipoPropiedad(self):
        try:
            tipo = var.dlgGestion.ui.txtGestTipoProp.text().title()
            registro = conexion.Conexion.altaTipoPropiedad(tipo)
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
            registro = conexion.Conexion.bajaTipoPropiedad(tipo)
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
        try:
            propiedad = [var.ui.txtFechaProp.text(),var.ui.txtDirProp.text(),
                         var.ui.cmbProvProp.currentText(),var.ui.cmbMuniProp.currentText(),
                         var.ui.cmbTipoProp.currentText(),var.ui.spinHabProp.text(),
                         var.ui.spinBanosProp.text(),var.ui.txtSuperProp.text(),
                         var.ui.txtPrecioAlquilerProp.text(),var.ui.txtPrecioVentaProp.text(),
                         var.ui.txtCPProp.text(),var.ui.areatxtDescripProp.toPlainText()]
            tipooper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipooper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipooper.append(var.ui.chkVentaProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipooper.append(var.ui.chkIntercambioProp.text())
            propiedad.append(tipooper)
            if var.ui.rbtEstadoDisponibleProp.isChecked():
                propiedad.append(var.ui.rbtEstadoDisponibleProp.text())
            if var.ui.rbtEstadoAlquiladoProp.isChecked():
                propiedad.append(var.ui.rbtEstadoAlquiladoProp.text())
            if var.ui.rbtEstadoVendidoProp.isChecked():
                propiedad.append(var.ui.rbtEstadoVendidoProp.text())
            propiedad.append(var.ui.txtNomeProp.text())
            propiedad.append(var.ui.txtMovilProp.text())
            conexion.Conexion.altaPropiedad(propiedad)
        except Exception as error:
            print("Error en alta propiedad: ", error)