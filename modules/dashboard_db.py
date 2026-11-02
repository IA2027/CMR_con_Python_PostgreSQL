
from database.conexion import obtener_conexion


def obtener_indicadores():

    conexion = obtener_conexion()

    if conexion is None:
        return None

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    (SELECT COUNT(*)
                     FROM clientes),

                    (SELECT COUNT(*)
                     FROM clientes
                     WHERE estado = 'Activo'),

                    (SELECT COUNT(*)
                     FROM oportunidades),

                    (SELECT COUNT(*)
                     FROM oportunidades
                     WHERE estado = 'Ganada'),

                    (SELECT COALESCE(SUM(valor), 0)
                     FROM oportunidades
                     WHERE estado = 'Ganada'),

                    (SELECT COALESCE(SUM(valor), 0)
                     FROM oportunidades
                     WHERE estado IN ('Nueva', 'En proceso'));
            """)

            resultado = cursor.fetchone()

            return {
                "clientes": resultado[0],
                "clientes_activos": resultado[1],
                "oportunidades": resultado[2],
                "ganadas": resultado[3],
                "valor_ganado": resultado[4],
                "pipeline": resultado[5]
            }

    except Exception as error:
        print("Error al consultar indicadores:", error)
        return None

    finally:
        conexion.close()


def obtener_pipeline_por_estado():

    conexion = obtener_conexion()

    if conexion is None:
        return []

    try:
        with conexion.cursor() as cursor:

            cursor.execute("""
                SELECT
                    estado,
                    COUNT(*),
                    COALESCE(SUM(valor), 0)
                FROM oportunidades
                GROUP BY estado
                ORDER BY
                    CASE estado
                        WHEN 'Nueva' THEN 1
                        WHEN 'En proceso' THEN 2
                        WHEN 'Ganada' THEN 3
                        WHEN 'Perdida' THEN 4
                        ELSE 5
                    END;
            """)

            return cursor.fetchall()

    except Exception as error:
        print("Error al consultar pipeline:", error)
        return []

    finally:
        conexion.close()
