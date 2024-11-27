import mysql.connector
from mysql.connector import Error
from datetime import datetime

import var


class ConexionServer():
    def crear_conexion(self):
        try:
            conexion = mysql.connector.connect(
                host='192.168.10.66',  # Cambia esto a la IP de tu servidor user='dam', # Usuario creado
                # host='192.168.1.49',
                user='dam',
                password='dam2425',
                database='bbdd',
                charset="utf8mb4",
                collation="utf8mb4_general_ci"  # Asegúrate de que aquí esté configurado
                # Contraseña del usuario database='bbdd' # Nombre de la base de datos
            )
            if conexion.is_connected():
                pass
                # print("Conexión exitosa a la base de datos")
            return conexion
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
        return None

    @staticmethod
    def listaProv(self=None):
        listaprov = []
        conexion = ConexionServer().crear_conexion()
        if conexion:
            try:
                cursor = conexion.cursor()
                cursor.execute("SELECT * FROM provincias")
                resultados = cursor.fetchall()
                for fila in resultados:
                    listaprov.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
                cursor.close()
                conexion.close()
            except Error as e:
                print(f"Error al ejecutar la consulta: {e}")
        return listaprov

    @staticmethod
    def listaMuniProv(provincia):
        try:
            conexion = ConexionServer().crear_conexion()
            listamunicipios = []
            cursor = conexion.cursor()
            cursor.execute(
                "SELECT * FROM municipios WHERE idprov = (SELECT idprov FROM provincias WHERE provincia = %s)",
                (provincia,)
            )
            resultados = cursor.fetchall()
            for fila in resultados:
                listamunicipios.append(fila[1])  # Asumiendo que el nombre de la provincia está en la segunda columna
            cursor.close()
            conexion.close()
            return listamunicipios
        except Exception as error:
            print("error lista muni", error)

    def listadoClientes(self):
        try:
            conexion = ConexionServer().crear_conexion()
            listadoclientes = []
            cursor = conexion.cursor()
            queryStr = ""
            if var.historico == 1:
                queryStr = "SELECT * FROM clientes WHERE bajacli IS NULL OR bajacli = '' ORDER BY apelcli, nomecli ASC"
            elif var.historico == 0:
                queryStr = "SELECT * FROM clientes ORDER BY apelcli, nomecli ASC"

            cursor.execute(queryStr)
            resultados = cursor.fetchall()
            for fila in resultados:
                listadoclientes.append(list(fila))
            cursor.close()
            conexion.close()
            return listadoclientes
        except Exception as e:
            print("error listado en conexion", e)

    def altaCliente(self, cliente):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de inserción
                query = """
                INSERT INTO clientes (dnicli, altacli, apelcli, nomecli, dircli, emailcli, movilcli, provcli, municli)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, cliente)  # Ejecutar la consulta pasando la lista directamente
                conexion.commit()  # Confirmar la transacción
                cursor.close()  # Cerrar el cursor y la conexión
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el cliente: {e}")

    def datosOneCliente(dni):
        registro = []  # Inicializa la lista para almacenar los datos del cliente
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                # Definir la consulta de selección
                query = '''SELECT * FROM clientes WHERE dnicli = %s'''  # Usa %s para el placeholder
                cursor.execute(query, (dni,))  # Pasar 'dni' como una tupla
                # Recuperar los datos de la consulta
                for row in cursor.fetchall():
                    registro.extend([str(col) for col in row])
            return registro

        except Exception as e:
            print("Error al obtener datos de un cliente:", e)
            return None  # Devolver None en caso de error

    def modifCliente(registro):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT count(*) FROM clientes WHERE dnicli = %s", (str(registro[0]),))
                if cursor.fetchone()[0] > 0:
                    query = """
                    UPDATE clientes SET altacli = %s, apelcli = %s, nomecli = %s, emailcli = %s, movilcli = %s, 
                    dircli = %s, provcli = %s, municli = %s, bajacli = %s WHERE dnicli = %s
                    """
                    cursor.execute(query, (
                        str(registro[1]), str(registro[2]), str(registro[3]), str(registro[4]), str(registro[5]),
                        str(registro[6]), str(registro[7]), str(registro[8]),
                        None if registro[9] == "" else str(registro[9]),
                        str(registro[0])
                    ))
                    conexion.commit()
                    return cursor.rowcount != 0
                return False
        except Error as error:
            print("Error al modificar cliente:", error)
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def bajaCliente(datos):
        try:
            conexion = ConexionServer().crear_conexion()
            if conexion:
                cursor = conexion.cursor()
                query = "UPDATE clientes SET bajacli = %s WHERE dnicli = %s"
                cursor.execute(query, (datetime.now().strftime("%d/%m/%Y"), str(datos[1])))
                conexion.commit()
                return cursor.rowcount != 0
        except Error as error:
            print("Error en baja cliente:", error)
        finally:
            if cursor:
                cursor.close()
            if conexion:
                conexion.close()

    def listadoPropiedades(self):
        try:
            conexion = ConexionServer.crear_conexion(self)
            listado = []
            cursor = conexion.cursor()
            queryStr = ""
            if var.historico == 1:
                queryStr = "SELECT * FROM propiedades WHERE bajaprop IS NULL OR bajaprop = '' ORDER BY muniprop ASC"
            elif var.historico == 0:
                queryStr = "SELECT * FROM propiedades ORDER BY muniprop ASC"

            cursor.execute(queryStr)
            resultados = cursor.fetchall()
            for fila in resultados:
                listado.append(list(fila))
            cursor.close()
            conexion.close()
            return listado
        except Error as e:
            print("Error listado en conexion", e)

    def datosOnePropiedad(self,codigo):
        try:
            conexion = ConexionServer.crear_conexion(self)
            registro = []
            cursor = conexion.cursor()
            query = "SELECT * FROM propiedades WHERE codigo = %s"
            cursor.execute(query, (codigo,))
            for row in cursor.fetchall():
                registro.extend([str(col) for col in row])
            cursor.close()
            conexion.close()
            return registro
        except Error as e:
            print("Error en datos datosOnePropiedad:", e)

    def bajaPropiedad(self,datos):
        try:
            conexion = ConexionServer.crear_conexion(self)
            cursor = conexion.cursor()
            query = "UPDATE propiedades SET bajaprop = %s WHERE codigo = %s"
            cursor.execute(query, (datetime.now().strftime("%d/%m/%Y"), datos))
            conexion.commit()
            cursor.close()
            conexion.close()
            return True
        except Error as e:
            print("Error en baja propiedad:", e)
        return False

    def modifPropiedad(self,propiedad):
        try:
            conexion = ConexionServer.crear_conexion(self)
            cursor = conexion.cursor()
            cursor.execute("SELECT count(*) FROM propiedades WHERE codigo = %s", (int(propiedad[0]),))
            if cursor.fetchone()[0] > 0:
                query = """
                UPDATE propiedades SET altaprop = %s, dirprop = %s, provprop = %s, muniprop = %s, tipoprop = %s,
                habprop = %s, banprop = %s, superprop = %s, prealquiprop = %s, prevenprop = %s, cpprop = %s,
                obserprop = %s, tipooper = %s, estadoprop = %s, nomeprop = %s, movilprop = %s WHERE codigo = %s
                """
                cursor.execute(query, (
                    str(propiedad[1]), str(propiedad[2]), str(propiedad[3]), str(propiedad[4]),
                    str(propiedad[5]),
                    int(propiedad[6]), int(propiedad[7]), float(propiedad[8]), float(propiedad[9]),
                    float(propiedad[10]),
                    str(propiedad[11]), str(propiedad[12]), str(propiedad[13]), str(propiedad[14]),
                    str(propiedad[15]),
                    str(propiedad[16]), int(propiedad[0])
                ))
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
            return False
        except Error as e:
            print("Error modificar propiedad:", e)

    def cargarTipoPropiedad(self):
        try:
            conexion = ConexionServer.crear_conexion(self)
            if conexion:
                cursor = conexion.cursor()
                cursor.execute("SELECT tipo FROM tipopropiedad")
                resultados = cursor.fetchall()
                tipos = [fila[0] for fila in resultados]
                cursor.close()
                conexion.close()
                return tipos
        except Error as e:
            print("Error al cargar tipos de propiedad:", e)
            return []

    def altaPropiedad(self,nuevaProp):
        try:
            conexion = ConexionServer.crear_conexion(self)
            if conexion:
                cursor = conexion.cursor()
                query = """
                INSERT INTO propiedades (altaprop, dirprop, provprop, muniprop, tipoprop, habprop, banprop, superprop, prealquiprop, prevenprop, cpprop, obserprop, nomeprop, estadoprop, tipooper, movilprop)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                cursor.execute(query, nuevaProp)
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar la propiedad: {e}")
            return False

    def altaTipoPropiedad(self, nuevoTipo):
        try:
            conexion = ConexionServer.crear_conexion(self)
            if conexion:
                cursor = conexion.cursor()
                query = "INSERT INTO tipopropiedad (tipo) VALUES (%s)"
                cursor.execute(query, (nuevoTipo,))
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Error as e:
            print(f"Error al insertar el tipo de propiedad: {e}")
            return False

    def bajaTipoPropiedad(self, tipoId):
        try:
            conexion = ConexionServer.crear_conexion(self)
            if conexion:
                cursor = conexion.cursor()
                query = "DELETE FROM tipopropiedad WHERE tipo = %s"
                cursor.execute(query, (tipoId,))
                conexion.commit()
                cursor.close()
                conexion.close()
                return True
        except Error as e:
            print(f"Error al eliminar el tipo de propiedad: {e}")
            return False