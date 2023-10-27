from db_connection import create_connection, close_connection

class Library:
    def __init__(self):
        self.__id = None
        self.__username = None
        self.__rol = None
        self.__password = None

    @staticmethod
    def register(id, username, rol, password):
        connection = create_connection()
        if not connection:
            return
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO Usuarios (id, username, rol, password) VALUES (%s, %s, %s, %s)",
                           (id, username, rol, password))
            connection.commit()
            print("Usuario registrado exitosamente.")

        except Exception as e:
            print("Error al registrar usuario:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def login(username, password):
        connection = create_connection()
        if not connection:
            return
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id, rol FROM Usuarios WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()

            if user:
                id, rol = user
                print(f"Bienvenido, {username} ({rol}).")
                return id, username, rol
            else:
                print("Credenciales incorrectas. Por favor, intenta de nuevo.")

        except Exception as e:
            print("Error al iniciar sesión:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def add_book(codix, name, author, status):
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO Libros (cod, Nombre, Autor, Estado) VALUES (%s, %s, %s, %s)",
                           (codix, name, author, status))
            connection.commit()
            print(f"Libro registrado exitosamente: Código {codix}, Nombre {name}")

        except Exception as e:
            print("Error al registrar el libro:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def list_books():
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT Cod, Nombre, Autor, Estado FROM Libros")
            books = cursor.fetchall()

            if books:
                print("Lista de libros:")
                for book in books:
                    code, name, author, status = book
                    print(f"Código: {code}, Nombre: {name}, Autor: {author}, Estado: {status}")
            else:
                print("No hay libros registrados en la base de datos.")

        except Exception as e:
            print("Error al listar libros:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def list_loans():
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT p.id, l.cod, l.Nombre, l.Autor FROM Prestamos p "
                           "INNER JOIN Libros l ON p.libro_codigo = l.cod")
            loans = cursor.fetchall()

            if loans:
                print("Lista de préstamos:")
                for loan in loans:
                    loan_id, book_code, book_name, book_author = loan
                    print(f"Préstamo ID: {loan_id}, Código del libro: {book_code}, Nombre del libro: {book_name}, Autor: {book_author}")
            else:
                print("No hay préstamos registrados en la base de datos.")

        except Exception as e:
            print("Error al listar préstamos:", str(e))

        finally:
            cursor.close()
            close_connection(connection)


    @staticmethod
    def borrow_book(user_id, book_code):
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT Estado FROM Libros WHERE cod = %s", (book_code,))
            book_status = cursor.fetchone()

            if book_status and book_status[0] == "disponible":
                cursor.execute("UPDATE Libros SET Estado = 'prestado' WHERE cod = %s", (book_code,))
                cursor.execute("INSERT INTO Prestamos (usuario_id, libro_codigo, fecha_prestamo) VALUES (%s, %s, NOW())", (user_id, book_code))
                connection.commit()
                print("Libro prestado con éxito.")
            else:
                print("El libro no está disponible para préstamo.")

        except Exception as e:
            print("Error al prestar el libro:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    @staticmethod
    def return_book(user_id, book_code):
        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id FROM Prestamos WHERE usuario_id = %s AND libro_codigo = %s", (user_id, book_code))
            loan_id = cursor.fetchone()

            if loan_id:
                cursor.execute("UPDATE Libros SET Estado = 'disponible' WHERE cod = %s", (book_code,))
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

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def rol(self):
        return self.__rol

    @rol.setter
    def rol(self, rol):
        self.__rol = rol

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password
