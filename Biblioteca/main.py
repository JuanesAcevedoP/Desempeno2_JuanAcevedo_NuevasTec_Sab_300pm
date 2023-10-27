from library import Library
from librarian import Librarian
from user import User

def main():
    print("Bienvenido a la Biblioteca")
    while True:
        print("Menú Principal")
        print("1. Registro")
        print("2. Iniciar Sesión")
        print("3. Salir")
        choice = input("Seleccione una opción: ")

        if choice == '1':
            username = input("Ingrese su nombre de usuario: ")
            rol = input("Ingrese su rol (bibliotecario/usuario): ")
            password = input("Digite su contraseña: ")

            id = 0

            Library.register(id, username, rol, password)
            print("Registro exitoso")
        elif choice == '2':
            username = input("Ingrese su nombre de usuario: ")
            password = input("Ingrese su contraseña: ")
            user_id, username, rol = Library.login(username, password)
            if rol == 'bibliotecario':
                Librarian(id=user_id, username=username, password=password).librarian_menu()
            elif rol == 'usuario':
                 User(id=user_id, username=username, password=password).user_menu()
        elif choice == '3':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")

if __name__ == "__main__":
    main()
