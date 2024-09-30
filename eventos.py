import sys
from PyQt6 import QtWidgets

import conexion
import var


class Eventos():
    def mensajeSalir(self=None):
        mbox = QtWidgets.QMessageBox()
        mbox.setIcon(QtWidgets.QMessageBox.Icon.Question)
        mbox.setWindowTitle('Salir')
        mbox.setText('Desea usted Salir?')
        mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        mbox.setDefaultButton(QtWidgets.QMessageBox.StandardButton.No)
        mbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
        mbox.button(QtWidgets.QMessageBox.StandardButton.No).setText('No')

        if mbox.exec() == QtWidgets.QMessageBox.StandardButton.Yes:
            sys.exit()
        else:
            mbox.hide()

    def cargarProv(self):
        cmbProvCli = var.ui.cmbProvCli
        listaprov = conexion.Conexion.listaProv(self)
        cmbProvCli.clear()
        cmbProvCli.addItems(listaprov)

    def cargarMun(self,pkProv):
        cmbMuniCli = var.ui.cmbMuniCli
        listaprov = conexion.Conexion.listaMun(self,pkProv)
        cmbMuniCli.clear()
        cmbMuniCli.addItems(listaprov)