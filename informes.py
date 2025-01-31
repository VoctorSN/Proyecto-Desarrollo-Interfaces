import os
from datetime import datetime

from PIL import Image
from PyQt6 import QtSql
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
            if(query0.next()):
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
            var.report.setFont('Helvetica-Bold',size=10)
            var.report.drawString(55,650,str(items[0]))
            var.report.drawString(100,650,str(items[1]))
            var.report.drawString(245, 650, str(items[2]))
            var.report.drawString(350, 650, str(items[3]))
            var.report.drawString(450, 650, str(items[4]))
            var.report.line(50, 645, 525, 645)
            query.prepare("SELECT codigo, dirprop, tipooper, prealquiprop, prevenprop from propiedades where muniprop = '" + municipio + "'")
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
                        operacion = query.value(2).replace("[","").replace("]","").replace("'","")
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
                    operacion = query.value(2).replace("[","").replace("]","").replace("'","")
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


    def footInforme(titulo,paginas):
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


    def reportFacturas(self):
        print("d")