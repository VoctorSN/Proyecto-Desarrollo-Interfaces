from tkinter.messagebox import ERROR

from PyQt6 import QtWidgets

import conexion
import eventos
import var

class Clientes:

    @staticmethod
    def altaCliente():
        nuevoCli = [var.ui.txtDniCli.text(),var.ui.txtCalendarCli.text(),
                 var.ui.txtApelCli.text(),var.ui.txtNomCli.text(),
                 var.ui.txtEmailCli.text(),var.ui.txtMovilCli.text(),
                 var.ui.txtDirCli.text(),
                 var.ui.cmbProvCli.currentText(),
                 var.ui.cmbMuniCli.currentText()]
        conexion.Conexion.altaCliente(nuevoCli)

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

        except Exception as error:
            print("error check cliente", error)