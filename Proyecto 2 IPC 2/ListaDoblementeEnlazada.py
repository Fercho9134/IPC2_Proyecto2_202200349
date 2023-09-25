from Nodo import Nodo

class ListaDoblementeEnlazada:

    def __init__(self):
        self.inicio = None
        self.final = None
        self.cantidad_elementos = 0

    def insertar(self, objeto):
        nuevo_nodo = Nodo(objeto)
        if self.cantidad_elementos == 0:
            self.inicio = nuevo_nodo
            self.final = nuevo_nodo
        else:
            nuevo_nodo.anterior = self.final
            self.final.siguiente = nuevo_nodo
            self.final = nuevo_nodo
        self.cantidad_elementos += 1

    def buscar(self, nombre):
        actual = self.inicio
        while actual:
            if actual.objeto.nombre == nombre:
                return actual.objeto
            actual = actual.siguiente

        return None

    def eliminar(self, nombre):
        
        actual = self.inicio

        while actual:
            if actual.objeto.nombre == nombre:
                if actual.anterior:
                    actual.anterior.siguiente = actual.siguiente
                else:
                    self.inicio = actual.siguiente
                if actual.siguiente:
                    actual.siguiente.anterior = actual.anterior
                else:
                    self.final = actual.anterior
                self.cantidad_elementos -= 1
                return
            actual = actual.siguiente

    def imprimir(self):
        actual = self.inicio
        while actual:
            print(actual.objeto.nombre, end=" <-> ")
            actual = actual.siguiente

    def contar_elementos(self):
        return self.cantidad_elementos