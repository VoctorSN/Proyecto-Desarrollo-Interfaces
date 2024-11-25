import sys

import clientes
import conexionserver
import styles
from venAux import *
from venPrincipal import Ui_venPrincipal


class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        var.uicalendar = Calendar()
        var.dlgGestion = dlgTipoProp()
        var.dlgabrir = FileDialogAbrir()
        var.dlgAbout = dlgAbout()
        self.setStyleSheet(styles.load_stylesheet())
        var.historico = 1
        # conexion.Conexion.db_conexion(self)
        conexionserver.ConexionServer.crear_conexion(self)

        '''
        EVENTOS DE TABLAS
        '''
        clientes.Clientes.cargaTablaClientes(self)
        eventos.Eventos.resizeTablaClientes(self)
        var.ui.tabClientes.clicked.connect(clientes.Clientes.cargaCliente)
        propiedades.Propiedades.cargaTablaPropiedades(self, 0)
        eventos.Eventos.resizeTablaPropiedades(self)
        var.ui.tabPropiedades.clicked.connect(propiedades.Propiedades.cargaPropiedad)

        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionCrear_Backup.triggered.connect(eventos.Eventos.crearBackup)
        var.ui.actionRestaurar_Backup.triggered.connect(eventos.Eventos.restaurarBackup)
        var.ui.menuGestion.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionExportar_Clientes_CSV.triggered.connect(eventos.Eventos.exportCSVProp)
        var.ui.actionExportar_Clientes_JSON.triggered.connect(eventos.Eventos.exportJSONProp)
        var.ui.actionAbout.triggered.connect(eventos.Eventos.abrirAbout)

        '''
        ZONA DE EVENTOS DE BOTONES
        '''
        var.ui.btnAltaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(self, 0))
        var.ui.btnBajaCli.clicked.connect(lambda: eventos.Eventos.abrirCalendar(self, 1))
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)
        var.ui.btnModifCli.clicked.connect(clientes.Clientes.modifCliente)
        var.ui.btnDelCli.clicked.connect(clientes.Clientes.bajaCliente)
        var.ui.btnGrabarProp.clicked.connect(propiedades.Propiedades.altaPropiedad)
        var.ui.btnModifProp.clicked.connect(propiedades.Propiedades.modifPropiedad)
        var.ui.btnDelProp.clicked.connect(propiedades.Propiedades.bajaPropiedad)
        var.ui.btnFechaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(self, 2))
        var.ui.btnFechaBajaProp.clicked.connect(lambda: eventos.Eventos.abrirCalendar(self, 3))
        var.ui.btnTipoProp.clicked.connect(lambda: propiedades.Propiedades.cargaTablaPropiedades(self, 1))
        var.ui.btnBuscarDniCli.clicked.connect(lambda: clientes.Clientes.cargaClienteDni(self))

        '''
        ZONA DE EVENTOS DE TEXTBOX  
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda: clientes.Clientes.checkDni(var.ui.txtDniCli.text()))
        var.ui.txtEmailCli.editingFinished.connect(
            lambda: clientes.Clientes.checkEmail(self, var.ui.txtEmailCli.text()))
        var.ui.txtMovilCli.editingFinished.connect(lambda: clientes.Clientes.checkTelefono(var.ui.txtMovilCli.text()))
        var.ui.txtPrecioVentaProp.textEdited.connect(lambda: propiedades.Propiedades.checkVentaProp(self))
        var.ui.txtPrecioAlquilerProp.textChanged.connect(lambda: propiedades.Propiedades.checkAlquilerProp(self))
        var.ui.txtFechaBajaProp.textChanged.connect(lambda: propiedades.Propiedades.checkBajaProp(self))

        '''
        ZONA DE EVENTOS DE COMBOX  
        '''
        eventos.Eventos.cargarProv(self)
        var.ui.cmbProvCli.currentIndexChanged.connect(eventos.Eventos.cargarMuniCli)
        var.ui.cmbProvProp.currentIndexChanged.connect(eventos.Eventos.cargarMuniProp)
        eventos.Eventos.cargarTipoPropiedad(self)

        '''
        ZONA DE EVENTOS DE TOOLBAR  
        '''
        var.ui.actionbarSalir.triggered.connect(eventos.Eventos.mensajeSalir)
        var.ui.actionbarLimpiar.triggered.connect(eventos.Eventos.limpiarPanel)
        var.ui.actionbarTipoProp.triggered.connect(eventos.Eventos.abrirTipoProp)
        var.ui.actionFiltrarbarProp.triggered.connect(lambda: propiedades.Propiedades.cargaTablaPropiedades(self, 1))

        '''
        ZONA DE EVENTOS DE CHECKBOX  
        '''
        var.ui.chkHistoriaCli.stateChanged.connect(clientes.Clientes.historicoCli)
        var.ui.chkHistoriaProp.stateChanged.connect(propiedades.Propiedades.historicoProp)
        propiedades.Propiedades.checkBajaProp(self)
        propiedades.Propiedades.checkVentaProp(self)
        propiedades.Propiedades.checkAlquilerProp(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())