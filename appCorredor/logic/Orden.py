import uuid
class Orden():
    def __init__(self, empresa, operacion, precio, inversor, cantidad,):
        self.idOrden = None #Todo: Asignar el UUID generado por la Bolsa
        self.empresa = empresa
        self.operacion = operacion
        self.precio = int(precio)
        self.inversor = inversor
        self.cantidad = int(cantidad)

    def getCantidad(self):
        return self.cantidad

    def __str__(self):
        #representación del objero orden
        registroorden = "ORDEN: ["+str(self.operacion)+" ("+str(self.empresa)+"){"+str(self.cantidad)+" * $"+str(self.precio)+"} ("+str(self.inversor)+")] "
        return registroorden

    def __unicode__(self):
        return self.__str__().encode()

    def __repr__(self):
        return self.__str__()
