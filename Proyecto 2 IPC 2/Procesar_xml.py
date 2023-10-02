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

contador_mensaje = 1

def procesar_entrada(entrada, lista_drones, lista_sistemas, lista_mensajes):
    global contador_mensaje
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
            print("Se ha agregado el dron", dron.text, "a la lista de drones")
            print(f"> Se ha agregado el dron {dron.text} a la lista de drones")
    

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
                lista_sistemas.eliminar(sistema_nuevo.nombre)

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

                for instruccion in instrucciones.findall("instruccion"):
                    nombre_dron = instruccion.get("dron")
                    altura = int(instruccion.text)
                    instruccion_nueva = Instruccion(nombre_dron, altura)
                    letra = obtenerLetra(lista_sistemas, nombre_sistema, nombre_dron, altura)
                    mensaje_nuevo.lista_caracteres.insertar(letra)
                    mensaje_nuevo.mensaje_decodificado += letra
                    mensaje_nuevo.lista_instrucciones.insertar(instruccion_nueva)

    print("Se ha procesado la entrada correctamente")
                    


def obtenerLetra(lista_sistemas, sistema, dron, altura):
    #Se obtiene la letra de la altura del dron en el sistema
    if lista_sistemas == None:
        sistema_actual = sistema
    else:
        sistema_actual = lista_sistemas.buscar(sistema)
        
    altura = sistema_actual.drones.buscar_dron_sistema_altura(dron, altura)
    letra = altura.letra
    return letra

def obtenerDronesOrdenadosAlfabeticamente(lista_drones):
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

def obtenerMensajesOrdenadosAlfabeticamente(lista_mensajes):
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

def graficarSistemas(lista_sistemas):
    # Inicializar el grafo con el nombre Sistemas de drones
    grafo = graphviz.Digraph('Sistemas de drones', filename='Sistemas de drones.gv', format='png')
    
    sistema_actual = lista_sistemas.inicio

    while sistema_actual != None:
        # Agregar el nodo del sistema
        grafo.node(str(sistema_actual.id_nodo), str(sistema_actual.objeto.nombre))

        #Agregamos titulos a las filas
        grafo.node(str(sistema_actual.id_nodo) + "alt", "Altura\n(mts)")
        grafo.edge(str(sistema_actual.id_nodo), str(sistema_actual.id_nodo) + "alt")

        primeraFilaAlturas = True

        for i in range(1, sistema_actual.objeto.altura_maxima + 1):
            # Agregar el nodo de la altura
            grafo.node(str(sistema_actual.id_nodo) + str(i), str(i))
            
            if primeraFilaAlturas:
                grafo.edge(str(sistema_actual.id_nodo) + "alt", str(sistema_actual.id_nodo) + str(i))
                primeraFilaAlturas = False
            else:
                grafo.edge(str(sistema_actual.id_nodo) + str(i-1), str(sistema_actual.id_nodo) + str(i))
        
        # Agregar el nodo de los drones
        dron_actual = sistema_actual.objeto.drones.inicio

        while dron_actual != None:
            primerFilaDrones = True
            grafo.node(str(dron_actual.id_nodo), str(dron_actual.objeto.dron.nombre))
            grafo.edge(str(sistema_actual.id_nodo), str(dron_actual.id_nodo))
            #Agregamos letras del dron segun su altura
            altura_actual = dron_actual.objeto.lista_alturas.inicio

            while altura_actual != None:
                grafo.node(str(altura_actual.id_nodo), str(altura_actual.objeto.letra))
                if primerFilaDrones:
                    grafo.edge(str(dron_actual.id_nodo), str(altura_actual.id_nodo))
                    primerFilaDrones = False
                else:
                    grafo.edge(str(altura_actual.anterior.id_nodo), str(altura_actual.id_nodo))

                altura_actual = altura_actual.siguiente
            
            dron_actual = dron_actual.siguiente

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




