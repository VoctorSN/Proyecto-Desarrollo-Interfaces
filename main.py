import clientes
import conexion
import eventos
import styles
from VenPrincipal import *
import sys
import var
from VenPrincipal import Ui_venPrincipal

class Main(QtWidgets.QMainWindow):

    def __init__(self):
        super(Main, self).__init__()
        var.ui = Ui_venPrincipal()
        var.ui.setupUi(self)
        self.setStyleSheet(styles.load_stylesheet())
        conexion.Conexion.db_conexion(self)
        eventos.Eventos.cargarProv(self)
        eventos.Eventos.cargarMun(self,var.ui.cmbProvCli.currentText())

        '''
        ZONA DE EVENTOS DEL MENUBAR
        '''
        var.ui.actionSalir.triggered.connect(eventos.Eventos.mensajeSalir)

        '''
        ZONA DE EVENTOS DE BOTONES
        '''
        var.ui.btnGrabarCli.clicked.connect(clientes.Clientes.altaCliente)

        '''
        ZONA DE EVENTOS DE TEXTBOX  
        '''
        var.ui.txtDniCli.editingFinished.connect(lambda : clientes.Clientes.checkDni(var.ui.txtDniCli.text()))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Main()
    window.showMaximized()
    sys.exit(app.exec())
