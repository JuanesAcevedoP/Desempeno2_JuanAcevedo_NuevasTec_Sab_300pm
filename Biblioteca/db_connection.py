import mysql.connector

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="dblibrary"
        )
        if connection.is_connected():
            print("Conexión exitosa a la base de datos.")
            return connection
    except Exception as e:
        print("Error al conectar a la base de datos:", str(e))
        return None

def close_connection(connection):
    if connection:
        connection.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    conn = create_connection()

    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT VERSION()")
            db_version = cursor.fetchone()
            print("Versión de MySQL:", db_version[0])
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if conn.is_connected():
                cursor.close()
        close_connection(conn)
    else:
        print("No se pudo establecer la conexión a la base de datos.")
