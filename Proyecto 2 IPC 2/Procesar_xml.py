import xml.etree.ElementTree as ET
from Dron import Dron
from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from SistemaDrones import SistemaDrones
from DronSistema import DronSistema
from Altura import Altura
from Mensaje import Mensaje
import copy
import graphviz
from Instruccion import Instruccion
from tkinter import messagebox
import xml.dom.minidom
from tkinter import messagebox

contador_mensaje = 1
contador_drones = 0

def procesar_entrada(entrada, lista_drones, lista_sistemas, lista_mensajes):
    global contador_mensaje, contador_drones
    #Entrada es la direccion del archivo XML
    try:
        arbol = ET.parse(entrada)
        raiz = arbol.getroot()
    except Exception as exception:
        print("Error al abrir el archivo")
        print(exception)
        return

    for listaDrones in raiz.findall("listaDrones"):

        for dron in listaDrones.findall("dron"):
            
            #Si el dron ya existe, se omite
            if lista_drones.buscar(dron.text):
                print(f"> El dron {dron.text} ya existe, se omitirá")
                continue

            dron_nuevo = Dron(dron.text)
            lista_drones.insertar(dron_nuevo)
            print(f"> Se ha agregado el dron {dron.text} a la lista de drones")
    

    #Modificaremos la logica para permitir que los sistemas se puedan crear desde dos o mas archivos de entrada, para eso el sistema de ambos archivos debe tener el mismo nombre, la misma cantidad de drones y la misma altura maxima.
    #Primero se crearan todos los objetos para la cantidad de drones, y alturas. Luego se rellenaran con los datos de los archivos de entrada. Si alguno de los datos no aparece en el archivo de entrada, la letra de la altura se colocara como null y si algun dron no aparece se creara el sistema con el nombre SinDron y sus letras seran null

    for listaSistemas in raiz.findall("listaSistemasDrones"):
        for sistemaDrones in listaSistemas.findall("sistemaDrones"):
            nombreDelSistema = sistemaDrones.get("nombre")

            for alturaMaxima in sistemaDrones.findall("alturaMaxima"):
                altura_maxima = int(alturaMaxima.text)
            
            for cantidadDrones in sistemaDrones.findall("cantidadDrones"):
                cantidad_drones = int(cantidadDrones.text)

            #Verificar que la cantidad de drones sea mayor a 0 y menor o igual a 200 y que la altura maxima sea mayor a 0 y menor o igual a 100, Si superan estos datos solo se tomara en cuenta esos valores maximos
            if cantidad_drones > 200:
                cantidad_drones = 200
                print("> La cantidad de drones supera el limite, se tomará el valor máximo de 200")
            elif cantidad_drones < 1:
                #Se omite el sistema
                print("> La cantidad de drones es menor a 1, se omitirá")
                continue

            if altura_maxima > 100:
                print("> La altura maxima supera el limite, se tomará el valor máximo de 100")
                altura_maxima = 100
            elif altura_maxima < 1:
                #Se omite el sistema
                print("> La altura maxima es menor a 1, se omitirá")
                continue

            #Dos casos se trata de un sistema nuevo o se trata de un sistema que ya existe, si ya existe se agregaran los drones y las alturas al sistema existente modificando los datos que ya esten presentes, si no existe se creara un sistema nuevo
            existeElSistema = lista_sistemas.buscar(nombreDelSistema)

            if existeElSistema == None:
                sistema_nuevo = SistemaDrones(nombreDelSistema, altura_maxima, cantidad_drones)
                lista_sistemas.insertar(sistema_nuevo)

                #Se crean los drones y las alturas
                for i in range(1, cantidad_drones + 1):
                    dron_nuevo = DronSistema(Dron("DronSinNombre"))
                    sistema_nuevo.drones.insertar(dron_nuevo)

                    for j in range(1, altura_maxima + 1):
                        altura_nueva = Altura(j, "null")
                        dron_nuevo.lista_alturas.insertar(altura_nueva)
            else:
                #Caso en el que el sistema ya existe, verificamos que la cantidad de drones y la altura maxima coincidan con el sistema existente, si no coinciden se omitira el sistema
                if existeElSistema.altura_maxima != altura_maxima or existeElSistema.cantidad_drones != cantidad_drones:
                    messagebox.showerror("Error", "La cantidad de drones o la altura maxima del sistema "+nombreDelSistema+" no coinciden con el sistema existente, se omitiran los datos del sistema")
                    continue
                else:
                    sistema_nuevo = existeElSistema

            #Se editan los drones y las alturas con los datos del archivo de entrada

            for contenido in sistemaDrones.findall("contenido"):

                for dron in contenido.findall("dron"):
                    #Primero verificamos si el dron ya pertenece a la lista de drones del sistema, si no existe se iterara sobre los drones del sistema hasta encontrar uno cuyo nombre sea DroneSinNombre, si no se encuentra ese espacio vacio el dron se omitira el sistema 
                    dron_nuevo =  sistema_nuevo.drones.buscar_dron_sistema(dron.text)
                    print("nombre del sistema", nombreDelSistema)
                    print(dron_nuevo, "Se encontró el dron")
                    if dron_nuevo == None:
                        dron_nuevo = sistema_nuevo.drones.buscar_dron_sistema("DronSinNombre")
                        print(dron_nuevo, "Se encontró el dron sin nombre")
                        if dron_nuevo == None:
                            print("No se encontró el dron sin nombre")
                            continue
                        else:
                            dron_nuevo.dron.nombre = dron.text

                if dron_nuevo == None:
                    messagebox.showerror("Error", "No se pudo agregar el dron "+dron.text+" al sistema "+nombreDelSistema+", porque no hay espacios libre se omitirá el sistema")
                    continue
            
                #En este caso se modificaran las letras de las alturas de los drones
                for alturas in contenido.findall("alturas"):
                    
                    for i in range(1,altura_maxima+1):

                        for altura in alturas.findall("altura"):
                            
                            #Si la altura no coincide con la altura actual, se omite
                            if int(altura.get("valor")) != i:
                                continue

                            letra = altura.text
                            altura = int(altura.get("valor"))

                            if letra == " " or letra == "" or letra == None:
                                #Es un espacio vacio
                                letra = " "

                            #Se busca la altura en el dron y se modifica la letra
                            altura_nueva = dron_nuevo.lista_alturas.buscar_altura(altura)
                            altura_nueva.letra = letra

    actualizar_mensajes(lista_mensajes)

    
    """
    for listaSistemas in raiz.findall("listaSistemasDrones"):


        for sistemaDrones in listaSistemas.findall("sistemaDrones"):
            contador_drones = 0
            errores = 0
            

            for alturaMaxima in sistemaDrones.findall("alturaMaxima"):
                altura_maxima = int(alturaMaxima.text)
            
            for cantidadDrones in sistemaDrones.findall("cantidadDrones"):
                cantidad_drones = int(cantidadDrones.text)

            #Verificar que la cantidad de drones sea mayor a 0 y menor o igual a 200 y que la altura maxima sea mayor a 0 y menor o igual a 100, Si superan estos datos solo se tomara en cuenta esos valores maximos
            if cantidad_drones > 200:
                cantidad_drones = 200
                print("> La cantidad de drones supera el limite, se tomará el valor máximo de 200")
            elif cantidad_drones < 1:
                #Se omite el sistema
                print("> La cantidad de drones es menor a 1, se omitirá")
                continue
            
            if altura_maxima > 100:
                print("> La altura maxima supera el limite, se tomará el valor máximo de 100")
                altura_maxima = 100
            elif altura_maxima < 1:
                #Se omite el sistema
                print("> La altura maxima es menor a 1, se omitirá")
                continue

        
            sistema_nuevo = SistemaDrones(sistemaDrones.get("nombre"), altura_maxima, cantidad_drones)
            
            #Si el sistema ya existe, se omite
            if lista_sistemas.buscar(sistema_nuevo.nombre):
                print(f"> El sistema {sistema_nuevo.nombre} ya existe, se omitirá")
                continue
    
            lista_sistemas.insertar(sistema_nuevo)

            for contenido in sistemaDrones.findall("contenido"):
                for dron in contenido.findall("dron"):

                    dron = lista_drones.buscar(dron.text)
                    dron_sistema_nuevo = DronSistema(dron)
                    sistema_nuevo.drones.insertar(dron_sistema_nuevo)
                
                #Si el dron no existe, se omite el sistema
                if dron == None:
                    print(f"> El dron {dron.text} no existe, se omitirá el sistema {sistemaDrones.get('nombre')}")
                    errores += 1
                    continue

                contador_drones += 1
                    
                
                for alturas in contenido.findall("alturas"):

                    contador_alturas = 0

                    for i in range(1,altura_maxima+1):

                        for altura in alturas.findall("altura"):
                            
                            #Si la altura no coincide con la altura actual, se omite
                            if int(altura.get("valor")) != i:
                                continue

                            letra = altura.text
                            altura = int(altura.get("valor"))

                            if letra == " " or letra == "":
                                #Es un espacio vacio
                                letra = " "

                            altura_nueva = Altura(altura, letra)
                            dron_sistema_nuevo.lista_alturas.insertar(altura_nueva)
                            contador_alturas += 1
                        
                    if contador_alturas != altura_maxima:
                        print(f"> La cantidad de alturas no coincide con la altura máxima del sistema {sistemaDrones.get('nombre')}, se omitirá")
                        errores += 1
                        continue
            
            if contador_drones != cantidad_drones:
                print(f"> La cantidad de drones no coincide con la cantidad de drones del sistema {sistemaDrones.get('nombre')}, se omitirá")
                errores += 1

            if errores > 0:
                print("Elimino")
                lista_sistemas.eliminar(sistema_nuevo.nombre)"""

    #Se llenara la lista de mensajes obtenidos del archivo de entrada
    for listaMensajes in raiz.findall("listaMensajes"):

        for mensaje in listaMensajes.findall("Mensaje"):

            nombre = mensaje.get("nombre")
            
            for sistema in mensaje.findall("sistemaDrones"):
                nombre_sistema = sistema.text
            
            if lista_sistemas.buscar(nombre_sistema) == None:
                print(f"> El sistema {nombre_sistema} no existe, se omitirá el mensaje {nombre}")
                continue

            mensaje_nuevo = Mensaje(contador_mensaje, nombre, nombre_sistema, lista_sistemas.buscar(nombre_sistema))
            contador_mensaje += 1
            lista_mensajes.insertar(mensaje_nuevo)

            
            for instrucciones in mensaje.findall("instrucciones"):
                contador_instruccion = 1
                for instruccion in instrucciones.findall("instruccion"):
                    nombre_dron = instruccion.get("dron")
                    altura = int(instruccion.text)
                    letra = obtenerLetra(lista_sistemas, nombre_sistema, nombre_dron, altura)
                    instruccion_nueva = Instruccion(nombre_dron, altura, letra, contador_instruccion)
                    contador_instruccion += 1
                    mensaje_nuevo.lista_caracteres.insertar(letra)
                    mensaje_nuevo.mensaje_decodificado += letra
                    mensaje_nuevo.lista_instrucciones.insertar(instruccion_nueva)

    print("Se ha procesado la entrada correctamente")
                    


def obtenerLetra(lista_sistemas, sistema, dron, altura):
    try:
        #Se obtiene la letra de la altura del dron en el sistema
        if lista_sistemas == None:
            sistema_actual = sistema
        else:
            sistema_actual = lista_sistemas.buscar(sistema)
            
        altura = sistema_actual.drones.buscar_dron_sistema_altura(dron, altura)
        letra = altura.letra
        return letra
    except Exception as e:
        print(e)
        return "null"

def obtenerDronesOrdenadosAlfabeticamente(lista_drones):
    try:
        # Se ordenan los drones alfabéticamente y se retorna una lista con los drones ordenados
        lista_drones_ordenados = ListaDoblementeEnlazada()
        
        # Crear una copia independiente de la lista original
        lista_drones_aux = copy.deepcopy(lista_drones)
        
        dron_actual = lista_drones_aux.inicio
        while dron_actual != None:
            dron_menor = dron_actual
            dron_actual = dron_actual.siguiente
            dron_actual_aux = dron_actual
            while dron_actual_aux != None:
                if dron_actual_aux.objeto.nombre < dron_menor.objeto.nombre:
                    dron_menor = dron_actual_aux
                dron_actual_aux = dron_actual_aux.siguiente
            lista_drones_ordenados.insertar(dron_menor.objeto)
            lista_drones_aux.eliminar(dron_menor.objeto.nombre)
            dron_actual = lista_drones_aux.inicio

        return lista_drones_ordenados
    
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "No se pudo ordenar los drones")
        return None

def obtenerMensajesOrdenadosAlfabeticamente(lista_mensajes):
    try:
        lista_mensajes_ordenados = ListaDoblementeEnlazada()
        lista_mensajes_aux = copy.deepcopy(lista_mensajes)
        mensaje_actual = lista_mensajes_aux.inicio
        while mensaje_actual != None:
            mensaje_menor = mensaje_actual
            mensaje_actual = mensaje_actual.siguiente
            mensaje_actual_aux = mensaje_actual
            while mensaje_actual_aux != None:
                if mensaje_actual_aux.objeto.nombre < mensaje_menor.objeto.nombre:
                    mensaje_menor = mensaje_actual_aux
                mensaje_actual_aux = mensaje_actual_aux.siguiente
            lista_mensajes_ordenados.insertar(mensaje_menor.objeto)
            lista_mensajes_aux.eliminar(mensaje_menor.objeto.nombre)
            mensaje_actual = lista_mensajes_aux.inicio

        return lista_mensajes_ordenados
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "No se pudo ordenar los mensajes")
        return None

def graficarSistemas(lista_sistemas):
    # Inicializar el grafo con el nombre Sistemas de drones
    grafo = graphviz.Digraph('Sistemas de drones', filename='Sistemas_de_drones.gv', format='png')

    sistema_actual = lista_sistemas.inicio

    while sistema_actual != None:
        # Crear el código HTML para la tabla
        tabla_html = "<<table border='1' cellborder='1' cellspacing='0'><tr><td bgcolor='#80ed99' colspan='"+str(sistema_actual.objeto.cantidad_drones + 1)+"' align='center'><b>"+str(sistema_actual.objeto.nombre)+"</b></td></tr><tr><td bgcolor = '#c7f9cc' align='center'>Altura (mts)</td>"
        #Queda pendiente cerrar el tr
        #Agregamos el nombre de cada dron
        dron_actual = sistema_actual.objeto.drones.inicio
        while dron_actual != None:
            tabla_html += "<td bgcolor='#c7f9cc' align='center'>"+str(dron_actual.objeto.dron.nombre)+"</td>"
            dron_actual = dron_actual.siguiente

        # Cerrar el tr
        tabla_html += "</tr>"
        

        #Agregamos las filas de las alturas de cada dron, además del numero de altura
        for i in range(1, sistema_actual.objeto.altura_maxima + 1):
            tabla_html += "<tr><td align='center'>"+str(i)+"</td>"
            dron_actual = sistema_actual.objeto.drones.inicio
            while dron_actual != None:
                altura_actual = dron_actual.objeto.lista_alturas.inicio
                while altura_actual != None:
                    if altura_actual.objeto.altura == i:
                        tabla_html += "<td align='center'>"+str(altura_actual.objeto.letra)+"</td>"
                    altura_actual = altura_actual.siguiente
                dron_actual = dron_actual.siguiente
            tabla_html += "</tr>"

        
        # Cerrar la tabla HTML
        tabla_html += "</table>>"
        
        # Agregar el nodo con formato HTML
        grafo.node(str(sistema_actual.id_nodo), label=tabla_html, shape='none', margin='0')
        
        sistema_actual = sistema_actual.siguiente

    grafo.view()

        

    

                






"""
lista_drones = ListaDoblementeEnlazada()
lista_sistemas = ListaDoblementeEnlazada()
lista_mensajes = ListaDoblementeEnlazada()

procesar_entrada("entradaV3.xml", lista_drones, lista_sistemas, lista_mensajes)

sistema_actual = lista_sistemas.inicio

while sistema_actual != None:
    print(sistema_actual.objeto.nombre)

    dron_actual = sistema_actual.objeto.drones.inicio
    while dron_actual != None:
        print(dron_actual.objeto.dron.nombre)
        altura_actual = dron_actual.objeto.lista_alturas.inicio
        while altura_actual != None:
            print(str(altura_actual.objeto.altura) + " - "+altura_actual.objeto.letra)
            altura_actual = altura_actual.siguiente
        dron_actual = dron_actual.siguiente
    sistema_actual = sistema_actual.siguiente

mensaje_actual = lista_mensajes.inicio
while mensaje_actual != None:
    print(mensaje_actual.objeto.nombre)
    print(mensaje_actual.objeto.mensaje_decodificado)
    mensaje_actual = mensaje_actual.siguiente

    """


def escribir_salida(lista_instrucciones):
    try:
        if lista_instrucciones.contar_elementos() == 0:
            messagebox.showerror("Error", "No se pudo escribir el archivo de salida, no se han procesado mensajes")
            
        else:
            respuesta = ET.Element("respuesta")
            listaMensajes = ET.SubElement(respuesta, "listaMensajes")
            instruccion_actual = lista_instrucciones.inicio
            
            while instruccion_actual != None:

                mensaje = ET.SubElement(listaMensajes, "mensaje")

                mensaje_objeto = instruccion_actual.objeto.mensaje

                mensaje.set("nombre", mensaje_objeto.nombre)

                SistemaDrones = ET.SubElement(mensaje, "SistemaDrones")

                SistemaDrones.text = mensaje_objeto.sistema

                tiempo_optimo = ET.SubElement(mensaje, "tiempoOptimo")

                tiempo_optimo.text = str(mensaje_objeto.tiempo_optimo)

                mensajeRecibido = ET.SubElement(mensaje, "mensajeRecibido")
                mensajeRecibido.text = mensaje_objeto.mensaje_decodificado

                instrucciones = ET.SubElement(mensaje, "instrucciones")

                instruccion = instruccion_actual.objeto.instrucciones.inicio
                
                for i in range(1, mensaje_objeto.tiempo_optimo + 1):
                    tiempo = ET.SubElement(instrucciones, "tiempo")
                    tiempo.set("valor", str(i))
                    acciones = ET.SubElement(tiempo, "acciones")

                    instruccion = instruccion_actual.objeto.instrucciones.inicio
                    while instruccion != None:
                        
                        if instruccion.objeto.tiempo == i:
                            accion = ET.SubElement(acciones, "dron")
                            accion.set("nombre", instruccion.objeto.dron.nombre)
                            accion.text = instruccion.objeto.accion

                        instruccion = instruccion.siguiente

                instruccion_actual = instruccion_actual.siguiente

            tree = ET.ElementTree(respuesta)
            xmlstr = ET.tostring(respuesta, encoding="utf-8")
            dom = xml.dom.minidom.parseString(xmlstr)

            with open("respuesta.xml", "wb") as archivo:
                archivo.write(dom.toprettyxml(indent="   ").encode("utf-8"))

            messagebox.showinfo("Información", "Archivo de salida generado exitosamente")


        
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "No se pudo escribir el archivo de salida")
        

#Funcion para actualizar la lista de caracteres y el mensaje decodificado de todos los mensajes. Puesto que se pueden actualizar los sistemas y los drones, se debe actualizar el mensaje decodificado y la lista de caracteres. Esta funcion se llama cada vez que se actualiza un sistema o un dron
def actualizar_mensajes(lista_mensajes):
    try:
        mensaje_actual = lista_mensajes.inicio
        while mensaje_actual != None:
            mensaje_actual.objeto.mensaje_decodificado = ""
            mensaje_actual.objeto.lista_caracteres = ListaDoblementeEnlazada()
            instruccion_actual = mensaje_actual.objeto.lista_instrucciones.inicio
            while instruccion_actual != None:
                letra = obtenerLetra(None, mensaje_actual.objeto.sistemaObjeto, instruccion_actual.objeto.nombreDron, instruccion_actual.objeto.altura)
                mensaje_actual.objeto.lista_caracteres.insertar(letra)
                mensaje_actual.objeto.mensaje_decodificado += letra
                instruccion_actual = instruccion_actual.siguiente
            mensaje_actual = mensaje_actual.siguiente
    except Exception as e:
        print(e)
        messagebox.showerror("Error", "No se pudo actualizar los mensajes")