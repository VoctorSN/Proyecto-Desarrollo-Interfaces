import os
import sqlite3
from datetime import datetime

from PyQt6 import QtSql, QtWidgets

import var


class Conexion:
    '''

    método de una clase que no depende de una instancia específica de esa clase. 
    Se puede llamarlo directamente a través de la clase, sin necesidad de crear un objeto de esa clase. 
    Es útil en comportamientos o funcionalidades que son más a una clase en general que a una instancia en particular.
    
    '''

    @staticmethod
    def db_conexion(self):
        """

        :param self:
        :type self:
        :return: True or False depending on the connection status
        :rtype: bool

        Metodo que se encarga de conectar con la base de datos y devuelve un booleano dependiendo de si se ha conectado o no
        """
        # Verifica si el archivo de base de datos existe
        if not os.path.isfile('bbdd.sqlite'):
            QtWidgets.QMessageBox.critical(None, 'Error', 'El archivo de la base de datos no existe.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False
        # Crear la conexión con la base de datos SQLite
        db = QtSql.QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('bbdd.sqlite')

        if db.open():
            # Verificar si la base de datos contiene tablas
            query = QtSql.QSqlQuery()
            query.exec("SELECT name FROM sqlite_master WHERE type='table';")

            if not query.next():  # Si no hay tablas
                QtWidgets.QMessageBox.critical(None, 'Error', 'Base de datos vacía o no válida.',
                                               QtWidgets.QMessageBox.StandardButton.Cancel)
                return False
            else:
                QtWidgets.QMessageBox.information(None, 'Aviso', 'Conexión Base de Datos realizada',
                                                  QtWidgets.QMessageBox.StandardButton.Ok)
                return True
        else:
            QtWidgets.QMessageBox.critical(None, 'Error', 'No se pudo abrir la base de datos.',
                                           QtWidgets.QMessageBox.StandardButton.Cancel)
            return False

    @staticmethod
    def listaProv(self):
        """

        :param self:
        :type self:
        :return: the list of provincias
        :rtype: list

        Metodo que devuelve una lista con las provincias
        """
        listaprov = []
        query = QtSql.QSqlQuery()
        query.prepare('SELECT * FROM provincias')
        if query.exec():
            while query.next():
                listaprov.append(query.value(1))

        return listaprov

    @staticmethod
    def listaMunicipios(provincia):
        """

        :param provincia: la provincia por la que buscar los municipios
        :type provincia: str
        :return: la lista de municipios de una provincia
        :rtype: list

        Metodo que devuelve una lista con los municipios de una provincia que le pasas por parametro
        """
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT * FROM municipios where idprov = (select idprov from provincias where provincia = :provincia)")
            query.bindValue(":provincia", provincia)
            if query.exec():
                while query.next():
                    listamunicipios.append(query.value(1))
            return listamunicipios
        except Exception as error:
            print("error lista muni: ", error)

    def altaCliente(self, nuevoCli):
        """

        :param nuevoCli: datos a insertar de un nuevo cliente
        :type nuevoCli: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un cliente cogiendo los datos de este de la lista que le pasas por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO CLIENTES (dnicli, altacli, apelcli, nomecli, emailcli, movilcli, dircli, provcli, municli) "
                " VALUES (:dnicli, :altacli, :apelcli, :nomecli, :emailcli, :movilcli, :dircli, :provcli, :municli)")
            query.bindValue(":dnicli", str(nuevoCli[0]))
            query.bindValue(":altacli", str(nuevoCli[1]))
            query.bindValue(":apelcli", str(nuevoCli[2]))
            query.bindValue(":nomecli", str(nuevoCli[3]))
            query.bindValue(":emailcli", str(nuevoCli[4]))
            query.bindValue(":movilcli", str(nuevoCli[5]))
            query.bindValue(":dircli", str(nuevoCli[6]))
            query.bindValue(":provcli", str(nuevoCli[7]))
            query.bindValue(":municli", str(nuevoCli[8]))
            if query.exec():
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en alta cliente: ", error)

    def listadoClientes(self):
        """

        :return: lista de los clientes no dados de baja o ambos dependiendo de la variable historico
        :rtype: list

        Metodo que devuelve una lista con los datos de los clientes, coge los datos de todos
         o solo de los que no están dados de baja dependiendo del estado de la variable historico
        """
        try:
            listado = []
            if var.historico == 1:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes WHERE bajacli is NULL ORDER BY apelcli, nomecli ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
            elif var.historico == 0:
                query = QtSql.QSqlQuery()
                query.prepare("SELECT * FROM clientes ORDER BY apelcli, nomecli ASC ")
                if query.exec():
                    while query.next():
                        fila = [query.value(i) for i in range(query.record().count())]
                        listado.append(fila)
                return listado
        except Exception as e:
            print("Error listado en conexion", e)

    def datosOneCliente(dni):
        """

        :param dni: dni por el que buscar los datos de un cliente
        :type dni: string
        :return: datos de un cliente en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de un cliente con el dni de este sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM CLIENTES WHERE dnicli = :dni")
            query.bindValue(":dni", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos cliente: ", error)

    def modifCliente(registro):
        """

        :param registro: datos del cliente a modificar
        :type registro: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que modifica los datos de un cliente cogiendo el dni del cual le pasas por parametro
        y usando el resto de la lista que le pasas como los datos a modificar
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("select count(*) from clientes where dnicli = :dni")
            query.bindValue(":dni", str(registro[0]))
            if query.exec():
                if query.next() and query.value(0) > 0:
                    query.prepare("UPDATE clientes set altacli = :altacli, apelcli = :apelcli, nomecli = :nomecli, "
                                  " emailcli = :emailcli, movilcli = :movilcli, dircli = :dircli, provcli = :provcli, "
                                  " municli = :municli, bajacli = :bajacli where dnicli = :dni")
                    query.bindValue(":dni", str(registro[0]))
                    query.bindValue(":altacli", str(registro[1]))
                    query.bindValue(":apelcli", str(registro[2]))
                    query.bindValue(":nomecli", str(registro[3]))
                    query.bindValue(":emailcli", str(registro[4]))
                    query.bindValue(":movilcli", str(registro[5]))
                    query.bindValue(":dircli", str(registro[6]))
                    query.bindValue(":provcli", str(registro[7]))
                    query.bindValue(":municli", str(registro[8]))
                    if registro[9] == "":
                        query.bindValue(":bajacli", None)
                    else:
                        query.bindValue(":bajacli", str(registro[9]))
                    query.exec()
                    return query.numRowsAffected() != 0
            return False
        except Exception as error:
            print("error modificar cliente", error)

    def bajaCliente(datos):
        """

        :param datos: fecha de baja a introducir y dni del cliente al cual damos de baja
        :type datos: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de baja a un cliente cogiendo el dni del cliente del cual le pasas por parametro
        Este metodo no elimina el cliente de la base de datos, solo le pone la fecha de baja y asi no
         se ve en la tabla a menos que pulses en mostrar historico
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE clientes set bajacli = :bajacli WHERE dnicli = :dnicli")
            query.bindValue(":bajacli", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":dnicli", str(datos[1]))
            query.exec()
            return query.numRowsAffected() != 0
        except Exception as error:
            print("Error en baja cliente: ", error)

    """
    -------------------- GESTION PROPIEDADES --------------------
    """

    def altaTipoPropiedad(tipo):
        """

        :param tipo: tipo de propiedad que dar de alta
        :type tipo: str
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un tipo de propiedad cogiendo el tipo de propiedad del cual le pasas por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("INSERT INTO tipoPropiedad (tipo) VALUES (:tipo)")
            query.bindValue(":tipo", tipo)
            return query.exec()
        except Exception as error:
            print("Error en alta tipo propiedad: ", error)

    def bajaTipoPropiedad(tipo):
        """

        :param tipo: tipo de propiedad que dar de baja
        :type tipo: str
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de baja a un tipo de propiedad cogiendo el tipo de propiedad del cual le pasas por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("DELETE FROM tipoPropiedad WHERE tipo = :tipo")
            query.bindValue(":tipo", tipo)
            return query.exec()
        except Exception as error:
            print("Error en baja tipo propiedad: ", error)

    def cargarTipoPropiedad(self):
        """

        :return: lista de los tipos de propiedad
        :rtype: list

        Metodo que devuelve una lista con los tipos de propiedad
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT tipo FROM tipoPropiedad")
            registro = []
            if query.exec():
                while query.next():
                    registro.append(query.value(0))
            return registro
        except Exception as error:
            print("Error en cargar tipo propiedad: ", error)

    def altaPropiedad(propiedad):
        """

        :param propiedad: datos de la propiedad que dar de alta
        :type propiedad: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a una propiedad cogiendo los datos de esta de la lista que le pasas por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                " INSERT into PROPIEDADES (altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, "
                " superprop, prealquiprop, prevenprop, cpprop, obserprop, tipooper, estadoprop, nomeprop, movilprop) "
                " VALUES (:altaprop, :dirprop, :provprop, :muniprop, :tipoprop, :habprop, :banprop, :superprop, "
                " :prealquiprop, :prevenprop, :cpprop, :obserprop, :tipooper, :estadoprop, :nomeprop, :movilprop)")
            query.bindValue(":altaprop", str(propiedad[0]))
            query.bindValue(":dirprop", str(propiedad[1]))
            query.bindValue(":provprop", str(propiedad[2]))
            query.bindValue(":muniprop", str(propiedad[3]))
            query.bindValue(":tipoprop", str(propiedad[4]))
            query.bindValue(":habprop", int(propiedad[5]))
            query.bindValue(":banprop", int(propiedad[6]))
            query.bindValue(":superprop", float(propiedad[7]))
            if propiedad[8] == "":
                query.bindValue(":prealquiprop", None)
            else:
                query.bindValue(":prealquiprop", float(propiedad[8]))
            if propiedad[9] == "":
                query.bindValue(":prealquiprop", None)
            else:
                query.bindValue(":prealquiprop", float(propiedad[9]))
            query.bindValue(":cpprop", str(propiedad[10]))
            query.bindValue(":obserprop", str(propiedad[11]))
            query.bindValue(":tipooper", str(propiedad[14]))
            query.bindValue(":estadoprop", str(propiedad[15]))
            query.bindValue(":nomeprop", str(propiedad[12]))
            query.bindValue(":movilprop", str(propiedad[13]))
            return query.exec()

        except Exception as e:
            print("error altaPropiedad en conexion", e)

    def listadoPropiedades(self):
        """

        :return: lista de los datos de las propiedades no dadas de baja o ambas dependiendo de la variable historico
        :rtype: list

        Metodo que devuelve una lista con los datos de las propiedades,
        coge los datos de todas o solo de las que no están dadas de baja dependiendo del estado de la variable historico
        """
        try:
            listado = []
            queryStr = ""
            if var.historico == 1:
                queryStr = "SELECT * FROM propiedades WHERE bajaprop is NULL ORDER BY muniprop ASC "

            elif var.historico == 0:
                queryStr = "SELECT * FROM propiedades ORDER BY muniprop ASC "

            query = QtSql.QSqlQuery()
            query.prepare(queryStr)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listado en conexion", e)

    def datosOnePropiedad(codigo):
        """

        :param codigo: propiedad que dar de alta
        :type codigo: String
        :return: lista de los datos de una propiedad en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de una propiedad que tenga el mismop codigo que el codigo de esta sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos datosOnePropiedad: ", error)

    def bajaPropiedad(datos):
        """

        :param datos: fecha de baja a introducir y codigo de la propiedad al cual damos de baja
        :type datos: int
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de baja a una propiedad cogiendo el codigo de la propiedad del cual le pasas por parametro
        El metodo no elimina la propiedad de la base de datos, solo le pone la fecha de baja y
         asi no se ve en la tabla a menos que pulses en mostrar historico
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE propiedades SET bajaprop = :bajaprop WHERE codigo = :codigo")
            query.bindValue(":bajaprop", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":codigo", datos)
            return query.exec()
        except Exception as error:
            print("Error en baja propiedad: ", error)

    def modifPropiedad(propiedad):
        """

        :param propiedad: propiedad a modificar
        :type propiedad: propiedad
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que modifica los datos de una propiedad cogiendo el codigo de la propiedad del cual le pasas por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("SELECT count(*) FROM propiedades WHERE codigo = :codigo")
            query.bindValue(":codigo", int(propiedad[0]))
            if query.exec() and query.next() and query.value(0) > 0:
                query.prepare(
                    "UPDATE propiedades SET altaprop = :altaprop, dirprop = :dirprop, provprop = :provprop, "
                    "muniprop = :muniprop, tipoprop = :tipoprop, habprop = :habprop, banprop = :banprop, "
                    "superprop = :superprop, prealquiprop = :prealquiprop, prevenprop = :prevenprop, cpprop = :cpprop, "
                    "obserprop = :obserprop, tipooper = :tipooper, estadoprop = :estadoprop, nomeprop = :nomeprop, "
                    "movilprop = :movilprop WHERE codigo = :codigo"
                )
                query.bindValue(":altaprop", str(propiedad[1]))
                query.bindValue(":dirprop", str(propiedad[2]))
                query.bindValue(":provprop", str(propiedad[3]))
                query.bindValue(":muniprop", str(propiedad[4]))
                query.bindValue(":tipoprop", str(propiedad[5]))
                query.bindValue(":habprop", int(propiedad[6]))
                query.bindValue(":banprop", int(propiedad[7]))
                query.bindValue(":superprop", float(propiedad[8]))
                query.bindValue(":prealquiprop", float(propiedad[9]))
                query.bindValue(":prevenprop", float(propiedad[10]))
                query.bindValue(":cpprop", str(propiedad[11]))
                query.bindValue(":obserprop", str(propiedad[12]))
                query.bindValue(":tipooper", str(propiedad[13]))
                query.bindValue(":estadoprop", str(propiedad[14]))
                query.bindValue(":nomeprop", str(propiedad[15]))
                query.bindValue(":movilprop", str(propiedad[16]))
                query.bindValue(":codigo", int(propiedad[0]))

                return query.exec()
            return False
        except Exception as error:
            print("Error modificar propiedad conexion ", error)

    def altaVen(self, nuevoVen):
        """

        :param nuevoVen: datos a insertar de un nuevo vendedor
        :type nuevoVen: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un vendendor cogiendo los datos de este de la lista
         que le pasas por parametro y elige el vendedor con el dni que está en los datos de la lista pasada por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO vendedores (dniVendedor, nombreVendedor, altaVendedor, movilVendedor, mailVendedor, delegacionVendedor) "
                " VALUES (:dniVendedor, :nombreVendedor, :altaVendedor, :movilVendedor, :mailVendedor, :delegacionVendedor)")
            query.bindValue(":dniVendedor", str(nuevoVen[1]))
            query.bindValue(":nombreVendedor", str(nuevoVen[0]))
            query.bindValue(":altaVendedor", str(nuevoVen[4]))
            query.bindValue(":movilVendedor", str(nuevoVen[3]))
            query.bindValue(":mailVendedor", str(nuevoVen[5]))
            query.bindValue(":delegacionVendedor", str(nuevoVen[2]))
            if query.exec():
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en alta vendedor: ", error)

    def listadoVendedores(self):
        """

        :return: lista de los vendedores no dados de baja o ambos dependiendo de la variable historico
        :rtype: list

        Metodo que devuelve una lista con los datos de los vendedores, coge los datos de todos o solo de
        los que no están dados de baja dependiendo de el estado de la variable historico
        """
        try:
            listado = []
            queryStr = ""
            if var.historico == 1:
                queryStr = "SELECT * FROM vendedores WHERE bajaVendedor is NULL ORDER BY idVendedor ASC "

            elif var.historico == 0:
                queryStr = "SELECT * FROM vendedores ORDER BY idVendedor ASC "

            query = QtSql.QSqlQuery()
            query.prepare(queryStr)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listado en conexion", e)

    def bajaVendedor(datos):
        """

        :param datos: id del vendedor al cual damos de baja
        :type datos: int
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de baja a un vendedor cogiendo el id del vendedor del cual le pasas por parametro
        No lo elimina completamente de la base de datos, solo le pone la fecha de baja y asi no se ve en
        la tabla a menos que pulses en mostrar historico
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare("UPDATE vendedores SET bajaVendedor = :bajaVendedor WHERE idVendedor = :idVendedor")
            query.bindValue(":bajaVendedor", datetime.now().strftime("%d/%m/%Y"))
            query.bindValue(":idVendedor", datos)
            return query.exec()
        except Exception as error:
            print("Error en baja propiedad: ", error)

    def datosOneVendedor(codigo):
        """

        :param codigo: id del vendedor del cual queremos obtener los datos
        :type codigo: codigo del vendedor
        :return: lista de los datos de un vendedor en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de un vendedor con el id de este sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE idVendedor = :idVendedor")
            query.bindValue(":idVendedor", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos datosOneVendedor: ", error)

    def datosOneVendedorDNI(self, dni):
        """

        :param dni: dni del vendedor del cual queremos obtener los datos
        :type dni: str
        :return: datos de un vendedor en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de un vendedor con el dni de este sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE dniVendedor = :dniVendedor")
            query.bindValue(":dniVendedor", str(dni))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos datosOneVendedor: ", error)

    def datosOneVendedorMovil(self, movil):
        """

        :param movil: movil del vendedor del cual queremos obtener los datos
        :type movil: str
        :return: datos de un vendedor en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de un vendedor con el movil de este sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT * FROM vendedores WHERE movilVendedor = :movilVendedor")
            query.bindValue(":movilVendedor", str(movil))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos datosOneVendedor: ", error)

    def modifVen(vendedor):
        """

        :param vendedor: datos del vendedor a modificar
        :type vendedor: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que modifica los datos de un vendedor cogiendo el dni del cual le pasas por parametro y
         usando el resto de la lista que le pasas como los datos a modificar
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "UPDATE vendedores SET dniVendedor = :dniVendedor, nombreVendedor = :nombreVendedor, altaVendedor = :altaVendedor, "
                "movilVendedor = :movilVendedor, mailVendedor = :mailVendedor, delegacionVendedor = :delegacionVendedor"
                " WHERE idVendedor = :idVendedor"
            )
            query.bindValue(":idVendedor", str(vendedor[0]))
            query.bindValue(":dniVendedor", str(vendedor[2]))
            query.bindValue(":nombreVendedor", str(vendedor[1]))
            query.bindValue(":altaVendedor", str(vendedor[5]))
            query.bindValue(":movilVendedor", str(vendedor[4]))
            query.bindValue(":mailVendedor", str(vendedor[6]))
            query.bindValue(":delegacionVendedor", str(vendedor[3]))

            return query.exec()
        except Exception as error:
            print("Error modificar vendedor", error)

    def listaMunicipiosTexto(self):
        try:
            listamunicipios = []
            query = QtSql.QSqlQuery()
            if query.exec("SELECT * FROM municipios"):
                while query.next():
                    listamunicipios.append(query.value("municipio"))
            return listamunicipios
        except Exception as error:
            print("error lista muniText: ", error)

    def altaFactura(self, nuevaFac):
        """

        :param nuevoVen: datos a insertar de un nuevo vendedor
        :type nuevoVen: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un vendendor cogiendo los datos de este de la lista
         que le pasas por parametro y elige el vendedor con el dni que está en los datos de la lista pasada por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO facturas (dnifac,fechafac) "
                " VALUES (:dni, :fecha)")
            query.bindValue(":dni", str(nuevaFac[0]))
            query.bindValue(":fecha", str(nuevaFac[1]))
            if query.exec():
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en alta factura: ", error)

    def listadoFacturas(self):
        """

        :return: lista de los datos de las propiedades no dadas de baja o ambas dependiendo de la variable historico
        :rtype: list

        Metodo que devuelve una lista con los datos de las propiedades,
        coge los datos de todas o solo de las que no están dadas de baja dependiendo del estado de la variable historico
        """
        try:
            listado = []
            queryStr = "SELECT * FROM facturas "

            query = QtSql.QSqlQuery()
            query.prepare(queryStr)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listado en facturas", e)

    def delFactura(self, idFactura):
        """

        :param nuevoVen: datos a insertar de un nuevo vendedor
        :type nuevoVen: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un vendendor cogiendo los datos de este de la lista
         que le pasas por parametro y elige el vendedor con el dni que está en los datos de la lista pasada por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "DELETE FROM  facturas "
                " WHERE id = :idFactura")
            query.bindValue(":idFactura", idFactura)
            if query.exec():
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en eliminar factura: ", error)

    def datosOneFactura(codigo):
        """

        :param codigo: id del vendedor del cual queremos obtener los datos
        :type codigo: codigo del vendedor
        :return: lista de los datos de un vendedor en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de un vendedor con el id de este sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("SELECT f.id, f.fechafac, f.dnifac, cl.nomecli, cl.apelcli"
                          " FROM facturas AS f "
                          " INNER JOIN clientes AS cl ON cl.dnicli = f.dnifac"
                          " WHERE f.id = :idVendedor ")
            query.bindValue(":idVendedor", str(codigo))
            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
            return registro
        except Exception as error:
            print("Error en datos datosOneFactura: ", error)

    def listadoVentas(self, idFactura=None):
        """

        :return: lista de los datos de las propiedades no dadas de baja o ambas dependiendo de la variable historico
        :rtype: list

        Metodo que devuelve una lista con los datos de las propiedades,
        coge los datos de todas o solo de las que no están dadas de baja dependiendo del estado de la variable historico
        """
        try:
            listado = []
            query = QtSql.QSqlQuery()
            if idFactura is None:

                query.prepare("""
                            SELECT 
                                v.id, 
                                v.idPropiedad, 
                                p.dirprop, 
                                p.muniprop, 
                                p.tipoprop, 
                                p.prevenprop 
                            FROM 
                                ventas AS v 
                            INNER JOIN 
                                propiedades AS p 
                            ON 
                                p.codigo = v.idPropiedad
                        """)
            else:
                query.prepare("""
                            SELECT 
                                v.id, 
                                v.idPropiedad, 
                                p.dirprop, 
                                p.muniprop, 
                                p.tipoprop, 
                                p.prevenprop 
                            FROM 
                                ventas AS v 
                            INNER JOIN 
                                propiedades AS p 
                            ON 
                                p.codigo = v.idPropiedad
                            WHERE 
                                v.idFactura = :idFactura"""
                              )
                query.bindValue(":idFactura", idFactura)
            if query.exec():
                while query.next():
                    fila = [query.value(i) for i in range(query.record().count())]
                    listado.append(fila)
            return listado
        except Exception as e:
            print("Error listado en facturas", e)

    def datosOneVenta(codigo):
        """

        :param codigo: id del vendedor del cual queremos obtener los datos
        :type codigo: codigo del vendedor
        :return: lista de los datos de un vendedor en concreto
        :rtype: list

        Metodo que devuelve una lista con los datos de un vendedor con el id de este sacado por el parametro
        """
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("""
                SELECT 
                       v.idVendedor, 
                       f.id, f.fechafac, f.dnifac,
                       cl.nomecli, cl.apelcli, 
                       p.codigo, p.dirprop, p.tipoprop, p.muniprop, p.prevenprop
                FROM ventas AS v
                INNER JOIN clientes AS cl ON f.dnifac = cl.dnicli
                INNER JOIN facturas AS f ON v.idFactura = f.id
                INNER JOIN propiedades AS p ON p.codigo = v.idPropiedad
                WHERE v.id = :codigo
            """)
            query.bindValue(":codigo", str(codigo))

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
                    return registro
        except Exception as error:
            print("Error en datos datosOneVenta: ", error)

    def altaVenta(self, nuevaVenta):
        """

        :param nuevoVen: datos a insertar de un nuevo vendedor
        :type nuevoVen: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un vendendor cogiendo los datos de este de la lista
         que le pasas por parametro y elige el vendedor con el dni que está en los datos de la lista pasada por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "INSERT INTO ventas (idPropiedad, idFactura, idVendedor) "
                " VALUES (:propiedad, :factura, :vendedor)")
            query.bindValue(":propiedad", str(nuevaVenta[0]))
            query.bindValue(":factura", str(nuevaVenta[1]))
            query.bindValue(":vendedor", str(nuevaVenta[2]))
            if query.exec():
                Conexion.cambiarEstadoPropiedad(self, nuevaVenta[0], "Vendido")
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en alta venta: ", error)

    def cambiarEstadoPropiedad(self, codigo, estado):
        query = QtSql.QSqlQuery()
        query.prepare(
            "UPDATE propiedades SET bajaprop = :bajaPropiedad, estadoprop = :estado WHERE codigo = :codigo ")
        query.bindValue(":bajaPropiedad", datetime.now().strftime("%d/%m/%Y"))
        if estado == "Disponible":
            query.bindValue(":bajaPropiedad", None)
        query.bindValue(":codigo", str(codigo))
        query.bindValue(":estado", str(estado))
        query.exec()

    def facturaUtilizada(self, idFactura):
        try:
            registro = []
            query = QtSql.QSqlQuery()
            query.prepare("""
                SELECT v.id
                FROM facturas AS f
                INNER JOIN ventas AS v ON f.id = v.idFactura
                WHERE f.id = :idFactura
            """)
            query.bindValue(":idFactura", int(idFactura))

            if query.exec():
                while query.next():
                    for i in range(query.record().count()):
                        registro.append(query.value(i))
                return registro
        except Exception as error:
            print("Error en facturaUtilizada: ", error)


    def delVenta(self, idPropiedad, idVenta):
        """

        :param nuevoVen: datos a insertar de un nuevo vendedor
        :type nuevoVen: list
        :return: verdadero o falso dependiendo del éxito de la operación
        :rtype: bool

        Metodo que da de alta a un vendendor cogiendo los datos de este de la lista
         que le pasas por parametro y elige el vendedor con el dni que está en los datos de la lista pasada por parametro
        """
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "DELETE FROM  ventas "
                " WHERE id = :idVenta")
            query.bindValue(":idVenta", idVenta)
            if query.exec():
                Conexion.cambiarEstadoPropiedad(self, idPropiedad, "Disponible")
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en eliminar Venta: ", error)

    def isFacturada(self,idVenta):
        try:
            query = QtSql.QSqlQuery()
            query.prepare(
                "SELECT * FROM ventas WHERE idPropiedad = :idVenta")
            query.bindValue(":idVenta", idVenta)
            return query.exec()
        except sqlite3.Error as e:
            print(e)
        except Exception as error:
            print("Error en idFacturada conexion: ", error)