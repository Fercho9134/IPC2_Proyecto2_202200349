from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Forma import Forma
from FormaConTiempo import FormaConTiempo
from InstruccionesFinales import InstruccionesFinales
from MensajeConInstruccion import MensajeConInstruccion
from Procesar_xml import obtenerLetra
from tkinter import messagebox


import copy

"""def obtenerFormasPosibles(mensaje, forma, dron_actual, altura_actual, caracter_actual, lista_formas_posibles):
    if forma is None:
        forma = ListaDoblementeEnlazada()

    dron_inicio = mensaje.sistemaObjeto.drones.inicio
    altura_inicio = dron_inicio.objeto.lista_alturas.inicio

    if mensaje.lista_caracteres.contar_elementos() == 0:
        # Realizar una copia profunda de 'forma' antes de agregarla a la lista
        forma_copia = copy.deepcopy(forma)
        lista_formas_posibles.insertar(forma_copia)
        return lista_formas_posibles

    while dron_actual is not None:

        while altura_actual is not None:
            if caracter_actual is None:
                break
            caracter = caracter_actual.objeto
            if altura_actual.objeto.letra == caracter:
                forma.insertar(Forma(dron_actual.objeto.dron.nombre, altura_actual.objeto.altura, caracter_actual.objeto))
                obtenerFormasPosibles(mensaje, copy.deepcopy(forma), dron_inicio, altura_inicio, caracter_actual.siguiente, lista_formas_posibles)
                forma.eliminar_ultimo()
            altura_actual = altura_actual.siguiente

        dron_actual = dron_actual.siguiente
        if altura_actual is None and dron_actual is not None:
            altura_actual = dron_actual.objeto.lista_alturas.inicio

    if forma.contar_elementos() == mensaje.lista_caracteres.contar_elementos():
        # Realizar una copia profunda de 'forma' antes de agregarla a la lista
        forma_copia = copy.deepcopy(forma)
        lista_formas_posibles.insertar(forma_copia)

    return lista_formas_posibles

"""

def obtenerTiempoDeCadaForma(lista_formas_posibles, lista_drones):
    primera_forma = lista_formas_posibles.inicio
    lista_tiempos = ListaDoblementeEnlazada()
    
    while primera_forma is not None:
        tiempo = 0
        altura_maxima = 0
        ultimo_dron = None
        seRepite = False
        forma_actual = primera_forma.objeto.inicio
        while forma_actual is not None:
            altura = forma_actual.objeto.altura
            nombre_dron = forma_actual.objeto.nombreDron
            dron_actual = lista_drones.buscar(nombre_dron)

            if ultimo_dron == nombre_dron:
                seRepite = True
            else:
                seRepite = False

            # Para la primera letra siempre va a subir al menos un metro
            if altura_maxima == 0:
                # Tiempo en subir a la altura
                tiempo += altura
                altura_maxima = altura

                dron_actual.altitud = altura
                # Tiempo en emitir la letra
                tiempo += 1
                forma_actual.objeto.tiempo_emision = tiempo
                dron_actual.ultima_emision = tiempo

            else:
                # Casos para los que no se trata del primer caracter
                # Si la altura es menor a la altura máxima hay dos casos:
                # 1. Que el dron no se haya movido, entonces suponemos que en ese tiempo ya se ha movido y solo se emite la letra.
                # 2. El otro caso es que el dron se haya movido, entonces se suma el tiempo que se demora en subir o bajar a la altura y el tiempo que se demora en emitir la letra.
                if altura <= altura_maxima:
                    if dron_actual.altitud == 0:
                        tiempo += 1
                        forma_actual.objeto.tiempo_emision = tiempo
                        dron_actual.ultima_emision = tiempo
                        dron_actual.altitud = altura
                    else:
                        # Tiempo en subir o bajar a la altura
                        tiempo += (abs(dron_actual.altitud - altura)) 
                        dron_actual.altitud = altura
                        # Tiempo en emitir la letra
                        if seRepite:
                            tiempo += 1
                        forma_actual.objeto.tiempo_emision = tiempo
                        dron_actual.ultima_emision = tiempo

                # Si la altura es mayor a la altura máxima entonces el dron se mueve a la altura y se emite la letra, habiendo dos casos:
                # 1. Que el dron no se haya movido, entonces el tiempo será la diferencia entre la altura máxima actual y la altura máxima nueva.
                # 2. El otro caso es que el dron se haya movido, entonces se suma el tiempo que se demora en subir o bajar a la altura y el tiempo que se demora en emitir la letra.
                else:
                    if dron_actual.altitud == 0:
                        tiempo += abs(altura_maxima - altura)
                        altura_maxima = altura
                        dron_actual.altitud = altura
                        if seRepite:
                            tiempo += 1
                        forma_actual.objeto.tiempo_emision = tiempo
                        dron_actual.ultima_emision = tiempo
                    else:
                        tiempo += abs(dron_actual.altitud - altura)
                        altura_maxima = altura
                        dron_actual.altitud = altura
                        tiempo += 1
                        if seRepite:
                            tiempo += 1
                        forma_actual.objeto.tiempo_emision = tiempo
                        dron_actual.ultima_emision = tiempo


            ultimo_dron = nombre_dron
            forma_actual = forma_actual.siguiente
        lista_tiempos.insertar(FormaConTiempo(primera_forma.objeto, tiempo))


        
        # Reiniciar altitud de drones a 0
        dron_actual = lista_drones.inicio
        while dron_actual is not None:
            dron_actual.objeto.altitud = 0
            dron_actual = dron_actual.siguiente

        primera_forma = primera_forma.siguiente
    
    lista_tiempos.ordenarPorTiempoBurbuja()
    tiempo_minimo = lista_tiempos.inicio.objeto

    return tiempo_minimo


def generarInstrucciones(tiempo_minimo, lista_instrucciones, mensaje):
    lista_drones = mensaje.sistemaObjeto.drones
    cantidad_tiempos = tiempo_minimo.tiempo

    listaInstruccionestmp = ListaDoblementeEnlazada()
    forma = tiempo_minimo.forma.inicio

    dron_actual = lista_drones.inicio

    while dron_actual is not None:

        forma_actual = forma
        contador = 0

        #Recorremos la forma del tiempo minimo
        while forma_actual is not None:


            if dron_actual.objeto.dron.nombre == forma_actual.objeto.nombreDron:


                for i in range(1, cantidad_tiempos+1):

                    if dron_actual.objeto.dron.altitud < forma_actual.objeto.altura:
                        listaInstruccionestmp.insertar(InstruccionesFinales(contador+1,dron_actual.objeto.dron, "Subir"))
                        dron_actual.objeto.dron.altitud += 1
                        contador += 1
                    elif dron_actual.objeto.dron.altitud > forma_actual.objeto.altura:
                        listaInstruccionestmp.insertar(InstruccionesFinales(contador+1,dron_actual.objeto.dron, "Bajar"))
                        dron_actual.objeto.dron.altitud -= 1
                        contador += 1
                    elif dron_actual.objeto.dron.altitud == forma_actual.objeto.altura and forma_actual.objeto.tiempo_emision == contador+1:
                        listaInstruccionestmp.insertar(InstruccionesFinales(contador+1,dron_actual.objeto.dron, "Emitir Luz"))
                        contador += 1
                        break
                    elif dron_actual.objeto.dron.altitud == forma_actual.objeto.altura and forma_actual.objeto.tiempo_emision > contador+1:
                        listaInstruccionestmp.insertar(InstruccionesFinales(contador+1,dron_actual.objeto.dron, "Esperar"))
                        contador += 1

            forma_actual = forma_actual.siguiente
        
        if contador < cantidad_tiempos:
            for i in range(contador+1, cantidad_tiempos+1):
                listaInstruccionestmp.insertar(InstruccionesFinales(i,dron_actual.objeto.dron, "Esperar"))
        
        contador = 0
        dron_actual = dron_actual.siguiente

    lista_instrucciones.insertar(MensajeConInstruccion(listaInstruccionestmp, mensaje))
    #Reiniciamos altitud de drones a 0
    dron_actual = lista_drones.inicio
    while dron_actual is not None:
        dron_actual.objeto.dron.altitud = 0
        dron_actual = dron_actual.siguiente
                    

def obtenerTiempoDeCadaForma2(lista_formas_posibles, lista_drones, mensaje):
    primera_forma = lista_formas_posibles.inicio
    lista_tiempos = ListaDoblementeEnlazada()
    cantidad_instrucciones_seguidas = 0
    
    while primera_forma is not None:
        tiempo = 0
        se_emitio = False
        forma_actual = primera_forma.objeto.inicio
        forma_emitida = None

        lista_drones_forma_actual = mensaje.sistemaObjeto.drones

        #Impresion de la forma actual
        print("Forma actual: ")
        forma_actual_aux = primera_forma.objeto.inicio
        while forma_actual_aux is not None:
            print(forma_actual_aux.objeto.nombreDron, forma_actual_aux.objeto.altura, forma_actual_aux.objeto.letra, forma_actual_aux.objeto.numero_de_instruccion)
            print("")
            forma_actual_aux = forma_actual_aux.siguiente

        ###Vamos a ir subiendo, bajando y emitiendo la letra de todos los drones, segundo a segundo
        while cantidad_instrucciones_seguidas != primera_forma.objeto.contar_elementos():
            print("Tiempo: ", tiempo, "Instrucciones ejecutadas", cantidad_instrucciones_seguidas, "de", primera_forma.objeto.contar_elementos())
            forma_actual = primera_forma.objeto.inicio
            if "null" in mensaje.mensaje_decodificado:
                messagebox.showerror("Error", "No se puede decodificar el mensaje, verifique el sistema")
                return None
                

            #por cada segundo, recorremos la forma completa, para ver si hay que subir, bajar o emitir cada uno de los drones
            while forma_actual is not None:

                dron_actual = lista_drones_forma_actual.inicio

                while dron_actual != None:

                    if dron_actual.objeto.dron.nombre == forma_actual.objeto.nombreDron and forma_actual.objeto.usada == False:

                        if dron_actual.objeto.dron.altitud < forma_actual.objeto.altura and forma_actual.objeto.usada == False and forma_actual.objeto.estado == "en curso":
                            dron_actual.objeto.dron.altitud += 1
                            #Cambiamos el estado de todas las demas formas en las que aparece el dron menos la actual, a "en espera"
                            forma_actual_aux = primera_forma.objeto.inicio
                            
                            print("Se subio el dron", dron_actual.objeto.dron.nombre, "a la altura", dron_actual.objeto.dron.altitud)

                            while forma_actual_aux is not None:
                                if forma_actual_aux.objeto.nombreDron == forma_actual.objeto.nombreDron and forma_actual_aux.objeto.numero_de_instruccion != forma_actual.objeto.numero_de_instruccion:
                                    forma_actual_aux.objeto.estado = "en espera"
                                forma_actual_aux = forma_actual_aux.siguiente
                            
                            

                        elif dron_actual.objeto.dron.altitud > forma_actual.objeto.altura and forma_actual.objeto.usada == False and forma_actual.objeto.estado == "en curso":
                            dron_actual.objeto.dron.altitud -= 1
                            #Cambiamos el estado de todas las demas formas en las que aparece el dron menos la actual, a "en espera"
                            forma_actual_aux = primera_forma.objeto.inicio
                            print("Se bajo el dron", dron_actual.objeto.dron.nombre, "a la altura", dron_actual.objeto.dron.altitud)
                            
                            while forma_actual_aux is not None:
                                if forma_actual_aux.objeto.nombreDron == forma_actual.objeto.nombreDron and forma_actual_aux.objeto.numero_de_instruccion != forma_actual.objeto.numero_de_instruccion:
                                    forma_actual_aux.objeto.estado = "en espera"
                                forma_actual_aux = forma_actual_aux.siguiente
                            

                        elif dron_actual.objeto.dron.altitud == forma_actual.objeto.altura and forma_actual.objeto.numero_de_instruccion == cantidad_instrucciones_seguidas+1 and forma_actual.objeto.usada == False and forma_actual.objeto.estado == "en curso":
                            forma_actual.objeto.usada = True

                            forma_actual.objeto.tiempo_emision = tiempo+1
                            #Cambiamos el estado de todas las demas formas en las que aparece el dron menos la actual, a "en curso" la actual la marcamos como "emitida"
                            forma_emitida = forma_actual
                            se_emitio = True	
                            
                            
                        elif dron_actual.objeto.dron.altitud == forma_actual.objeto.altura and forma_actual.objeto.numero_de_instruccion > cantidad_instrucciones_seguidas+1 and forma_actual.objeto.usada == False and forma_actual.objeto.estado == "en curso":
                            print("El dron", dron_actual.objeto.dron.nombre, "espera", "en la altura", dron_actual.objeto.dron.altitud)
                            if dron_actual.objeto.dron.altitud == 5 and dron_actual.objeto.dron.nombre == "Dron03" and forma_actual.objeto.numero_de_instruccion == 8:
                                print("")

                            forma_actual_aux = primera_forma.objeto.inicio
                            while forma_actual_aux is not None:
                                if forma_actual_aux.objeto.nombreDron == forma_actual.objeto.nombreDron and forma_actual_aux.objeto.numero_de_instruccion != forma_actual.objeto.numero_de_instruccion:
                                    forma_actual_aux.objeto.estado = "en espera"
                                forma_actual_aux = forma_actual_aux.siguiente
                        

                    dron_actual = dron_actual.siguiente
                
                forma_actual = forma_actual.siguiente
            tiempo += 1

            if se_emitio == True:

                cantidad_instrucciones_seguidas += 1
                se_emitio = False
                forma_actual_aux = primera_forma.objeto.inicio

                if forma_emitida.objeto.numero_de_instruccion == 4:
                    print("")

                while forma_actual_aux is not None:
                    if forma_actual_aux.objeto.nombreDron == forma_emitida.objeto.nombreDron and forma_actual_aux.objeto.numero_de_instruccion != forma_emitida.objeto.numero_de_instruccion:
                        forma_actual_aux.objeto.estado = "en curso"
                    forma_actual_aux = forma_actual_aux.siguiente

                forma_emitida.objeto.estado = "emitida"
                print("Se emitio la letra", forma_emitida.objeto.letra, "en el tiempo", tiempo-1, "por el dron", forma_emitida.objeto.nombreDron, "en la altura", forma_emitida.objeto.altura)
                forma_emitida = None

        
        lista_tiempos.insertar(FormaConTiempo(primera_forma.objeto, tiempo))
        cantidad_instrucciones_seguidas = 0

        #Reiniciamos altitud de drones a 0
        dron_actual = mensaje.sistemaObjeto.drones.inicio
        while dron_actual is not None:
            dron_actual.objeto.dron.altitud = 0
            dron_actual = dron_actual.siguiente

        #Reiniciamos usada de formas a False
        forma_actual = primera_forma.objeto.inicio
        while forma_actual is not None:
            forma_actual.objeto.usada = False
            forma_actual = forma_actual.siguiente
        
        primera_forma = primera_forma.siguiente

    
    lista_tiempos.ordenarPorTiempoBurbuja()
    tiempo_minimo = lista_tiempos.inicio.objeto

    return tiempo_minimo



    
            



    # la lista contendrá los tiempos de cada dron


        



            
"""
if altura_actual != None:
            if altura_actual.objeto.letra == caracter_actual.objeto:
                forma.insertar(dron_actual.objeto)
                obtenerFormasPosibles(mensaje, forma, dron_actual, altura_actual.siguiente, caracter_actual.siguiente)
                forma.eliminar_ultimo()
        else:
            lista_formas_posibles.insertar(forma)
            return
        
        dron_actual = dron_actual.siguiente
    return
    """


    
    