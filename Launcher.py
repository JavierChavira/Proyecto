import os
import time

#ejecutar la carga de datos
def ManejoDatos():
    os.system("py Proyecto_Final.py --update")
    time.sleep(2)


#ejecutar Streamlit
def Visualizacion():
    os.system("py -m streamlit run Proyecto_Final.py")
    time.sleep(2)


#Buen día Maestro
#Para que funcione el proyecto es necesario que tenga creada la Base de datos "Proyecto" en SQL Server.
#Primero tiene que ejecutar la primera opción que es la que actualiza los indicadores y los guarda en SQL Server,
#son varias tablas así que por favor tenga paciencia.
#Después debe de iniciar la visualización. En esta parte también trabajamos con datos y llamamos
#las tablas desde python a SQL Server.
#Debera de analizar cual es el driver de SQL Server de su computadora
# y cambiar en el archivo "Proyecto_Final.py" el usuario y los drivers. Por favor
# Y Nada mas por si acaso, debera de revisar si su consola funciona con py o python,
# en nuestro caso utilizamos "py" para ejecutar los comandos.
def main_menu():
    opc = 0
    while opc !=3:
        print("           MENÚ PRINCIPAL")
        print("1. Actualizar indicadores y guardar en SQL Server")
        print("2. Iniciar visualización (Dashboard Streamlit)")
        print("3. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ManejoDatos()

        elif opcion == "2":
            Visualizacion()

        elif opcion == "3":
            print("\nSaliendo del programa...")
            break

        else:
            print("\nOpción no válida, intente de nuevo.")
            time.sleep(1)


if __name__ == "__main__":
    main_menu()
