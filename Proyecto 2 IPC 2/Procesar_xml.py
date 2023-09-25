import xml.etree.ElementTree as ET
from Dron import Dron
from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from SistemaDrones import SistemaDrones
from DronSistema import DronSistema
from Altura import Altura

def procesar_entrada(entrada, lista_drones, lista_sistemas, lista_mensajes):
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

            if lista_drones.buscar(dron.text):
                print(f"> El dron {dron.text} ya existe, se omitirá")
                continue

            dron_nuevo = Dron(dron.text)
            lista_drones.insertar(dron_nuevo)
            print(f"> Se ha agregado el dron {dron.text} a la lista de drones")
    
    for listaSistemas in raiz.findall("listaSistemasDrones"):

        for sistemaDrones in listaSistemas.findall("sistemaDrones"):
            contador_drones = 0
            errores = 0
            
            for alturaMaxima in sistemaDrones.findall("alturaMaxima"):
                altura_maxima = int(alturaMaxima.text)
            
            for cantidadDrones in sistemaDrones.findall("cantidadDrones"):
                cantidad_drones = int(cantidadDrones.text)
        
            sistema_nuevo = SistemaDrones(sistemaDrones.get("nombre"), altura_maxima, cantidad_drones)
            lista_sistemas.insertar(sistema_nuevo)

            for contenido in sistemaDrones.findall("contenido"):
                for dron in contenido.findall("dron"):
                    
                    dron = lista_drones.buscar(dron.text)
                
                #Si el dron no existe, se omite el sistema
                if dron == None:
                    print(f"> El dron {dron.text} no existe, se omitirá el sistema {sistemaDrones.get('nombre')}")
                    errores += 1
                    continue

                contador_drones += 1
                    
                for alturas in contenido.findall("alturas"):

                    contador_alturas = 0

                    for altura in alturas.findall("altura"):

                        letra = altura.text
                        altura = int(altura.get("valor"))

                        dron_sistema_nuevo = DronSistema(dron)
                        sistema_nuevo.drones.insertar(dron_sistema_nuevo)
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
                continue

            if errores != 0:
                print("Elimino")
                lista_sistemas.eliminar(sistema_nuevo.nombre)

    #Se implementara la logica para obtener el mensaje ya decodificado que se desea obtener


                







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




