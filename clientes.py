from tkinter.messagebox import ERROR

from PyQt6 import QtWidgets

import eventos
import var

class Clientes:
    def altaCliente(self):
        dni  = var.ui.txtDniCli.text()

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