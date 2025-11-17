class Forma:
    def __init__(self, nombreDron, altura, letra, numero_de_instruccion, usada = False, estado = "en curso"):
        self.nombreDron = nombreDron
        self.altura = altura
        self.letra = letra
        self.tiempo_emision = 0
        self.usada = usada
        self.numero_de_instruccion = numero_de_instruccion
        self.estado = estado
        