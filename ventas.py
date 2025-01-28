from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import var
from propiedades import Propiedades


class Ventas():

    def altaVenta(self):
        nuevaVenta = [var.ui.txtCodigoVentaFac.text(), var.ui.txtNumFac.text(), var.ui.txtIdVendedorFac.text()]

        mensajes_error = [
            "Falta agregar la propiedad",
            "Falta agregar la factura",
            "Falta agregar al vendedor"
        ]

        for i, dato in enumerate(nuevaVenta):
            if dato == '':
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en los datos")
                mbox.setText(mensajes_error[i])
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

        try:
            if conexion.Conexion.altaVenta(self, nuevaVenta):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Aviso")
                mbox.setText("Se ha insertado la venta correctamente.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print(e)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText('Error al insertar la venta. Intente nuevamente.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()
        Ventas.cargaTablaVentas(self)
        Propiedades.cargaTablaPropiedades(self,0)

    def cargaTablaVentas(self):
        try:
            listado = conexion.Conexion.listadoVentas(self)

            var.ui.tabVentasFac.setRowCount(0)

            i = 0

            for registro in listado:
                var.ui.tabVentasFac.setRowCount(i + 1)

                var.ui.tabVentasFac.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabVentasFac.setItem(i, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabVentasFac.setItem(i, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tabVentasFac.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tabVentasFac.setItem(i, 4, QtWidgets.QTableWidgetItem(str(registro[4])))
                var.ui.tabVentasFac.setItem(i, 5, QtWidgets.QTableWidgetItem(str(registro[5])))

                var.ui.tabVentasFac.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVentasFac.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVentasFac.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVentasFac.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                var.ui.tabVentasFac.item(i, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                var.ui.tabVentasFac.item(i, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1

            if var.ui.tabVentasFac.rowCount() == 0:
                return Ventas.setTablaVaciaVenta(self)

        except Exception as e:
            print("Error cargar tabla venta", e)

    def setTablaVaciaVenta(self):
        var.ui.tabVentasFac.setRowCount(1)
        var.ui.tabVentasFac.setItem(0, 1, QtWidgets.QTableWidgetItem("No hay ventas"))
        var.ui.tabVentasFac.item(0, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        return

    def cargaOneVenta(self):
        try:
            fila = var.ui.tabVentasFac.selectedItems()
            datos = [dato.text() for dato in fila]
            if (datos[0] == "No hay Ventas"):
                return
            registro = conexion.Conexion.datosOneVenta(str(datos[0]))

            listado = [
                var.ui.txtIdVendedorFac, var.ui.txtNumFac,
                var.ui.txtFechaFac, var.ui.txtDniFac,
                var.ui.txtNomFac, var.ui.txtApelFac,
                var.ui.txtCodigoVentaFac, var.ui.txtDirFac,
                var.ui.txtTipoFac, var.ui.txtLocalidadFac, var.ui.txtPrecioFac
            ]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLabel):
                    casilla.setText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLineEdit):
                    casilla.setText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))

        except Exception as e:
            print("Error cargar Vendedor", e)

    def eliminar_factura(self, idFactura):
        try:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            msgbox.setWindowTitle('Aviso')
            msgbox.setText("Desea Eliminar la Factura")
            msgbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            msgbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            if msgbox.exec():
                if conexion.Conexion.delFactura(self, int(idFactura)):
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    msgbox.setWindowTitle('Aviso')
                    msgbox.setText("Factura Eliminada")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    msgbox.exec()
                    Ventas.cargaTablaVentas(self)
            else:
                msgbox.hide()
        except Exception as error:
            print("Eliminar facturade ", error)