import tkinter as tk
from tkinter import filedialog, messagebox
from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Procesar_xml import *
from TiempoOptimo import *
from Dron import Dron

class MainGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Encriptación de mensajes")
        self.root.geometry("800x600")  # Cambiar el tamaño de la ventana principal
        self.root.resizable(False, False)  # Evitar que la ventana principal cambie de tamaño
        #Agregar texto "Hola" al centro de la ventana principal
        self.label = tk.Label(self.root, text="Encriptación de mensajes", font=("roboto", 40, "bold"))
        self.label.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        
        self.imagen = tk.PhotoImage(file="imagenDron.png")
        self.label_imagen = tk.Label(self.root, image=self.imagen)
        self.label_imagen.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

        # Crear el menú principal   
        self.menu = tk.Menu(root)
        root.config(menu=self.menu)

        # Opciones del menú
        self.menu_mensajes = tk.Menu(self.menu, tearoff=0)
        #self.menu.add_cascade(label="Sistema", menu=self.menu_sistema)
        self.menu.add_command(label="Inicializar sistema", command=self.inicializar_sistema)
        self.menu.add_command(label="Cargar archivo XML", command=self.cargar_xml)
        self.menu.add_command(label="Generar archivo XML de salida", command=self.generar_xml)
        self.menu.add_command(label="Gestión de drones", command=self.gestion_drones)
        self.menu.add_command(label="Gestión de sistema de drones", command=self.generar_imagen_sistema)
        self.menu.add_cascade(label="Gestión de mensajes", menu=self.menu_mensajes)
        self.menu_mensajes.add_command(label="Ver listado de mensajes", command=self.ver_listado_mensajes)
        self.menu_mensajes.add_command(label="Ver instrucciones", command=self.ver_instrucciones)
        self.menu.add_command(label="Ayuda", command=self.mostrar_ayuda)

        #Agregamos listas generales
        self.lista_mensajes = ListaDoblementeEnlazada()
        self.lista_drones = ListaDoblementeEnlazada()
        self.lista_sistema = ListaDoblementeEnlazada()
        self.lista_instrucciones = ListaDoblementeEnlazada()

    def mostrar_ayuda(self):
        mensaje_ayuda = """Datos del estudiante:
Nombre: Irving Fernando Alvarado Asensio
Carné: 202200349
Curso: Introducción a la Programación y Computación 2 Sección N
Carrera: Ingeniería en Ciencias y Sistemas
Semestre: 4to"""
        messagebox.showinfo("Ayuda", mensaje_ayuda)

    def inicializar_sistema(self):
        #Reiniciamos listas
        self.lista_mensajes = ListaDoblementeEnlazada()
        self.lista_drones = ListaDoblementeEnlazada()
        self.lista_sistema = ListaDoblementeEnlazada()
        self.lista_instrucciones = ListaDoblementeEnlazada()


    def cargar_xml(self):
        archivo_seleccionado = filedialog.askopenfilename(filetypes=[("Archivos XML", "*.xml")])
        if archivo_seleccionado:
            messagebox.showinfo("Archivo seleccionado", f"Archivo XML seleccionado: {archivo_seleccionado}")
            try:
                procesar_entrada(archivo_seleccionado, self.lista_drones, self.lista_sistema, self.lista_mensajes)
                messagebox.showinfo("Procesamiento exitoso", "El archivo XML se procesó correctamente")
                self.lista_drones.imprimir()
                print(self.lista_drones.contar_elementos())
            except:
                messagebox.showerror("Error", "Ocurrió un error al procesar el archivo XML")
        else:
            messagebox.showinfo("Archivo no seleccionado", "No se seleccionó ningún archivo XML")

    def generar_xml(self):
        print()
        self.lista_drones.imprimir()
        pass

    def gestion_drones(self):
        # Crear una nueva ventana emergente para la gestión de drones
        ventana_drones = tk.Toplevel(self.root)
        ventana_drones.title("Gestión de Drones")
        ventana_drones.geometry("400x300")

        # Texto grande
        texto_drones = tk.Text(ventana_drones, height=10, width=40)
        texto_drones.pack(padx=10, pady=10)

        # Campo de texto para agregar
        entrada_dron = tk.Entry(ventana_drones)
        entrada_dron.pack(padx=10, pady=5)

        self.obtener_drones(texto_drones)
        # Botón para agregar
        boton_agregar = tk.Button(ventana_drones, text="Agregar", command=lambda: self.agregar_dron(texto_drones, entrada_dron))
        boton_agregar.pack(padx=10, pady=5)
        #Boton mostrar drones
        #boton_mostrar_drones = tk.Button(ventana_drones, text="Mostrar Drones", command=lambda: self.obtener_drones(texto_drones))
        #boton_mostrar_drones.pack(padx=10, pady=5)
    
    def obtener_drones(self, texto_drones):
        try:
            #Limpiamos todo el texto de la ventana
            texto_drones.delete("1.0", tk.END)
            # Rellenamos la lista de drones con los drones que ya existen
            lista_drones_ordenados = obtenerDronesOrdenadosAlfabeticamente(self.lista_drones)
            dron_actual = lista_drones_ordenados.inicio
            while dron_actual != None:
                texto_drones.insert(tk.END, dron_actual.objeto.nombre + "\n")
                dron_actual = dron_actual.siguiente
        except:
            messagebox.showerror("Error", "No se han podido obtener los drones")
    
    def obtener_mensajes(self, texto_mensajes):
            texto_mensajes.delete("1.0", tk.END)
            # Rellenamos la lista de mensajes junto a sus instrucciones
            lista_mensajes_ordenados = obtenerMensajesOrdenadosAlfabeticamente(self.lista_mensajes)
            mensaje_actual = lista_mensajes_ordenados.inicio
            contador = 1
            while mensaje_actual != None:
                texto_mensajes.insert(tk.END, "No." + str(contador) + " Nombre: "+ str(mensaje_actual.objeto.nombre)  +  " - Sistema: " + str(mensaje_actual.objeto.sistema) + " - Mensaje: " + str(mensaje_actual.objeto.mensaje_decodificado) + "\n")
                texto_mensajes.insert(tk.END, "Instrucciones: \n")
                instruccion_actual = mensaje_actual.objeto.lista_instrucciones.inicio
                while instruccion_actual != None:
                    texto_mensajes.insert(tk.END, str(instruccion_actual.objeto.nombreDron) + " - " + str(instruccion_actual.objeto.altura) + "\n")
                    instruccion_actual = instruccion_actual.siguiente
                texto_mensajes.insert(tk.END, "\n")
                mensaje_actual = mensaje_actual.siguiente
                contador += 1



    def agregar_dron(self, texto_drones, entrada_dron):
        try:
            #Se agregan los drones a la lista de drones
            nombre_dron = entrada_dron.get()
            if nombre_dron == "":
                messagebox.showerror("Error", "No se ingresó un nombre de dron")
                return
            if self.lista_drones.buscar(nombre_dron) != None:
                messagebox.showerror("Error", "El dron ya existe")
                return
            
            dron_nuevo = Dron(nombre_dron)
            self.lista_drones.insertar(dron_nuevo)
            print("Se ha agregado el dron correctamente")
            self.obtener_drones(texto_drones)
            #Limpiamos el campo de texto
            entrada_dron.delete(0, tk.END)
        except:
            messagebox.showerror("Error", "No se ha podido agregar el dron")

    def generar_imagen_sistema(self):
        try:
            graficarSistemas(self.lista_sistema)
        except:
            messagebox.showerror("Error", "No se ha podido generar el grafico del sistema")

    def ver_listado_mensajes(self):
        # Crear una nueva ventana emergente para ver listado de mensajes
        ventana_listado_mensajes = tk.Toplevel(self.root)
        ventana_listado_mensajes.title("Ver Listado de Mensajes")
        ventana_listado_mensajes.geometry("400x300")

        # Texto grande
        texto_mensajes = tk.Text(ventana_listado_mensajes, height=50, width=80)
        texto_mensajes.pack(padx=10, pady=10)

        self.obtener_mensajes(texto_mensajes)

    def ver_instrucciones(self):
        # Crear una nueva ventana emergente para ver instrucciones
        ventana_instrucciones = tk.Toplevel(self.root)
        ventana_instrucciones.title("Ver Instrucciones")
        ventana_instrucciones.geometry("500x400")

        # Caja de texto
        texto_mensajes = tk.Text(ventana_instrucciones, height=10, width=60)
        texto_mensajes.pack(padx=10, pady=5)
        
        # Campo de entrada para ID del mensaje
        id_mensaje_entry = tk.Entry(ventana_instrucciones, width=30)
        id_mensaje_entry.insert(0, "Escribe la ID del mensaje")  # Placeholder
        id_mensaje_entry.pack(padx=10, pady=5)

        # Evento para borrar el placeholder cuando el usuario haga clic en el campo
        def borrar_placeholder(event):
            if id_mensaje_entry.get() == "Escribe la ID del mensaje":
                id_mensaje_entry.delete(0, tk.END)

        # Enlaza el evento con el campo de entrada
        id_mensaje_entry.bind("<FocusIn>", borrar_placeholder)
        
        # Campos de texto para información del mensaje
        campo_texto_1 = tk.Entry(ventana_instrucciones, width=30)
        campo_texto_1.pack(padx=10, pady=5)
        campo_texto_2 = tk.Entry(ventana_instrucciones, width=30)
        campo_texto_2.pack(padx=10, pady=5)
        campo_texto_3 = tk.Entry(ventana_instrucciones, width=30)
        campo_texto_3.pack(padx=10, pady=5)

        def seleccionar_mensaje():
            # Obtener el ID del mensaje desde el campo de entrada
            id_mensaje = id_mensaje_entry.get()
            
            # Llamar al método para buscar el mensaje por su ID (debes implementarlo)
            mensaje = obtener_mensaje_por_id(id_mensaje)
            
            # Rellenar los campos de texto con la información del mensaje si se encuentra
            if mensaje:

                    lista_formas_posibles = ListaDoblementeEnlazada()
                    dron_actual = mensaje.sistemaObjeto.drones.inicio
                    altura_actual = dron_actual.objeto.lista_alturas.inicio
                    caracter_actual = mensaje.lista_caracteres.inicio

                    lista_formas_posibles = obtenerFormasPosibles(mensaje, None, dron_actual, altura_actual, caracter_actual, lista_formas_posibles)
                    if lista_formas_posibles.contar_elementos() == 0:
                        messagebox.showerror("Error", "No es posible formar el mensaje con el sistema dado")
                        return
                    else:
                        tiempo_minimo = obtenerTiempoDeCadaForma(lista_formas_posibles, self.lista_drones)
                        mensaje.tiempo_optimo = tiempo_minimo.tiempo
                        generarInstrucciones(tiempo_minimo, self.lista_instrucciones, mensaje)


                    campo_texto_1.delete(0, tk.END)
                    campo_texto_1.insert(0, mensaje.sistema)
                    campo_texto_2.delete(0, tk.END)
                    campo_texto_2.insert(0, mensaje.mensaje_decodificado)
                    campo_texto_3.delete(0, tk.END)
                    campo_texto_3.insert(0, mensaje.tiempo_optimo)

                    #Imprimimos la lista de instrucciones
                    instruccion_actual = self.lista_instrucciones.inicio
                    while instruccion_actual != None:
                        instruccion = instruccion_actual.objeto.instrucciones.inicio
                        while instruccion != None:
                            print(instruccion.objeto.tiempo, instruccion.objeto.dron.nombre, instruccion.objeto.accion)
                            instruccion = instruccion.siguiente
                        instruccion_actual = instruccion_actual.siguiente
            else:
                messagebox.showerror("Error", "No se encontró el mensaje con el ID ingresado")
                return
            
        def ver_grafico_instrucciones():
            id_mensaje = id_mensaje_entry.get()
            mensaje = obtener_mensaje_por_id(id_mensaje)
            entro = False

            if mensaje:
                instruccion_actual = self.lista_instrucciones.inicio
                while instruccion_actual is not None:
                    if instruccion_actual.objeto.mensaje.id_mensaje == mensaje.id_mensaje:
                        entro = True
                        grafo = graphviz.Digraph('Instrucciones para transmitir mensajes', filename='Instrucciones.gv', format='png')

                        grafo.node(str(instruccion_actual.objeto.mensaje.nombre), str(instruccion_actual.objeto.mensaje.nombre))
                        grafo.node(str(instruccion_actual.objeto.mensaje.nombre) + "tiempo", "Tiempo (seg)")
                        grafo.edge(str(instruccion_actual.objeto.mensaje.nombre), str(instruccion_actual.objeto.mensaje.nombre) + "tiempo")
                        
                        #Agreamos numeracion de segundos
                        for i in range(1, instruccion_actual.objeto.mensaje.tiempo_optimo + 1):
                            grafo.node(str(instruccion_actual.objeto.mensaje.nombre) + "tiempo" + str(i), str(i))
                            if i == 1:
                                grafo.edge(str(instruccion_actual.objeto.mensaje.nombre) + "tiempo", str(instruccion_actual.objeto.mensaje.nombre) + "tiempo" + str(i))
                            else:
                                grafo.edge(str(instruccion_actual.objeto.mensaje.nombre) + "tiempo" + str(i-1), str(instruccion_actual.objeto.mensaje.nombre) + "tiempo" + str(i))
                        
                        

                        #Añadimos nodos para cada dron del sistema
                        dron_actual = instruccion_actual.objeto.mensaje.sistemaObjeto.drones.inicio
                        while dron_actual is not None:
                            grafo.node(str(dron_actual.id_nodo), str(dron_actual.objeto.dron.nombre))
                            grafo.edge(str(instruccion_actual.objeto.mensaje.nombre), str(dron_actual.id_nodo))
                            primer_tiempo = True
                            #Añadimos nodos para cada instruccion del dron
                            instruccion_dron_actual = instruccion_actual.objeto.instrucciones.inicio
                            while instruccion_dron_actual is not None:
                                if instruccion_dron_actual.objeto.dron.nombre == dron_actual.objeto.dron.nombre:
                                    grafo.node(str(instruccion_dron_actual.id_nodo), str(instruccion_dron_actual.objeto.accion))
                                    if primer_tiempo:
                                        grafo.edge(str(dron_actual.id_nodo), str(instruccion_dron_actual.id_nodo))
                                        primer_tiempo = False
                                    else:
                                        grafo.edge(str(instruccion_dron_actual.anterior.id_nodo), str(instruccion_dron_actual.id_nodo))
                                instruccion_dron_actual = instruccion_dron_actual.siguiente

                            dron_actual = dron_actual.siguiente
                        break
                    else:
                        instruccion_actual = instruccion_actual.siguiente
                if entro:
                    grafo.render(view=True)
                else:
                    messagebox.showerror("Error", "Procese el mensaje primero")




                     

        def obtener_mensaje_por_id(id_mensaje):
            mensaje_actual = self.lista_mensajes.inicio
            while mensaje_actual != None:
                if str(mensaje_actual.objeto.id_mensaje) == str(id_mensaje):
                    return mensaje_actual.objeto
                mensaje_actual = mensaje_actual.siguiente

        # Botón para seleccionar mensaje
        boton_seleccionar = tk.Button(ventana_instrucciones, text="Seleccionar", command=seleccionar_mensaje)
        boton_seleccionar.pack(padx=10, pady=5)

        # Botón para ver el "Grafico de Instrucciones"
        boton_ver_grafico = tk.Button(ventana_instrucciones, text="Ver Grafico de Instrucciones", command=ver_grafico_instrucciones)
        boton_ver_grafico.pack(padx=10, pady=5)

        self.obtener_mensaje_sin_ordenar(texto_mensajes)




                        

    def obtener_mensaje_sin_ordenar(self, texto_mensajes):
        mensaje_actual = self.lista_mensajes.inicio
        while mensaje_actual != None:
            texto_mensajes.insert(tk.END, "ID: " + str(mensaje_actual.objeto.id_mensaje) + " - Nombre: "+ str(mensaje_actual.objeto.nombre) +  " - Sistema: " + str(mensaje_actual.objeto.sistema) + " - Mensaje: " + str(mensaje_actual.objeto.mensaje_decodificado) + "\n")
            texto_mensajes.insert(tk.END, "Instrucciones:")
            instruccion_actual = mensaje_actual.objeto.lista_instrucciones.inicio
            while instruccion_actual != None:
                texto_mensajes.insert(tk.END, str(instruccion_actual.objeto.nombreDron) + " - " + str(instruccion_actual.objeto.altura) + "\n")
                instruccion_actual = instruccion_actual.siguiente
            texto_mensajes.insert(tk.END, "\n")

            mensaje_actual = mensaje_actual.siguiente



if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()