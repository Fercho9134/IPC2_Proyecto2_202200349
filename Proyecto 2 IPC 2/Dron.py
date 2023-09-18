class Dron:
    def __init__(self, nombre):
        self.nombre = nombre
        self.altitud = 0
        self.luz = False

    
    def subir(self):
        self.altitud += 1
    
    def bajar(self):
        if self.altitud > 0:
            self.altitud -= 1
        else:
            print("El dron no puede bajar más")
    
    def encender_apagar_luz(self):
        self.luz = not self.luz
    
    def esperar(self):
        pass