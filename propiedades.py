from PyQt6 import QtWidgets, QtCore

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
            propiedad = [var.ui.txtFechaProp.text(), var.ui.txtDirProp.text(),
                         var.ui.cmbProvProp.currentText(), var.ui.cmbMuniProp.currentText(),
                         var.ui.cmbTipoProp.currentText(), var.ui.spinHabProp.text(),
                         var.ui.spinBanosProp.text(), var.ui.txtSuperProp.text(),
                         var.ui.txtPrecioAlquilerProp.text(), var.ui.txtPrecioVentaProp.text(),
                         var.ui.txtCPProp.text(), var.ui.areatxtDescripProp.toPlainText()]
            tipooper = []
            if var.ui.chkAlquilerProp.isChecked():
                tipooper.append(var.ui.chkAlquilerProp.text())
            if var.ui.chkVentaProp.isChecked():
                tipooper.append(var.ui.chkVentaProp.text())
            if var.ui.chkIntercambioProp.isChecked():
                tipooper.append(var.ui.chkIntercambioProp.text())
            propiedad.append("-".join(tipooper))
            if var.ui.rbtEstadoDisponibleProp.isChecked():
                propiedad.append(var.ui.rbtEstadoDisponibleProp.text())
            if var.ui.rbtEstadoAlquiladoProp.isChecked():
                propiedad.append(var.ui.rbtEstadoAlquiladoProp.text())
            if var.ui.rbtEstadoVendidoProp.isChecked():
                propiedad.append(var.ui.rbtEstadoVendidoProp.text())
            propiedad.append(var.ui.txtNomeProp.text())
            propiedad.append(var.ui.txtMovilProp.text())
            conexion.Conexion.altaPropiedad(propiedad)
            Propiedades.cargaTablaPropiedades(self)
        except Exception as error:
            print("Error en alta propiedad: ", error)

    def cargaTablaPropiedades(self,*contexto):
        try:
            listado = conexion.Conexion.listadoPropiedades(self,contexto)
            for i, registro in enumerate(listado):
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

        except Exception as e:
            print("Error cargar tabPropiedades", e)

    def cargaPropiedad(self):
        try:
            fila = var.ui.tabPropiedades.selectedItems()
            datos = [dato.text() for dato in fila]
            registro = conexion.Conexion.datosOnePropiedad(str(datos[0]))

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
                    if ("Intercambio") in  registro[i]:
                        var.ui.chkIntercambioProp.setChecked(True)
                    else:
                        var.ui.chkIntercambioProp.setChecked(False)
                elif isinstance(casilla,QtWidgets.QRadioButton):
                    if registro[i] == "Vendido":
                        var.ui.rbtEstadoVendidoProp.setChecked(True)
                    elif registro[i] == "Disponible":
                        var.ui.rbtEstadoDisponibleProp.setChecked(True)
                    else:
                        var.ui.rbtEstadoAlquiladoProp.setChecked(True)
                elif isinstance(casilla,QtWidgets.QSpinBox):
                    casilla.setValue(registro[i])
                elif isinstance(casilla,QtWidgets.QTextEdit):
                    casilla.setPlainText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))

        except Exception as e:
            print("Error cargar Clientes", e)