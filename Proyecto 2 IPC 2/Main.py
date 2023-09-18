class Main:
    def __init__(self):
        pass

    def menu(self):
        print("╔══════════════════════════════════╗")
        print("║             Menú inicial         ║")
        print("╠══════════════════════════════════╣")
        print("║ 1. Inicializar sistema           ║")
        print("║ 2. Cargar XML de entrada         ║")
        print("║ 3. Generar XML de salida         ║")
        print("║ 4. Gestión de drones             ║")
        print("║ 5. Gestión de sistema de drones  ║")
        print("║ 6. Gestión de mensajes           ║")
        print("║ 7. Ayuda                         ║")
        print("║ 8. Salir                         ║")
        print("╚══════════════════════════════════╝")

        print("Ingrese una opción: ", end="")
        opcion = input()
        self.seleccionar_opcion(opcion)

    def seleccionar_opcion(self, opcion):
        if opcion.isnumeric():

            opcion = int(opcion)

            if opcion == 1:
                print("Inicializar sistema")
                self.menu()
                return
            elif opcion == 2:
                print("Cargar XML de entrada")
                self.menu()
                return
            elif opcion == 3:
                print("Generar XML de salida")
                self.menu()
                return
            elif opcion == 4:
                print("Gestión de drones")
                self.menu_drones()
                return
            elif opcion == 5:
                print("Gestión de sistema de drones")
                self.menu_sistema_drones()
                return
            elif opcion == 6:
                print("Gestión de mensajes")
                self.menu_mensajes()
                return
            elif opcion == 7:
                print("\nDatos del estudiante:")
                print("> Nombre: Irving Fernando Alvarado Asensio")
                print("> Carné: 202200349")
                print("> Curso: Introducción a la Programación y Computación 2 Sección N")
                print("> Carrera: Ingeniería en Ciencias y Sistemas")
                print("> Semestre: 4to\n")
                #Imprimir link a la documentacion
                self.menu()
                return
            elif opcion == 8:
                print("Salir")
                return
            else:
                print("Opción inválida")
                self.menu()
                return
        else:
            print("Opción inválida")
            self.menu()
            return
    
    def menu_drones(self):
        print("╔══════════════════════════════════╗")
        print("║         Gestión de drones        ║")
        print("╠══════════════════════════════════╣")
        print("║ 1. Ver listado de drones         ║")
        print("║ 2. Agregar nuevo dron            ║")
        print("║ 3. Volver al menu                ║")
        print("╚══════════════════════════════════╝")

        print("Ingrese una opción: ", end="")
        opcion = input()
        self.seleccionar_opcion_drones(opcion)
    
    def seleccionar_opcion_drones(self, opcion):
        if opcion.isnumeric():

            opcion = int(opcion)

            if opcion == 1:
                print("Ver listado de drones")
                self.menu_drones()
                return
            elif opcion == 2:
                print("Agregar nuevo dron")
                self.menu_drones()
                return
            elif opcion == 3:
                print("Volver al menu")
                self.menu()
                return
            else:
                print("Opción inválida")
                self.menu_drones()
                return
        else:
            print("Opción inválida")
            self.menu_drones()
            return
    
    def menu_sistema_drones(self):
        print("╔══════════════════════════════════╗")
        print("║   Gestión de sistema de drones   ║")
        print("╠══════════════════════════════════╣")
        print("║ 1. Mostrar listado de sistemas   ║")
        print("║ 2. Volver al menu                ║")
        print("╚══════════════════════════════════╝")

        print("Ingrese una opción: ", end="")
        opcion = input()
        self.seleccionar_opcion_sistema_drones(opcion)

    def seleccionar_opcion_sistema_drones(self, opcion):
        if opcion.isnumeric():

            opcion = int(opcion)

            if opcion == 1:
                print("Mostrar listado de sistemas")
                self.menu_sistema_drones()
                return
            elif opcion == 2:
                print("Volver al menu")
                self.menu()
                return
            else:
                print("Opción inválida")
                self.menu_sistema_drones()
                return
        else:
            print("Opción inválida")
            self.menu_sistema_drones()
            return
    

    def menu_mensajes(self):
        print("╔══════════════════════════════════╗")
        print("║        Gestión de mensajes       ║")
        print("╠══════════════════════════════════╣")
        print("║ 1. Ver listado de mensajes e ins.║")
        print("║ 2. Ver instrucciones para enviar ║")
        print("║ 3. Volver al menu                ║")
        print("╚══════════════════════════════════╝")

        print("Ingrese una opción: ", end="")
        opcion = input()
        self.seleccionar_opcion_mensajes(opcion)

    def seleccionar_opcion_mensajes(self, opcion):
        if opcion.isnumeric():

            opcion = int(opcion)

            if opcion == 1:
                print("Ver listado de mensajes e instrucciones")
                self.menu_mensajes()
                return
            elif opcion == 2:
                print("Ver instrucciones para enviar")
                self.menu_mensajes()
                return
            elif opcion == 3:
                print("Volver al menu")
                self.menu()
                return
            else:
                print("Opción inválida")
                self.menu_mensajes()
                return
        else:
            print("Opción inválida")
            self.menu_mensajes()
            return

if __name__ == "__main__":
    main = Main()
    main.menu()