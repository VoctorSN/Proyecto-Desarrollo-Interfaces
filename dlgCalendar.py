# Form implementation generated from reading ui file './templates/dlgCalendar.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_dlgCalendar(object):
    def setupUi(self, dlgCalendar):
        dlgCalendar.setObjectName("dlgCalendar")
        dlgCalendar.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        dlgCalendar.resize(312, 185)
        dlgCalendar.setMinimumSize(QtCore.QSize(312, 185))
        dlgCalendar.setMaximumSize(QtCore.QSize(312, 185))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("./templates\\../img/calendar.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        dlgCalendar.setWindowIcon(icon)
        dlgCalendar.setModal(True)
        self.Calendar = QtWidgets.QCalendarWidget(parent=dlgCalendar)
        self.Calendar.setGeometry(QtCore.QRect(0, 0, 312, 183))
        self.Calendar.setMinimumSize(QtCore.QSize(312, 183))
        self.Calendar.setMaximumSize(QtCore.QSize(312, 183))
        self.Calendar.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.VerticalHeaderFormat.NoVerticalHeader)
        self.Calendar.setNavigationBarVisible(True)
        self.Calendar.setDateEditEnabled(True)
        self.Calendar.setObjectName("Calendar")

        self.retranslateUi(dlgCalendar)
        QtCore.QMetaObject.connectSlotsByName(dlgCalendar)

    def retranslateUi(self, dlgCalendar):
        _translate = QtCore.QCoreApplication.translate
        dlgCalendar.setWindowTitle(_translate("dlgCalendar", "Seleccione Fecha"))
