from datetime import datetime

from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt

import conexion
import eventos
import var
import ventas


class Facturas:
    """
    Clase que gestiona las facturas dentro de la aplicación. Permite dar de alta,
    eliminar y cargar facturas en la tabla de la interfaz gráfica.
    """

    botonesdel = []  # Lista para almacenar los botones de eliminación de facturas

    def altaFactura(self):
        """
        Método que registra una nueva factura en la base de datos.

        Valida que los campos obligatorios estén completos antes de insertar
        la factura en la base de datos.

        :return: None
        :rtype: None
        """
        nuevaFac = [var.ui.txtDniFac.text(), var.ui.txtFechaFac.text()]

        mensajes_error = [
            "Falta ingresar el DNI",
            "Falta ingresar la fecha"
        ]

        for i, dato in enumerate(nuevaFac):
            if dato == '':
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en los datos")
                mbox.setText(mensajes_error[i])
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

        try:
            if conexion.Conexion.altaFactura(self, nuevaFac):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Aviso")
                mbox.setText("Se ha insertado la factura correctamente.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
        except Exception as e:
            print(e)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText('Error al insertar la factura. Intente nuevamente.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()
        Facturas.cargaTablaFacturas(self)

    def cargaTablaFacturas(self):
        """
        Método que carga la lista de facturas en la tabla de la interfaz gráfica.

        Si no hay facturas, se muestra un mensaje indicando que la tabla está vacía.

        :return: None
        :rtype: None
        """
        try:
            listado = conexion.Conexion.listadoFacturas(self)
            var.ui.tabFacturas.setRowCount(0)

            for i, registro in enumerate(listado):
                var.ui.tabFacturas.setRowCount(i + 1)

                # Crear botón de eliminación en cada fila
                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Facturas.botonesdel.append(QtWidgets.QPushButton())
                Facturas.botonesdel[-1].setFixedSize(30, 20)
                Facturas.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Facturas.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Facturas.botonesdel[-1].clicked.connect(lambda checked, id=registro[0]: Facturas.eliminar_factura(self, str(id)))
                layout.addWidget(Facturas.botonesdel[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)

                # Insertar datos en la tabla
                var.ui.tabFacturas.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabFacturas.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tabFacturas.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tabFacturas.setCellWidget(i, 3, container)

                # Alinear el texto en las celdas
                for j in range(3):
                    var.ui.tabFacturas.item(i, j).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

            if var.ui.tabFacturas.rowCount() == 0:
                return Facturas.setTablaVaciaFac(self)

        except Exception as e:
            print("Error al cargar las facturas:", e)

    def setTablaVaciaFac(self):
        """
        Método que establece la tabla de facturas con un mensaje indicando que no hay facturas.

        :return: None
        :rtype: None
        """
        var.ui.tabFacturas.setRowCount(1)
        var.ui.tabFacturas.setItem(0, 1, QtWidgets.QTableWidgetItem("No hay facturas"))
        var.ui.tabFacturas.item(0, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft | QtCore.Qt.AlignmentFlag.AlignVCenter)

    def cargaOneFactura(self):
        """
        Método que carga los datos de una factura seleccionada en los campos correspondientes.

        También carga la lista de ventas asociadas a la factura.

        :return: None
        :rtype: None
        """
        try:
            fila = var.ui.tabFacturas.selectedItems()
            datos = [dato.text() for dato in fila]

            if datos[0] == "No hay Facturas":
                return

            registro = conexion.Conexion.datosOneFactura(str(datos[0]))

            campos = [var.ui.txtNumFac, var.ui.txtFechaFac,
                      var.ui.txtDniFac, var.ui.txtNomFac, var.ui.txtApelFac]

            for i, campo in enumerate(campos):
                if isinstance(campo, QtWidgets.QComboBox):
                    campo.setCurrentText(str(registro[i]))
                elif isinstance(campo, (QtWidgets.QLabel, QtWidgets.QLineEdit)):
                    campo.setText(str(registro[i]))
                else:
                    campo.setText(str(registro[i]))

            ventas.Ventas.cargaTablaVentas(self, str(datos[0]))

        except Exception as e:
            print("Error al cargar la factura:", e)

    def eliminar_factura(self, idFactura):
        """
        Método que elimina una factura de la base de datos si no está en uso.

        Antes de eliminar la factura, se muestra un cuadro de diálogo para confirmar la acción.

        :param idFactura: ID de la factura a eliminar.
        :type idFactura: str
        :return: None
        :rtype: None
        """
        try:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            msgbox.setWindowTitle('Aviso')
            msgbox.setText("¿Desea eliminar la factura?")
            msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            msgbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Sí')

            if msgbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
                facturaUtilizada = conexion.Conexion.facturaUtilizada(self, int(idFactura)) != []
                if not facturaUtilizada and conexion.Conexion.delFactura(self, int(idFactura)):
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    msgbox.setWindowTitle('Aviso')
                    msgbox.setText("Factura eliminada correctamente.")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    msgbox.exec()
                    Facturas.cargaTablaFacturas(self)
                elif facturaUtilizada:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    msgbox.setWindowTitle('Aviso')
                    msgbox.setText("No se puede eliminar la factura porque está en uso.")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    msgbox.exec()
        except Exception as error:
            print("Error al eliminar la factura:", error)