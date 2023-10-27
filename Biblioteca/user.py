from db_connection import create_connection, close_connection


class User:
    def __init__(self, id, username, password):
        self.__id = id
        self.__username = username
        self.__password = password

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        self.__id = value

    def user_menu(self):
        while True:
            print("Menú de Usuario")
            print("1. Prestar libro")
            print("2. Devolver libro")
            print("3. Salir al Menú Principal")
            choice = input("Seleccione una opción: ")

            if choice == '1':
                book_code = input("Ingrese el código del libro que desea tomar prestado: ")
                self.borrow_book(book_code)
            elif choice == '2':
                book_code = input("Ingrese el código del libro que desea tomar prestado: ")
                self.return_book(book_code)
            elif choice == '3':
                break
            else:
                print("Opción no válida. Intente de nuevo")

    def borrow_book(self, book_code):
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT Estado FROM Libros WHERE cod = %s", (book_code,))
            book_status = cursor.fetchone()

            if book_status and book_status[0] == "disponible":
                cursor.execute("UPDATE Libros SET Estado = 'prestado' WHERE cod = %s", (book_code,))
                cursor.execute("INSERT INTO Prestamos (usuario_id, libro_codigo) VALUES (%s, %s)", (self.id, book_code))
                connection.commit()
                print("Libro prestado con éxito.")
            else:
                print("El libro no está disponible para préstamo.")

        except Exception as e:
            print("Error al prestar el libro:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    def return_book(self, book_code):
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            # Verifica si el libro está prestado al usuario
            cursor.execute("SELECT id FROM Prestamos WHERE usuario_id = %s AND libro_codigo = %s", (self.id, book_code))
            loan_id = cursor.fetchone()

            if loan_id:
                # Actualiza el estado del libro a "disponible"
                cursor.execute("UPDATE Libros SET Estado = 'disponible' WHERE cod = %s", (book_code,))
                # Elimina el registro del préstamo
                cursor.execute("DELETE FROM Prestamos WHERE id = %s", (loan_id[0],))
                connection.commit()
                print("Libro devuelto con éxito.")
            else:
                print("El libro no está prestado a este usuario.")

        except Exception as e:
            print("Error al devolver el libro:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

