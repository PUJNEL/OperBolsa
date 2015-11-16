import uuid
class Orden():
    def __init__(self, empresa, operacion, precio, corredor, cantidad):
        self.idOrden = uuid.uuid4()
        self.empresa = empresa
        self.operacion = operacion
        self.precio = precio
        self.corredor = corredor
        self.cantidad = cantidad