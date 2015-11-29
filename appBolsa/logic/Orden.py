import uuid
class Orden():
    def __init__(self, empresa, operacion, precio, corredor, cantidad,):
        self.idOrden = uuid.uuid4()
        self.empresa = empresa
        self.operacion = operacion
        self.precio = precio
        self.corredor = corredor
        self.cantidad = cantidad


    def getCantidad(self):
        return self.cantidad

    def __str__(self):
        #representación del objero orden
        registroorden = "ORDEN: ["+str(self.operacion)+" ("+str(self.empresa)+"){"+str(self.cantidad)+" * $"+str(self.precio)+"} ("+str(self.corredor)+")] "
        return registroorden

    def __unicode__(self):
        return self.__str__().encode()

    def __repr__(self):
        return self.__str__()
