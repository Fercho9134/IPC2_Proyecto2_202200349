from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Forma import Forma
from FormaConTiempo import FormaConTiempo
from InstruccionesFinales import InstruccionesFinales
from MensajeConInstruccion import MensajeConInstruccion
from Procesar_xml import obtenerLetra


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


    
    