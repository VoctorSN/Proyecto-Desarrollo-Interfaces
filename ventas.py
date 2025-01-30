from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import var
from propiedades import Propiedades


class Ventas():

    botonesdel = []

    def altaVenta(self):
        nuevaVenta = [var.ui.txtCodigoVentaFac.text(), var.ui.txtNumFac.text(), var.ui.txtIdVendedorFac.text(), var.ui.txtPrecioFac.text()]

        mensajes_error = [
            "Falta agregar la propiedad",
            "Falta agregar la factura",
            "Falta agregar al vendedor",
            "Esta propiedad no esta a la venta, (No tiene precio de Venta)"
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
            if conexion.Conexion.isFacturada(self,nuevaVenta[0]):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en grabar Venta")
                mbox.setText("Esta venta ya esta en una factura")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return
            elif conexion.Conexion.altaVenta(self, nuevaVenta):
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

    def cargaTablaVentas(self, idFactura=None):
        try:
            if idFactura is None:
                listado = conexion.Conexion.listadoVentas(self)
            else:
                listado = conexion.Conexion.listadoVentas(self, idFactura)


            var.ui.tabVentasFac.setRowCount(0)

            i = 0
            total = 0

            for registro in listado:
                var.ui.tabVentasFac.setRowCount(i + 1)



                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Ventas.botonesdel.append(QtWidgets.QPushButton())
                Ventas.botonesdel[-1].setFixedSize(30, 20)
                Ventas.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Ventas.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Ventas.botonesdel[-1].clicked.connect(lambda checked: Ventas.eliminar_venta(self, str(registro[0])))
                layout.addWidget(Ventas.botonesdel[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)

                var.ui.tabVentasFac.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabVentasFac.setItem(i, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabVentasFac.setItem(i, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tabVentasFac.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tabVentasFac.setItem(i, 4, QtWidgets.QTableWidgetItem(str(registro[4])))
                var.ui.tabVentasFac.setItem(i, 5, QtWidgets.QTableWidgetItem(str(registro[5]) + " €"))
                var.ui.tabVentasFac.setCellWidget(i, 6, container)

                var.ui.tabVentasFac.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVentasFac.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabVentasFac.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                var.ui.tabVentasFac.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                var.ui.tabVentasFac.item(i, 4).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
                var.ui.tabVentasFac.item(i, 5).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1

                total += float(registro[5])

            var.ui.lblPrecioBrutoFac.setText(str(total) + "€")
            var.ui.lblImpuestosFac.setText(str(total * 0.1)[:4] + "€")
            var.ui.lblTotalFac.setText(str(total + (total * 0.1)) + "€")

            if var.ui.tabVentasFac.rowCount() == 0:
                return Ventas.setTablaVaciaVenta(self)

        except Exception as e:
            print("Error cargar tabla venta", e)

    def setTablaVaciaVenta(self):
        var.ui.tabVentasFac.setRowCount(1)
        var.ui.tabVentasFac.setItem(0, 3, QtWidgets.QTableWidgetItem("No hay ventas"))
        var.ui.tabVentasFac.item(0, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignCenter)
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

    def eliminar_venta(self, idVenta):
        try:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            msgbox.setWindowTitle('Aviso')
            msgbox.setText("Desea Eliminar la Venta")
            msgbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            msgbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            idPropiedad = conexion.Conexion.datosOneVenta(idVenta)[6]
            if msgbox.exec():
                if conexion.Conexion.delVenta(self, idPropiedad, int(idVenta)):
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    msgbox.setWindowTitle('Aviso')
                    msgbox.setText("Venta Eliminada")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    msgbox.exec()
                    Ventas.cargaTablaVentas(self)
            else:
                msgbox.hide()
        except Exception as error:
            print("Eliminar venta ", error)