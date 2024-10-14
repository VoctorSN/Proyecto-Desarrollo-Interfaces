import sys

import clientes
import conexion
import conexionserver
import eventos
import styles
from VenPrincipal import Ui_venPrincipal
from venAux import *


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)

        '''
        EVENTOS DE TABLAS
        '''
        clientes.Clientes.cargaTablaClientes(self)
        eventos.Eventos.resizeTablaClientes(self)

        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        ZONA DE EVENTOS DE BOTONES
        '''
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0))
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)

        '''
        ZONA DE EVENTOS DE TEXTBOX  
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDni(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))

        '''
        ZONA DE EVENTOS DE COMBOX  
        '''
        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargarMuniCli)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
