import sys

import clientes
import conexion
import conexionserver
import eventos
import styles
import var
from venPrincipal import Ui_venPrincipal
from venAux import *


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgGestion = dlgTipoProp()
        var.dlgabrir = FileDialogAbrir()
        self.setStyleSheet(styles.load_stylesheet())
        var.historico = 1
        conexion.Conexion.db_conexion(self)

        '''
        EVENTOS DE TABLAS
        '''
        clientes.Clientes.cargaTablaClientes(self)
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaCliente)

        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.actionTipo_Propiedades.triggered.connect(eventos.Eventos.abrirTipoProp)

        '''
        ZONA DE EVENTOS DE BOTONES
        '''
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(0,1))
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnModifCli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelCli.clicked.connect(clientes.Clientes.bajaCliente)

        '''
        ZONA DE EVENTOS DE TEXTBOX  
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDni(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(lambda: clientes.Clientes.checkEmail(var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checkTelefono(var.ui.txtMovilCli.text()))

        '''
        ZONA DE EVENTOS DE COMBOX  
        '''
        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargarMuniCli)

        '''
        ZONA DE EVENTOS DE TOOLBAR  
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)

        '''
        ZONA DE EVENTOS DE CHECKBOX  
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
