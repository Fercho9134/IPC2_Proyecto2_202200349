from ListaDoblementeEnlazada import ListaDoblementeEnlazada
from Dron import Dron

class SistemaDrones:
    def __init__(self, nombre, altura_maxima, cantidad_drones):
        self.nombre = nombre
        self.altura_maxima = altura_maxima
        self.cantidad_drones = cantidad_drones
        self.drones = ListaDoblementeEnlazada()
    
    def agregar_dron(self, dron):
        
        if self.drones.contar_elementos() < self.cantidad_drones:
            self.drones.agregar_al_final(dron)
        else:
            print("No se pueden agregar más drones")

    def eliminar_dron(self, nombre):
        self.drones.eliminar(Dron(nombre))