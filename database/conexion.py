
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():

    try:

        conexion = psycopg.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        return conexion

    except psycopg.Error as error:

        print("ERROR DE CONEXION:")
        print(error)

        return None


def probar_conexion():

    conexion = obtener_conexion()

    if conexion is None:
        return False

    try:

        with conexion.cursor() as cursor:

            cursor.execute("SELECT version();")

            resultado = cursor.fetchone()

            print("CONEXION EXITOSA")
            print(resultado[0])

        return True

    except psycopg.Error as error:

        print("ERROR:", error)
        return False

    finally:

        conexion.close()
