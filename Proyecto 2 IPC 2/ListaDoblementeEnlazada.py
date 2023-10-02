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
    
    def buscar_dron_sistema(self, nombre):
        actual = self.inicio
        while actual:
            if actual.objeto.dron.nombre == nombre:
                return actual.objeto
            actual = actual.siguiente

        return None
    
    def buscar_dron_sistema_altura(self, nombre, altura):
        actual = self.inicio
        while actual:
            if actual.objeto.dron.nombre == nombre:
                return actual.objeto.lista_alturas.buscar_altura(altura)
            actual = actual.siguiente

        return None
    
    def buscar_altura(self, altura):
        actual = self.inicio
        while actual:
            if actual.objeto.altura == altura:
                #devuelve el objeto altura
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
    
    def eliminar_ultimo(self):
        if self.cantidad_elementos == 0:
            return
        if self.cantidad_elementos == 1:
            self.inicio = None
            self.final = None
            self.cantidad_elementos = 0
            return
        self.final = self.final.anterior
        self.final.siguiente = None
        self.cantidad_elementos -= 1

    def ordenarPorTiempoBurbuja(self):
        actual = self.inicio
        while actual:
            siguiente = actual.siguiente
            while siguiente:
                if actual.objeto.tiempo > siguiente.objeto.tiempo:
                    temporal = actual.objeto
                    actual.objeto = siguiente.objeto
                    siguiente.objeto = temporal
                siguiente = siguiente.siguiente
            actual = actual.siguiente

            
        