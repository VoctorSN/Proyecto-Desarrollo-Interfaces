import os
from datetime import datetime

from PIL import Image


from PyQt6 import QtWidgets, QtGui, QtCore, QtSql
from pyexpat import features
from reportlab.pdfgen import canvas

import var


class Informes:
    """
    :param self: None
    :type self: None
    :return: False or True
    :rtype:

    """

    @staticmethod
    def reportClientes(self):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfcli = fecha + "_listadoclientes.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado Clientes"
            Informes.topInforme(titulo)

            # Calculate total pages

            paginas = 0
            query0 = QtSql.QSqlQuery()
            query0.exec("select count(*) from clientes")
            if (query0.next()):
                registros = int(query0.value(0))
                paginas = int(registros / 23) + 1
            Informes.footInforme(titulo, paginas)
            items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))  # DNI
            var.report.drawString(100, 650, str(items[1]))  # APELLIDOS
            var.report.drawString(190, 650, str(items[2]))  # NOMBRE
            var.report.drawString(280, 650, str(items[3]))  # MOVIL
            var.report.drawString(360, 650, str(items[4]))  # PROVINCIA
            var.report.drawString(450, 650, str(items[5]))  # MUNICIPIO
            var.report.line(50, 645, 525, 645)
            query0.prepare("SELECT dniCli, apelCli, nomeCli, movilCli, provCli, muniCli from clientes order by apelCli")
            if query0.exec():
                x = 60
                y = 630
                while query0.next():
                    if y <= 90:
                        var.report.setFont('Helvetica-Oblique', size=8)  # HELVETICA OBLIQUE PARA LA FUENTE ITALIC
                        var.report.drawString(450, 80, 'Página siguiente...')
                        var.report.showPage()  # CREAMOS UNA PAGINA NUEVA
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo, paginas)
                        items = ['DNI', 'APELLIDOS', 'NOMBRE', 'MOVIL', 'PROVINCIA', 'MUNICIPIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))  # DNI
                        var.report.drawString(100, 650, str(items[1]))  # APELLIDOS
                        var.report.drawString(190, 650, str(items[2]))  # NOMBRE
                        var.report.drawString(280, 650, str(items[3]))  # MOVIL
                        var.report.drawString(360, 650, str(items[4]))  # PROVINCIA
                        var.report.drawString(450, 650, str(items[5]))  # MUNICIPIO
                        var.report.line(50, 645, 525, 645)
                        x = 60
                        y = 630

                    var.report.setFont('Helvetica', size=8)
                    dni = '****' + str(query0.value(0)[4:7] + '****')
                    var.report.drawCentredString(x + 5, y, str(dni))  # DNI
                    var.report.drawString(x + 40, y, str(query0.value(1)))  # APELLIDOS
                    var.report.drawString(x + 130, y, str(query0.value(2)))  # NOMBRE
                    var.report.drawString(x + 220, y, str(query0.value(3)))  # MOVIL
                    var.report.drawString(x + 310, y, str(query0.value(4)))  # PROVINCIA
                    var.report.drawString(x + 390, y, str(query0.value(5)))  # MUNICIPIO
                    y = y - 25.

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as error:
            print(error)

    @staticmethod
    def reportPropiedades(municipio):
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfprop = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfprop)
            var.report = canvas.Canvas(pdf_path)
            titulo = "Listado Propiedades"
            Informes.topInforme(titulo)

            # Calculate total pages

            paginas = 0
            query = QtSql.QSqlQuery()
            query.exec("select count(*) from propiedades where muniprop = '" + municipio + "'")
            if (query.next()):
                registros = int(query.value(0))
                paginas = int(registros / 23) + 1
            Informes.footInforme(titulo, paginas)
            items = ['CODIGO', 'DIRECCIÓN', 'TIPO OPERACION', 'PRECIO ALQUILER', 'PRECIO VENTA']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(245, 650, str(items[2]))
            var.report.drawString(350, 650, str(items[3]))
            var.report.drawString(450, 650, str(items[4]))
            var.report.line(50, 645, 525, 645)
            query.prepare(
                "SELECT codigo, dirprop, tipooper, prealquiprop, prevenprop from propiedades where muniprop = '" + municipio + "'")
            if query.exec():
                x = 60
                y = 630
                while query.next():
                    if y <= 90:
                        var.report.setFont('Helvetica-Oblique', size=8)  # HELVETICA OBLIQUE PARA LA FUENTE ITALIC
                        var.report.drawString(450, 80, 'Página siguiente...')
                        var.report.showPage()  # CREAMOS UNA PAGINA NUEVA
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo, paginas)
                        items = ['CODIGO', 'DIRECCIÓN', 'TIPO OPERACION', 'PRECIO ALQUILER', 'PRECIO VENTA']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))  # DNI
                        var.report.drawString(100, 650, str(items[1]))  # APELLIDOS
                        operacion = query.value(2).replace("[", "").replace("]", "").replace("'", "")
                        var.report.drawString(245, y, operacion)  # MOVIL
                        alquiler = "-" if not str(query.value(3)) else str(query.value(3))
                        var.report.drawString(350, y, alquiler)  # PROVINCIA
                        compra = "-" if not str(query.value(4)) else str(query.value(4))
                        var.report.drawString(450, y, compra)  # MUNICIPIO
                        var.report.line(50, 645, 525, 645)
                        x = 60
                        y = 630

                    var.report.setFont('Helvetica', size=8)
                    var.report.drawString(55, y, str(query.value(0)))  # APELLIDOS
                    var.report.drawString(100, y, str(query.value(1)))  # NOMBRE
                    operacion = query.value(2).replace("[", "").replace("]", "").replace("'", "")
                    var.report.drawString(245, y, operacion)  # MOVIL
                    alquiler = "-" if not str(query.value(3)) else str(query.value(3))
                    var.report.drawString(350, y, alquiler + "€")  # PROVINCIA
                    compra = "-" if not str(query.value(4)) else str(query.value(4))
                    var.report.drawString(450, y, compra + "€")  # MUNICIPIO
                    y = y - 25.

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfprop):
                    os.startfile(pdf_path)
        except Exception as error:
            print(error)


    def reportFacturas(self):
        factura = var.ui.txtNumFac.text()
        if factura == "":
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setWindowTitle("Error generando Factura")
            mbox.setText("No se encontro la factura")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()
            return None
        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.makedirs(rootPath)
            fecha = datetime.today()
            fecha = fecha.strftime("%Y_%m_%d_%H_%M_%S")
            nomepdfprop = fecha + "_listadofacturas.pdf"
            pdf_path = os.path.join(rootPath, nomepdfprop)
            var.report = canvas.Canvas(pdf_path)
            query = QtSql.QSqlQuery()
            query.exec("select fechafac from facturas where id = '" + factura + "'")
            query.next()
            fechaFac = str(query.value(0))
            var.report.setFont('Helvetica', size=9)
            var.report.drawString(55, 670, 'Fecha Factura: ' + fechaFac)
            titulo = "Listado Factura " + factura
            Informes.topInforme(titulo)

            # Calculate total pages

            paginas = 0
            query.exec("select count(*) from ventas where idFactura = '" + factura + "'")
            if (query.next()):
                registros = int(query.value(0))
                paginas = int(registros / 23) + 1
            Informes.footInforme(titulo, paginas)
            items = ['VENTA', 'PROPIEDAD', 'TIPO PROPIEDAD', 'LOCALIDAD', 'DIRECCION', 'PRECIO']
            var.report.setFont('Helvetica-Bold', size=10)
            var.report.drawString(55, 650, str(items[0]))
            var.report.drawString(100, 650, str(items[1]))
            var.report.drawString(170, 650, str(items[2]))
            var.report.drawString(285, 650, str(items[3]))
            var.report.drawString(380, 650, str(items[4]))
            var.report.drawString(475, 650, str(items[5]))
            var.report.line(50, 645, 525, 645)
            query.prepare(
                "SELECT v.id, p.codigo, p.tipoprop, p.muniprop, p.dirprop, p.prevenprop "
                " FROM ventas AS v"
                " INNER JOIN propiedades AS p ON v.idPropiedad = p.codigo"
                " WHERE idFactura = '" + factura + "'")
            if query.exec():
                y = 630
                total = 0
                while query.next():
                    if y <= 90:
                        var.report.setFont('Helvetica-Oblique', size=8)  # HELVETICA OBLIQUE PARA LA FUENTE ITALIC
                        var.report.drawString(450, 80, 'Página siguiente...')
                        var.report.showPage()  # CREAMOS UNA PAGINA NUEVA
                        Informes.topInforme(titulo)
                        Informes.footInforme(titulo, paginas)
                        items = ['VENTA', 'PROPIEDAD', 'TIPO PROPIEDAD', 'LOCALIDAD', 'DIRECCION', 'PRECIO']
                        var.report.setFont('Helvetica-Bold', size=10)
                        var.report.drawString(55, 650, str(items[0]))
                        var.report.drawString(100, 650, str(items[1]))
                        var.report.drawString(170, 650, str(items[2]))
                        var.report.drawString(285, 650, str(items[3]))
                        var.report.drawString(380, 650, str(items[4]))
                        var.report.drawString(475, 650, str(items[5]))
                        var.report.line(50, 645, 525, 645)
                        y = 630

                    var.report.setFont('Helvetica', size=8)
                    var.report.drawCentredString(70, y, str(query.value(0)))
                    var.report.drawCentredString(115, y, str(query.value(1)))
                    var.report.drawString(170, y, str(query.value(2)))
                    var.report.drawString(285, y, query.value(3))
                    var.report.drawString(380, y, query.value(4))
                    compra = "-" if not str(query.value(5)) else str(query.value(5)) + '€'
                    var.report.drawRightString(525, y, compra)
                    y = y - 25.
                    total += query.value(5)

                var.report.line(50, 110, 525, 110)
                var.report.drawString(400, 100, "Subtotal: ")
                var.report.drawString(400, 80, "Impuestos: ")
                var.report.drawString(400, 60, "Total: ")
                var.report.drawRightString(525, 100, str(total) + "€")
                var.report.drawRightString(525, 80, str(round(total*0.1,3)) + "€")
                var.report.drawRightString(525, 60, str(round(total*1.1,3)) + "€")

            var.report.save()
            for file in os.listdir(rootPath):
                if file.endswith(nomepdfprop):
                    os.startfile(pdf_path)
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Information)
            mbox.setWindowTitle("Aviso")
            mbox.setText("Se creado el informe.")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.button(QtWidgets.QMessageBox.StandardButton.Ok).setText('Aceptar')
            mbox.exec()
        except Exception as error:
            mbox = QtWidgets.QMessageBox()
            mbox.setIcon(QtWidgets.QMessageBox.Icon.Warning)
            mbox.setWindowTitle("Error generando Factura")
            mbox.setText("Ocurrio un error en la generacion de la factura")
            mbox.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            mbox.exec()
            print(error)

    @staticmethod
    def reportMensualidadActual(idMensualidad):
        """
        Método para generar un informe con los datos de la mensualidad.
        """

        try:
            rootPath = '.\\informes'
            if not os.path.exists(rootPath):
                os.mkdirs(rootPath)
            titulo = "Datos de la mensualidad: " + str(idMensualidad)
            fecha = datetime.today().strftime('%Y_%m_%d_%H_%M_%S')
            nomepdfcli = fecha + "_listadopropiedades.pdf"
            pdf_path = os.path.join(rootPath, nomepdfcli)
            var.report = canvas.Canvas(pdf_path)
            Informes.topInformeMensualidad(titulo)
            Informes.footInformeMensualidad(titulo)

            # Lista de títulos
            items = ['Mes de la mensualidad - ', 'Precio - ', 'DNI cliente - ',
                     'Nombre del Cliente - ',
                     'Apellidos del cliente - ', "Direccion de facturacion - ", "Localidad de la propiedad - "]

            var.report.setFont('Helvetica-Bold', size=10)
            y = 595  # Empezamos desde la parte superior

            # Dibujar los títulos en negrita en la primera columna
            for i, item in enumerate(items):
                var.report.drawString(55, y, item)  # Títulos a la izquierda
                y -= 30  # Espacio entre títulos

            query = QtSql.QSqlQuery()
            query.prepare("""
                                                SELECT    m.id  as "idMensualidad",
                                                          m.mes as "mesMensualidad",
                                                          p.prealquiprop as "precioMensualidad",
                                                          c.dniCli as "dniCliente",
                                                          cl.nomecli as "nombreCliente",
                                                          cl.apelcli as "apellidosCliente",
                                                          cl.dircli as "direccionCliente",
                                                          p.muniprop as "localidadPropiedad",
                                                          m.pagado as "Abono"

                                            FROM mensualidades AS m
                                            INNER JOIN contratos AS c
                                                ON c.id = m.contrato
                                            INNER JOIN propiedades AS p
                                                ON c.prop = p.codigo
                                            INNER JOIN clientes AS cl
                                                ON cl.dnicli = c.dniCli
                                            WHERE m.ID = :idMensualidad;
                                                """)
            query.bindValue(":idMensualidad", idMensualidad)
            if query.exec():
                y = 625
                print("Pre-while")
                while query.next():
                    if y <= 90:
                        var.report.setFont('Helvetica-Oblique', size=9)
                        var.report.drawString(450, 70, "Pagina siguiente")
                        var.report.showPage()
                        Informes.footInformeMensualidad(titulo)
                        Informes.topInformeMensualidad(titulo)

                        y = 625

                    var.report.setFont('Helvetica', size=9)
                    # Ahora intercalamos los datos con los títulos, de modo que la información va a la derecha
                    var.report.drawString(175, y - 30, str(query.value(1)).title())  # MES MENSUALIDAD
                    var.report.drawString(98, y - 60, str(query.value(2)) + " €")  # PRECIO MENSUALIDAD
                    var.report.drawString(117, y - 90, str(query.value(3)))  # DNI CLIENTE
                    var.report.drawString(155, y - 120, str(query.value(4)))  # NOMBRE CLIENTE
                    var.report.drawString(160, y - 150, str(query.value(5)))  # APELLIDOS CLIENTE
                    var.report.drawString(180, y - 180, str(query.value(6)))  # DIRECCIÓN CLIENTE
                    var.report.drawString(190, y - 210, str(query.value(7)))  # LOCALIDAD DE LA PROPIEDAD
                    var.report.line(50, y - 240, 525, y - 240)  # Línea justo después de la última fila

                    abonadobbdd = query.value(8)
                    abono = "NO ABONADO"

                    if abonadobbdd:
                        abono = "ABONADO"

                    var.report.setFont('Helvetica-Bold', size=40)  # Fuente más grande para ABONO
                    var.report.setFillColorRGB(1, 0, 0)
                    var.report.drawString(65, y - 300, str(abono).upper())  # ABONO en mayúsculas y grande
                    var.report.line(50, y - 330, 525, y - 330)  # Línea justo después de la última fila

                    var.report.setFont('Helvetica', size=8)  # Fuente más pequeña para la retaila
                    var.report.setFillColorRGB(0, 0, 0)  # Color negro para el texto

                    # Retaila de texto legal
                    retaila = """
                                                INFORMACIÓN LEGAL:
                                                1. Este informe sigue la Ley 22/2023 sobre la Protección de Datos. Si no te gusta, reinicia el sistema.
                                                2. Los datos están protegidos por el RGPD. Los hackers no están invitados.
                                                3. En caso de error, solo presiona F5 y todo volverá a la normalidad.
                                                4. No es necesario un antivirus para leer este informe... a menos que se imprima en papel.
                                                5. La divulgación está prohibida, pero si lo compartes con un bot, está bien (siempre que sea un bot de confianza).
                                                6. Si ves un error, no te preocupes, el código es todavía "beta".
                                                7. No necesitas ser un administrador de red para entender esto, solo un humano.
                                                8. Este informe es solo un "placeholder" para el contrato real que llegará pronto.
                                                9. Las disputas se resolverán en los tribunales, no en una consola de comandos.
                                                10. Nuestra política de privacidad está más segura que un servidor SSH con dos factores.
                                                11. La información puede ser más larga que un log de servidor. Toma un descanso.
                                                12. Para acceso, contacta con nuestro "admin" o simplemente pide a tu asistente virtual.
                                                13. El acceso está restringido, pero si tienes un script autorizado, adelante.
                                                14. Este informe no es un contrato, solo un "README" preliminar.
                                                15. Las modificaciones se rastrean como commits en nuestro repositorio.
                                                16. Si no entiendes algo, prueba con Google, o con "man página".
                                                17. El informe se guardó en formato PDF, no en un floppy de 1.44MB.
                                                18. Los cambios se reflejarán en el próximo "push" de la política de privacidad.
                                                19. Este informe es válido solo si se lee en la terminal de un sistema UNIX.
                                                20. Cualquier error se corregirá con un parche rápido y un café.
                                                21. Si ves "404", es que el informe no está disponible... o no tienes permisos.

                        """

                    # Dibujamos la retaila en líneas separadas
                    lines = retaila.strip().split('\n')
                    line_y = y - 350  # Comenzamos justo después de la línea de ABONO

                    for line in lines:
                        var.report.drawString(50, line_y, line.strip())  # Dibuja cada línea
                        line_y -= 10  # Espaciado entre líneas




            else:

                print(query.lastError().text())

            var.report.save()
            rootPath = '.\\informes'

            for file in os.listdir(rootPath):
                if file.endswith(nomepdfcli):
                    os.startfile(pdf_path)
        except Exception as e:
            print(e)

    def topInformeMensualidad(titulo):
        """

        """
        try:
            ruta_logo = '.\\img\\logo.ico'
            logo = Image.open(ruta_logo)

            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'InmoTeis')
                var.report.drawString(200, 680, titulo)
                var.report.line(50, 665, 525, 665)

                var.report.drawImage(ruta_logo, 480, 725, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF: A12345678')
                var.report.drawString(55, 755, 'Avda. Galicia - 101')
                var.report.drawString(55, 740, 'Chapela, Vigo - 36320 - España')
                var.report.drawString(55, 725, 'Teléfono: 654 333 979')
                var.report.drawString(55, 710, 'e-mail: evanchapela@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInformeMensualidad(titulo):
        """

        """
        try:

            total_pages = 0
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today().strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)


    def topInforme(titulo):
        try:
            ruta_logo = '.\\img\\logo.png'
            logo = Image.open(ruta_logo)

            # Asegúrate de que el objeto 'logo' sea de tipo 'PngImageFile'
            if isinstance(logo, Image.Image):
                var.report.line(50, 800, 525, 800)
                var.report.setFont('Helvetica-Bold', size=14)
                var.report.drawString(55, 785, 'Inmobiliaria Teis')
                var.report.drawString(230, 670, titulo)
                var.report.line(50, 665, 525, 665)

                # Dibuja la imagen en el informe
                var.report.drawImage(ruta_logo, 480, 725, width=40, height=40)

                var.report.setFont('Helvetica', size=9)
                var.report.drawString(55, 770, 'CIF: A12345678')
                var.report.drawString(55, 755, 'Avda. Galicia - 101')
                var.report.drawString(55, 740, 'Vigo - 36216 - España')
                var.report.drawString(55, 725, 'Teléfono: 986 132 456')
                var.report.drawString(55, 710, 'e-mail: cartesteisr@mail.com')
            else:
                print(f'Error: No se pudo cargar la imagen en {ruta_logo}')
        except Exception as error:
            print('Error en cabecera informe:', error)

    def footInforme(titulo, paginas):
        try:
            var.report.line(50, 50, 525, 50)
            fecha = datetime.today()
            fecha = fecha.strftime('%d-%m-%Y %H:%M:%S')
            var.report.setFont('Helvetica-Oblique', size=7)
            var.report.drawString(50, 40, str(fecha))
            var.report.drawString(250, 40, str(titulo))
            var.report.drawString(490, 40, str('Página %s' % var.report.getPageNumber() + '/' + str(paginas)))

        except Exception as error:
            print('Error en pie informe de cualquier tipo: ', error)