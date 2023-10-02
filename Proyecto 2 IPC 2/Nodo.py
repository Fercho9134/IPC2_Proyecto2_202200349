class Nodo:
    def __init__(self, objeto):
        self.id_nodo = id(self)
        self.objeto = objeto
        self.siguiente = None
        self.anterior = None