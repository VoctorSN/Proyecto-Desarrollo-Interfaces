from PyQt6 import QtWidgets, QtGui, QtCore

import conexion
import var
from informes import Informes
from propiedades import Propiedades


class Contrato():

    botonesdel = []
    botonespagar = []
    botonesimpresion = []

    def altaContrato(self):
        nuevoContrato = [
                         var.ui.txtFechaAlq.text(),var.ui.txtDniAlq.text(),
                         var.ui.txtPropiedadAlq.text(),var.ui.txtVendedorAlq.text(),
                         var.ui.txtFechaInicioMens.text(),var.ui.txtFechaFinMens.text()
                         ]

        mensajes_error = [
            "Falta agregar la fecha",
            "Falta agregar el cliente",
            "Falta agregar la propiedad",
            "Falta agregar al vendedor",
            "Falta agregar la fecha de inicio",
            "Falta agregar la fecha de fin"
        ]

        for i, dato in enumerate(nuevoContrato):
            if dato == '':
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en los datos")
                mbox.setText(mensajes_error[i])
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return

        try:
            if not conexion.Conexion.isDisponible(self, nuevoContrato[2]):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                mbox.setWindowTitle("Error en los datos")
                mbox.setText("No puedes alquilar esta propiedad, porque no esta Disponible")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()
                return
            if conexion.Conexion.altaContrato(self, nuevoContrato):
                mbox = QtWidgets.QMessageBox()
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                mbox.setWindowTitle("Aviso")
                mbox.setText("Se ha insertado el contrato correctamente.")
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                mbox.exec()
                Contrato.cargaTablaContratos(self)
            else:
                mbox = QtWidgets.QMessageBox()
                mbox.setWindowTitle("Error")
                mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                mbox.setText('La fecha de inicio tiene que ser menor a la de fin.')
                mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                mbox.exec()

        except Exception as e:
            print(e)
            mbox = QtWidgets.QMessageBox()
            mbox.setWindowTitle("Error")
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            mbox.setText('Error al insertar el contrato. Intente nuevamente.')
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()
        Contrato.cargaTablaContratos(self)
        Propiedades.cargaTablaPropiedades(self,0)

    def cargaTablaContratos(self):
        try:
            listado = conexion.Conexion.listadoContratos(self)


            var.ui.tabContratos.setRowCount(0)

            i = 0

            for registro in listado:
                var.ui.tabContratos.setRowCount(i + 1)



                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Contrato.botonesdel.append(QtWidgets.QPushButton())
                Contrato.botonesdel[-1].setFixedSize(30, 20)
                Contrato.botonesdel[-1].setIcon(QtGui.QIcon("./img/papelera.ico"))
                Contrato.botonesdel[-1].setStyleSheet("background-color: #efefef;")
                Contrato.botonesdel[-1].clicked.connect(lambda checked: Contrato.eliminar_contrato(self, str(registro[0])))
                layout.addWidget(Contrato.botonesdel[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)

                var.ui.tabContratos.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabContratos.setItem(i, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabContratos.setCellWidget(i, 2, container)

                var.ui.tabContratos.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabContratos.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1


            if var.ui.tabContratos.rowCount() == 0:
                return Contrato.setTablaVaciaContrato(self)

        except Exception as e:
            print("Error cargar tabla contrato", e)

    def setTablaVaciaContrato(self):
        var.ui.tabContratos.setRowCount(1)
        var.ui.tabContratos.setItem(0, 1, QtWidgets.QTableWidgetItem("No hay contratos"))
        var.ui.tabContratos.item(0, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignCenter)
        return

    def setTablaVaciaMensualidades(self):
        var.ui.tabMensualidadesAlq.setRowCount(1)
        var.ui.tabMensualidadesAlq.setItem(0, 3, QtWidgets.QTableWidgetItem("No hay mensualidades"))
        var.ui.tabMensualidadesAlq.item(0, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignLeft.AlignCenter)
        return


    def cargaOneContrato(self):
        try:
            fila = var.ui.tabContratos.selectedItems()
            datos = [dato.text() for dato in fila]
            if datos[0] == "No hay Contratos":
                return
            Contrato.cargarContrato(self,datos)



        except Exception as e:
            print("Error cargar Contrato", e)

    def cargarContrato(self, datos):
        registro = conexion.Conexion.datosOneContrato(str(datos[0]))
        listado = [
            var.ui.txtNumContratoAlq, var.ui.txtFechaAlq,
            var.ui.txtFechaInicioMens,var.ui.txtFechaFinMens,
            var.ui.txtDniAlq, var.ui.txtPropiedadAlq,
            var.ui.txtVendedorAlq
        ]
        for i, casilla in enumerate(listado):
            if isinstance(casilla, QtWidgets.QComboBox):
                casilla.setCurrentText(str(registro[i]))
            elif isinstance(casilla, QtWidgets.QLabel):
                casilla.setText(str(registro[i]))
                continue
            elif isinstance(casilla, QtWidgets.QLineEdit):
                casilla.setText(str(registro[i]))
            else:
                casilla.setText(str(registro[i]))
        return registro

    def cargaOneMensualidad(self):
        try:
            fila = var.ui.tabMensualidadesAlq.selectedItems()
            datos = [dato.text() for dato in fila]
            if datos[0] == "No hay Mensualidades":
                return
            registro = conexion.Conexion.datosOneMensualidad(str(datos[0]))

            listado = [
                var.ui.txtNumContratoMens, var.ui.txtPropiedadMens,
                var.ui.txtFechaFinMens, var.ui.txtFechaInicioMens
            ]

            for i, casilla in enumerate(listado):
                if isinstance(casilla, QtWidgets.QComboBox):
                    casilla.setCurrentText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLabel):
                    casilla.setText(str(registro[i]))
                elif isinstance(casilla, QtWidgets.QLineEdit):
                    casilla.setText(str(registro[i]))
                else:
                    casilla.setText(str(registro[i]))

            Contrato.cargarContrato(self, [registro[4]])


        except Exception as e:
            print("Error cargar Contrato", e)

    def eliminar_contrato(self, idContrato):
        try:
            msgbox = QtWidgets.QMessageBox()
            msgbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
            msgbox.setWindowTitle('Aviso')
            msgbox.setText("Desea Eliminar el Contrato")
            msgbox.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
            msgbox.button(QtWidgets.QMessageBox.StandardButton.Yes).setText('Si')
            idPropiedad = conexion.Conexion.datosOneContrato(idContrato)[5]
            if msgbox.exec():
                if conexion.Conexion.checkMensualidadesPagadas(self, int(idContrato)) != []:
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    msgbox.setWindowTitle('Aviso')
                    msgbox.setText("No se puede eliminar un contrato con mensualidades pagadas")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    msgbox.exec()
                    return
                if conexion.Conexion.delContrato(self, idPropiedad, int(idContrato)):
                    msgbox = QtWidgets.QMessageBox()
                    msgbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    msgbox.setWindowIcon(QtGui.QIcon('./img/logo.ico'))
                    msgbox.setWindowTitle('Aviso')
                    msgbox.setText("Contrato Eliminado")
                    msgbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
                    msgbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
                    msgbox.exec()
                    Contrato.cargaTablaContratos(self)
            else:
                msgbox.hide()
        except Exception as error:
            print("Error Eliminar contrato ", error)


    def cargaTablaMensualidades(self):
        contrato = var.ui.txtNumContratoAlq.text()
        if contrato=='':
            return Contrato.setTablaVaciaMensualidades(self)
        try:

            listado = conexion.Conexion.listadomensualidades(self, int(contrato))

            var.ui.tabMensualidadesAlq.setRowCount(0)

            i = 0

            for registro in listado:
                var.ui.tabMensualidadesAlq.setRowCount(i + 1)

                container = QtWidgets.QWidget()
                layout = QtWidgets.QVBoxLayout()
                Contrato.botonespagar.append(QtWidgets.QPushButton())
                Contrato.botonespagar[-1].setFixedSize(30, 20)
                Contrato.botonespagar[-1].setIcon(QtGui.QIcon("./img/cruz.png"))
                if registro[4]:
                    Contrato.botonespagar[-1].setIcon(QtGui.QIcon("./img/tick.png"))
                Contrato.botonespagar[-1].setStyleSheet("background-color: #efefef;")
                Contrato.botonespagar[-1].clicked.connect(
                    lambda checked, idMensualidad=registro[0]: Contrato.pagarMensualidad(self, idMensualidad))
                layout.addWidget(Contrato.botonespagar[-1])
                layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout.setContentsMargins(0, 0, 0, 0)
                layout.setSpacing(0)
                container.setLayout(layout)


                container1 = QtWidgets.QWidget()
                layout1 = QtWidgets.QVBoxLayout()
                Contrato.botonesimpresion.append(QtWidgets.QPushButton())
                Contrato.botonesimpresion[-1].setFixedSize(30, 20)
                Contrato.botonesimpresion[-1].setIcon(QtGui.QIcon("./img/impresora.png"))
                Contrato.botonesimpresion[-1].setStyleSheet("background-color: #efefef;")
                Contrato.botonesimpresion[-1].clicked.connect(
                    lambda checked, idMensualidad=registro[0]: Informes.reportMensualidadActual(idMensualidad))
                layout1.addWidget(Contrato.botonesimpresion[-1])
                layout1.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                layout1.setContentsMargins(0, 0, 0, 0)
                layout1.setSpacing(0)
                container1.setLayout(layout1)

                var.ui.tabMensualidadesAlq.setItem(i, 0, QtWidgets.QTableWidgetItem(str(registro[0])))
                var.ui.tabMensualidadesAlq.setItem(i, 1, QtWidgets.QTableWidgetItem(str(registro[1])))
                var.ui.tabMensualidadesAlq.setItem(i, 2, QtWidgets.QTableWidgetItem(str(registro[2])))
                var.ui.tabMensualidadesAlq.setItem(i, 3, QtWidgets.QTableWidgetItem(str(registro[3])))
                var.ui.tabMensualidadesAlq.setCellWidget(i, 4, container)
                var.ui.tabMensualidadesAlq.setCellWidget(i, 5, container1)

                var.ui.tabMensualidadesAlq.item(i, 0).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabMensualidadesAlq.item(i, 1).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabMensualidadesAlq.item(i, 2).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                var.ui.tabMensualidadesAlq.item(i, 3).setTextAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
                i += 1

            if var.ui.tabMensualidadesAlq.rowCount() == 0:
                return Contrato.setTablaVaciaMensualidades(self)

        except Exception as e:
            print("Error cargar tabla mensualidades", e)


    def pagarMensualidad(self,idMensualidad):
        conexion.Conexion.pagarMensualidad(self, idMensualidad)
        Contrato.cargaTablaMensualidades(self)