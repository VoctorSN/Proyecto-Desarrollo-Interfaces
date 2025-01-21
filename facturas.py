from datetime import datetime
from multiprocessing.resource_tracker import register

from PyQt6 import QtWidgets, QtGui, QtCore, QtSql
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import *

import conexion
import eventos
import var

from datetime import datetime


class Facturas():

    def deleteFactura(self):
        print("borrando factura")


    def altaFactura(self):
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
            if conexion.Conexion.altaFactura(self,nuevaFac):
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
        try:
            listado = conexion.Conexion.listadoFacturas(self)

            var.ui.tabFacturas.setRowCount(0)

            i = 0

            for registro in listado:

                var.ui.tabFacturas.setRowCount(i + 1)

                container = QWidget()
                layout = QVBoxLayout()
                var.botondel = QPushButton()
                var.botondel.setFixedSize(30, 20)
                var.botondel.setIcon(QIcon("./img/papelera.ico"))
                var.botondel.setStyleSheet("background-color: #efefef;")
                var.botondel.clicked.connect(Facturas.deleteFactura)
                layout.addWidget(var.botondel)
                layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)

                var.ui.tabFacturas.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabFacturas.setItem(i, 1, QtWidgets.QTableWidgetItem(registro[2]))
                var.ui.tabFacturas.setItem(i, 2, QtWidgets.QTableWidgetItem(registro[1]))
                var.ui.tabFacturas.setCellWidget(i, 3, container)

                var.ui.tabFacturas.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabFacturas.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabFacturas.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1

            if var.ui.tabPropiedades.rowCount() == 0:
                return Facturas.setTablaVaciaFac(self)

        except Exception as e:
            print("Error cargar tabPropiedades", e)


    def setTablaVaciaFac(self):
        var.ui.tabFacturas.setRowCount(1)
        var.ui.tabFacturas.setItem(0, 1, QtWidgets.QTableWidgetItem("No hay facturas"))
        var.ui.tabFacturas.item(0, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignVCenter)
        return