from db_connection import create_connection, close_connection

class Librarian:
    def __init__(self, id, username, password):
        self.__id = id
        self.__username = username
        self.__password = password

    def librarian_menu(self):
        while True:
            print("Menú de Bibliotecario")
            print("1. Registrar libro")
            print("2. Listar libros")
            print("3. Listar préstamos")
            print("4. Salir al Menú Principal")
            choice = input("Seleccione una opción: ")

            if choice == '1':
                self.add_book()
            elif choice == '2':
                self.list_books()
            elif choice == '3':
                self.list_loans()
            elif choice == '4':
                break
            else:
                print("Opción no válida. Intente de nuevo.")

    def add_book(self):
        codix = input("Código del libro: ")
        name = input("Nombre del libro: ")
        author = input("Autor del libro: ")
        status = input("Estado del libro (disponible/prestado): ")

        connection = create_connection()
        if not connection:
            return

        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO Libros (cod, Nombre, Autor, Estado) VALUES (%s, %s, %s, %s)",
                           (codix, name, author, status))
            connection.commit()
            print(f"Libro registrado exitosamente: Codigo {codix}, Nombre {name}")

        except Exception as e:
            print("Error al registrar el libro:", str(e))

        finally:
            cursor.close()
            close_connection(connection)

    def list_books(self):
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

    def list_loans(self):
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
