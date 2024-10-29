
from PyQt6 import QtWidgets, QtGui, QtCore, QtSql

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
            propiedad = [var.ui.txtFechaProp.text(),var.ui.txtDirProp.text(),var.ui.txtFechaBajaProp.text(),
                         var.ui.cmbProvProp.currentText(),var.ui.cmbMuniProp.currentText(),
                         var.ui.cmbTipoProp.currentText(),var.ui.spinHabProp.text(),
                         var.ui.spinBanosProp.text(),var.ui.txtSuperProp.text(),
                         var.ui.txtPrecioAlquilerProp.text(),var.ui.txtPrecioVentaProp.text(),
                         var.ui.txtCPProp.text(),var.ui.areatxtDescripProp.toPlainText(),
                         var.ui.txtNomeProp.text(),var.ui.txtMovilProp.text()]
            print(propiedad)
        except Exception as error:
            print("Error en alta propiedad: ", error)