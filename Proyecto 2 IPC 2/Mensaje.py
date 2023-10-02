from ListaDoblementeEnlazada import ListaDoblementeEnlazada

class Mensaje:

    def __init__(self, id_mensaje, nombre, sistema, sistemaObjeto):
        self.id_mensaje = id_mensaje
        self.nombre = nombre
        self.mensaje_decodificado = ""
        self.sistema = sistema
        self.lista_caracteres = ListaDoblementeEnlazada()
        self.lista_instrucciones = ListaDoblementeEnlazada()
        self.tiempo_optimo = 0
        self.sistemaObjeto = sistemaObjeto
