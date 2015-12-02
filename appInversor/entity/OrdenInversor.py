class Orden():
    def __init__(self, id, tipo, empresa, cantidad, valor):
        self.id = id
        self.tipo = tipo
        self.empresa = empresa
        self.cantidad = cantidad
        self.valor = valor

    def __str__(self):
        return str(self.id) + " " + self.tipo + " " + self.empresa + " " + str(self.cantidad) + " " + str(self.valor)
