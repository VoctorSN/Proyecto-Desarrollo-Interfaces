import sqlite3
from tkinter.messagebox import ERROR

from PyQt6 import QtWidgets, QtGui

import conexion
import eventos
import var

class Clientes:


    def altaCliente(self):
        nuevoCli = [var.ui.txtDniCli.text(),var.ui.txtCalendarCli.text(),
                 var.ui.txtApelCli.text(),var.ui.txtNomCli.text(),
                 var.ui.txtEmailCli.text(),var.ui.txtMovilCli.text(),
                 var.ui.txtDirCli.text(),
                 var.ui.cmbProvCli.currentText(),
                 var.ui.cmbMuniCli.currentText()]
        if conexion.Conexion.altaCliente(self,nuevoCli):
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowIcon(QtGui.QIcon('img/logo.ico'))
            mbox.setWindowTitle('Aviso')
            mbox.setText('Cliente dado de alta correctamente')
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
            mbox.setText("Error al dar de alta el cliente")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Cancel)
            mbox.exec()

    def checkDni(dni):
        try:
            dni = str(dni).upper()
            check = eventos.Eventos.checkDNI(dni)
            var.ui.txtDniCli.setText(str(dni))
            if check:
                var.ui.txtDniCli.setStyleSheet('background-color: rgb(255,255,220);')
            else:
                var.ui.txtDniCli.setStyleSheet('background-color:#FFC0CB;')
                var.ui.txtDniCli.setText(None)
                var.ui.txtDniCli.setFocus()
        except Exception as error:
            print("Error en validar dni ", error)

    def checkEmail(mail):
        try:
            mail = str(var.ui.txtEmailCli.text())
            if eventos.Eventos.validarMail(mail):
                var.ui.txtEmailCli.setStyleSheet('background-color: rgb(255, 255, 255);')
                var.ui.txtEmailCli.setText(mail.lower())

            else:
                var.ui.txtEmailCli.setStyleSheet('background-color:#FFC0CB; font-style: italic;')
                var.ui.txtEmailCli.setText(None)
                var.ui.txtEmailCli.setText("correo no válido")
                var.ui.txtEmailCli.setFocus()
        except sqlite3.IntegrityError as e:
            print("Error, ya existe el dni: ", e)
        except Exception as error:
            print("error check cliente", error)
