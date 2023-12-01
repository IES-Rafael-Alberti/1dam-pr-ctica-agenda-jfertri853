"""
27/11/2023

Práctica del examen para realizar en casa
-----------------------------------------

* El programa debe estar correctamente documentado.

* Debes intentar ajustarte lo máximo que puedas a lo que se pide en los comentarios TODO.

* Tienes libertad para desarrollar los métodos o funciones que consideres, pero estás obligado a usar como mínimo todos los que se solicitan en los comentarios TODO.

* Además, tu programa deberá pasar correctamente las pruebas unitarias que se adjuntan en el fichero test_agenda.py, por lo que estás obligado a desarrollar los métodos que se importan y prueban en la misma: pedir_email(), validar_email() y validar_telefono()

"""

import os
import pathlib
from os import path

# Constantes globales
RUTA = pathlib.Path(__file__).parent.absolute() 

NOMBRE_FICHERO = 'contactos.csv'

RUTA_FICHERO = path.join(RUTA, NOMBRE_FICHERO)

#TODO: Crear un conjunto con las posibles opciones del menú de la agenda -> DONE
OPCIONES_MENU = {1, 2, 3, 4, 5, 6, 7, 8} #Conjunto con todas las posibles opciones del menú
#TODO: Utiliza este conjunto en las funciones agenda() y pedir_opcion() -> IN PROGRESS


def borrar_consola():
    """ Limpia la consola
    """
    if os.name == "posix":
        os.system ("clear")
    elif os.name == "ce" or os.name == "nt" or os.name == "dos":
        os.system ("cls")


def cargar_contactos(contactos: list) -> list:
    """Carga los contactos iniciales de la agenda desde un fichero

    :return: Una lista donde se guarda cada contacto del fichero en un diccionario diferente
    """
    #TODO: Controlar los posibles problemas derivados del uso de ficheros... -> DONE
    try:
        with open(RUTA_FICHERO, 'r') as fichero:
            for linea in fichero:
                datos = linea.strip().split(";")
                contacto = {"nombre": datos[0], "apellido": datos[1], "email": datos[2], "telefonos": datos[3:]}
                contactos.append(contacto)
        return contactos
    except FileExistsError:
        print("***ERROR*** - El archivo no existe")
    except FileNotFoundError:
        print("***ERROR*** - No se puede encontrar el archivo")
    except PermissionError:
        print("***ERROR*** - No tienes los permisos necesarios para usar este archivo")
    except IndexError:
        print("***ERROR*** - Alguna o algunas lineas de tu archivo no tiene todos los campos necesarios")
    except Exception:
        print("***ERROR DESCONOCIDO*** - Algo ha ido mal")
    print("Los contactos no se cargaron correctamente")
    return contactos


def validar_nombre(nombre: str) -> bool:
    """Recibe un nombre o apellido y comprueba que sea válido

    :params: nombre: una cadena que contiene el nombre o el apellido introducido por el usuario
    :return: devuelve True en caso de que se cumplan los requisitos
    """
    if nombre.strip() != "":
        return True
    else:
        raise NameError("La cadena introducida no tiene ningún caracter")


def validar_email(email, contactos_iniciales) -> bool:
    """Comprueba que el email sea válido y que no esté repetido en la agenda

    :params: email: el email introducido por el usuario
    :return: True en caso de que cumpla los requisitos
    """
    for contacto in contactos_iniciales:
        if email.lower() == contacto.get("email").lower():
            raise ValueError("el email ya existe en la agenda")

    if email == "":
        raise ValueError("el email no puede ser una cadena vacía")

    if "@" not in email:
        raise ValueError("el email no es un correo válido")

    return True


def validar_telefono(telefono) -> bool:
    if len(telefono) == 9:
        if telefono.isnumeric():
            return True
    elif len(telefono) == 12:
        if telefono[0:3] == "+34" and telefono[3:].isnumeric():
            return True
    else:
        raise ValueError("El telefono introducido no es válido")


def pedir_cadena() -> str:
    cadena = input(": ")
    if validar_nombre(cadena):
        return cadena


def pedir_email(contactos_iniciales) -> str:
    email = input("Introduce un email: ")
    email.replace(" ", "") # He añadido esto porque no tiene sentido guardar emails con espacios entre caracteres
    if validar_email(email, contactos_iniciales):
        return email


def pedir_telefonos() -> list:
    telefonos = []
    telefono = None
    while telefono != "":
        try:
            telefono = input("Introduce un telefono: ")
            telefono = telefono.replace(" ", "")
            if telefono != "":
                if validar_telefono(telefono):
                    telefonos.append(telefono)
        except ValueError as e:
            print("***ERROR*** - ", e)
    return telefonos


def agregar_contacto(contactos: list) -> list:
    print("Introduce un nombre", end="")
    try:
        nombre = pedir_cadena()
        nombre.lower().capitalize()
    except NameError as e:
        print("***ERROR*** - ", e)
        raise Exception("No se pudo agregar el contacto debido a un error en el nombre")

    print("Introduce un apellido", end="")
    try:
        apellido = pedir_cadena()
        apellido.lower().capitalize()
    except NameError as e:
        print("***ERROR*** - ", e)
        raise Exception("No se pudo agregar el contacto debido a un error en el apellido")

    try:
        email = pedir_email(contactos)
    except ValueError as e:
        print("***ERROR*** - ", e)
        raise Exception("No se pudo agregar el contacto debido a un error en el email")

    try:
        telefonos = pedir_telefonos()
    except ValueError as e:
        print("***ERROR*** - ", e)
        raise Exception("No se pudo agregar el contacto debido a un error en los telefonos")

    nuevo_contacto = {"nombre": nombre, "apellido": apellido, "email": email, "telefonos": telefonos}
    contactos.append(nuevo_contacto)
    return contactos


def buscar_contacto(contactos: list, email: str) -> int:
    for posicion in range(len(contactos)):
        if contactos[posicion].get("email").lower() == email.lower():
            return posicion
    raise Exception("El contacto no existe")


def eliminar_contacto(contactos: list, email: str):
    """ Elimina un contacto de la agenda
    ...
    """
    try:
        #TODO: Crear función buscar_contacto para recuperar la posición de un contacto con un email determinado -> IN PROGRESS
        pos = buscar_contacto(contactos, email)
        if pos != None:
            del contactos[pos]
            print("Se eliminó 1 contacto")
        else:
            print("No se encontró el contacto para eliminar")
    except Exception as e:
        print(f"***Error*** {e}")
        print("No se eliminó ningún contacto")


def ordenar_nombres(contactos: list) -> list:
    nombres = []
    for contacto in contactos:
        nombre = contacto.get("nombre")
        nombre = nombre.lower()
        nombre = nombre.replace(" ", "")
        nombres.append(nombre)

    total = len(nombres) - 1
    intercambios = None
    contador = 0

    while contador != len(nombres) and intercambios != 0:
        intercambios = 0

        for i in range(0, total):
            if nombres[i] > nombres[i + 1]:
                mayor = nombres[i]
                nombres[i] = nombres[i + 1]
                nombres[i + 1] = mayor
                intercambios += 1

        total -= 1
        contador += 1
    return nombres


def ordenar_contactos(contactos: list) -> list:
    contactos_ordenados = []
    nombres_ordenados = ordenar_nombres(contactos)
    for nombre in nombres_ordenados:
        for contacto in contactos:
            nombre_formateado = contacto.get("nombre")
            nombre_formateado = nombre_formateado.lower()
            nombre_formateado = nombre_formateado.replace(" ", "")
            if nombre == nombre_formateado:
                contactos_ordenados.append(contacto)
    return contactos_ordenados


def mostrar_contactos(contactos: list):
    contactos_ordenados = ordenar_contactos(contactos)
    print("Agenda (" + str(len(contactos)) + ")")
    print("------")
    for contacto in contactos_ordenados:
        print("Nombre:" + contacto.get("nombre") + contacto.get("apellido") + "(" + contacto.get("email") + ")")
        if contacto.get("telefonos") == []:
            print("Teléfonos: ninguno", end="")
        else:
            contador = 0
            print("Teléfonos: ", end="")
            for telefono in contacto.get("telefonos"):
                contador += 1
                if len(telefono) == 12:
                    print(telefono[0:3] + "-" + telefono[3:], end="")
                else:
                    print(telefono, end="")
                if contador != len(contacto.get("telefonos")):
                    print(" / ", end="")
        print("\n......")


def mostrar_menu():
    print("AGENDA\n------\n1. Nuevo contacto\n2. Modificar contacto\n3. Eliminar contacto\n4. Vaciar agenda\n5. Cargar agenda inicial\n6. Mostrar contactos por criterio\n7. Mostrar la agenda completa\n8. Salir\n")


def pedir_opcion():
    opcion = int(input("Introduce una de las opciones: "))
    return opcion


def vaciar_agenda(contactos: list):
    for posicion in range(len(contactos) - 1, -1, -1):
        del contactos[posicion]


def agenda(contactos: list):
    """ Ejecuta el menú de la agenda con varias opciones
    ...
    """
    #TODO: Crear un bucle para mostrar el menú y ejecutar las funciones necesarias según la opción seleccionada... -> IN PROGRESS
    opcion = None
    while opcion != 8:
        mostrar_menu()
        try:
            opcion = pedir_opcion()
        except ValueError:
            print("Esa no es una opción válida")
            opcion = None

        #TODO: Se valorará que utilices la diferencia simétrica de conjuntos para comprobar que la opción es un número entero del 1 al 7 -> IN PROGRESS
        if opcion in OPCIONES_MENU:
            if opcion == 1:
                try:
                    agregar_contacto(contactos)
                except Exception as e:
                    print("***ERROR*** - ", e)
            #elif opcion == 2:
                #modificar_contacto(contactos)
            elif opcion == 3:
                email_contacto = input("Introduce el email del contacto que quieres eliminar: ")
                eliminar_contacto(contactos, email_contacto)
            elif opcion == 4:
                vaciar_agenda(contactos)
            elif opcion == 5:
                cargar_contactos(contactos)
            #elif opcion == 6:
                #mostrar_contactos_por_criterio()
            elif opcion == 7:
                mostrar_contactos(contactos)


def pulse_tecla_para_continuar():
    """ Muestra un mensaje y realiza una pausa hasta que se pulse una tecla
    """
    print("\n")
    os.system("pause")


def main():
    """ Función principal del programa
    """
    borrar_consola()

    #TODO: Asignar una estructura de datos vacía para trabajar con la agenda -> DONE
    contactos = []

    #TODO: Modificar la función cargar_contactos para que almacene todos los contactos del fichero en una lista con un diccionario por contacto (claves: nombre, apellido, email y telefonos) -> DONE
    #TODO: Realizar una llamada a la función cargar_contacto con todo lo necesario para que funcione correctamente. -> DONE
    cargar_contactos(contactos)

    #TODO: Crear función para agregar un contacto. Debes tener en cuenta lo siguiente: -> DONE
    # - El nombre y apellido no pueden ser una cadena vacía o solo espacios y se guardarán con la primera letra mayúscula y el resto minúsculas (ojo a los nombre compuestos)
    # - El email debe ser único en la lista de contactos, no puede ser una cadena vacía y debe contener el carácter @.
    # - El email se guardará tal cuál el usuario lo introduzca, con las mayúsculas y minúsculas que escriba. 
    #  (CORREO@gmail.com se considera el mismo email que correo@gmail.com)
    # - Pedir teléfonos hasta que el usuario introduzca una cadena vacía, es decir, que pulse la tecla <ENTER> sin introducir nada.
    # - Un teléfono debe estar compuesto solo por 9 números, aunque debe permitirse que se introduzcan espacios entre los números.
    # - Además, un número de teléfono puede incluir de manera opcional un prefijo +34.
    # - De igual manera, aunque existan espacios entre el prefijo y los 9 números al introducirlo, debe almacenarse sin espacios.
    # - Por ejemplo, será posible introducir el número +34 600 100 100, pero guardará +34600100100 y cuando se muestren los contactos, el telófono se mostrará como +34-600100100. 
    #TODO: Realizar una llamada a la función agregar_contacto con todo lo necesario para que funcione correctamente. -> DONE
    try:
        agregar_contacto(contactos)
    except Exception as e:
        print("***ERROR*** - ", e)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Realizar una llamada a la función eliminar_contacto con todo lo necesario para que funcione correctamente, eliminando el contacto con el email rciruelo@gmail.com -> DONE
    eliminar_contacto(contactos, "rciruelo@gmail.com")

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear función mostrar_contactos para que muestre todos los contactos de la agenda con el siguiente formato: -> DONE
    # ** IMPORTANTE: debe mostrarlos ordenados según el nombre, pero no modificar la lista de contactos de la agenda original **
    #
    # AGENDA (6)
    # ------
    # Nombre: Antonio Amargo (aamargo@gmail.com)
    # Teléfonos: niguno
    # ......
    # Nombre: Daniela Alba (danalba@gmail.com)
    # Teléfonos: +34-600606060 / +34-670898934
    # ......
    # Nombre: Laura Iglesias (liglesias@gmail.com)
    # Teléfonos: 666777333 / 666888555 / 607889988
    # ......
    # ** resto de contactos **
    #
    #TODO: Realizar una llamada a la función mostrar_contactos con todo lo necesario para que funcione correctamente. -> DONE
    mostrar_contactos(contactos)

    pulse_tecla_para_continuar()
    borrar_consola()

    #TODO: Crear un menú para gestionar la agenda con las funciones previamente desarrolladas y las nuevas que necesitéis: -> IN PROGRESS
    # AGENDA
    # ------
    # 1. Nuevo contacto
    # 2. Modificar contacto
    # 3. Eliminar contacto
    # 4. Vaciar agenda
    # 5. Cargar agenda inicial
    # 6. Mostrar contactos por criterio
    # 7. Mostrar la agenda completa
    # 8. Salir
    #
    # >> Seleccione una opción: 
    #
    #TODO: Para la opción 2, modificar un contacto, deberás desarrollar las funciones necesarias para actualizar la información de un contacto. -> IN PROGRESS
    #TODO: También deberás desarrollar la opción 6 que deberá preguntar por el criterio de búsqueda (nombre, apellido, email o telefono) y el valor a buscar para mostrar los contactos que encuentre en la agenda. -> IN PROGRESS
    agenda(contactos)


if __name__ == "__main__":
    main()
