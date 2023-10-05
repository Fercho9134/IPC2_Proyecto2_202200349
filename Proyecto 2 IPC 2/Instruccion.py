class Instruccion:
    def __init__(self, nombreDron, altura, caracter, numero_de_instruccion):
        self.nombreDron = nombreDron
        self.altura = altura
        self.caracter = caracter
        self.emitida = False
        self.numero_de_instruccion = numero_de_instruccion