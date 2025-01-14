from datetime import datetime

from PyQt6.QtCore import Qt

import conexion
import eventos
import informes
import propiedades
import var
from dlgAbout import Ui_dlgAbout
from dlgCalendar import *
from dlg_GestionProp import Ui_dlg_TipoProp
from dlg_listadoPropiedades import Ui_dlg_ListadoProp


class Calendar(QtWidgets.QDialog):
    def __init__(self):
        super(Calendar, self).__init__()
        var.uicalendar = Ui_dlgCalendar()
        var.uicalendar.setupUi(self)
        dia = datetime.now().day
        mes = datetime.now().month
        ano = datetime.now().year

        var.uicalendar.Calendar.setSelectedDate((QtCore.QDate(ano, mes, dia)))
        var.uicalendar.Calendar.clicked.connect(eventos.Eventos.cargaFecha)

class FileDialogAbrir(QtWidgets.QFileDialog):
    def __init__(self):
        super(FileDialogAbrir, self).__init__()

class dlgTipoProp(QtWidgets.QDialog):
    def __init__(self):
        super(dlgTipoProp,self).__init__()
        self.ui = Ui_dlg_TipoProp()
        self.ui.setupUi(self)
        self.ui.btnAltaTipoProp.clicked.connect(propiedades.Propiedades.altaTipoPropiedad)
        self.ui.btnDelTipoProp.clicked.connect(propiedades.Propiedades.bajaTipoPropiedad)

class dlgAbout(QtWidgets.QDialog):
    def __init__(self):
        super(dlgAbout, self).__init__()
        self.ui = Ui_dlgAbout()
        self.ui.setupUi(self)
        self.ui.btnSalir.clicked.connect(self.close)

class dlg_listadoPropiedades(QtWidgets.QDialog):
    def __init__(self):
        super(dlg_listadoPropiedades,self).__init__()
        self.ui = Ui_dlg_ListadoProp()
        self.ui.setupUi(self)
        provincias = conexion.Conexion.listaMunicipiosTexto(self)
        self.ui.chkElegirProp.addItem("")
        self.ui.chkElegirProp.addItems(provincias)
        print(provincias)

        completer = QtWidgets.QCompleter(provincias,self)
        completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)

        self.ui.chkElegirProp.setCompleter(completer)

        self.ui.btnGenerarInforme.clicked.connect(self.onBtnClicked)

    def onBtnClicked(self):
        texto = self.ui.chkElegirProp.currentText()
        informes.Informes.reportPropiedades(texto)
        self.accept()