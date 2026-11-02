
from database.conexion import obtener_conexion


def listar_clientes(filtro=""):
    """Lista todos los clientes o filtra por nombre, apellido o email."""

    conexion = obtener_conexion()

    if conexion is None:
        return []

    try:
        with conexion.cursor() as cursor:

            consulta = """
                SELECT
                    c.id_cliente,
                    c.nombre,
                    c.apellido,
                    c.email,
                    c.telefono,
                    c.estado,
                    e.nombre
                FROM clientes c
                LEFT JOIN empresas e
                    ON c.id_empresa = e.id_empresa
                WHERE
                    c.nombre ILIKE %s
                    OR c.apellido ILIKE %s
                    OR COALESCE(c.email, '') ILIKE %s
                ORDER BY c.id_cliente;
            """

            busqueda = f"%{filtro}%"

            cursor.execute(
                consulta,
                (busqueda, busqueda, busqueda)
            )

            return cursor.fetchall()

    except Exception as error:
        print("Error al listar clientes:", error)
        return []

    finally:
        conexion.close()


def obtener_empresas():
    """Obtiene las empresas para asociarlas a los clientes."""

    conexion = obtener_conexion()

    if conexion is None:
        return []

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT id_empresa, nombre
                FROM empresas
                ORDER BY nombre;
            """)

            return cursor.fetchall()

    except Exception as error:
        print("Error al obtener empresas:", error)
        return []

    finally:
        conexion.close()


def crear_cliente(nombre, apellido, email, telefono,
                  direccion, estado, id_empresa):

    conexion = obtener_conexion()

    if conexion is None:
        return False

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                INSERT INTO clientes
                (nombre, apellido, email, telefono,
                 direccion, estado, id_empresa)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
                nombre, apellido, email, telefono,
                direccion, estado, id_empresa
            ))

        conexion.commit()
        return True

    except Exception as error:
        conexion.rollback()
        print("Error al crear cliente:", error)
        return False

    finally:
        conexion.close()


def actualizar_cliente(id_cliente, nombre, apellido, email,
                       telefono, direccion, estado, id_empresa):

    conexion = obtener_conexion()

    if conexion is None:
        return False

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                UPDATE clientes
                SET nombre = %s,
                    apellido = %s,
                    email = %s,
                    telefono = %s,
                    direccion = %s,
                    estado = %s,
                    id_empresa = %s
                WHERE id_cliente = %s;
            """, (
                nombre, apellido, email, telefono,
                direccion, estado, id_empresa, id_cliente
            ))

        conexion.commit()
        return True

    except Exception as error:
        conexion.rollback()
        print("Error al actualizar cliente:", error)
        return False

    finally:
        conexion.close()


def eliminar_cliente(id_cliente):

    conexion = obtener_conexion()

    if conexion is None:
        return False

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                DELETE FROM clientes
                WHERE id_cliente = %s;
            """, (id_cliente,))

            eliminado = cursor.rowcount > 0

        conexion.commit()
        return eliminado

    except Exception as error:
        conexion.rollback()
        print("Error al eliminar cliente:", error)
        return False

    finally:
        conexion.close()
