from datetime import datetime

import eventos
import var
from dlgCalendar import *
from dlg_GestionProp import Ui_dlg_TipoProp


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
        super(dlgTipoProp).__init__()
        var.dlgGestion = Ui_dlg_TipoProp()
        var.dlgGestion.setupUi(self)
