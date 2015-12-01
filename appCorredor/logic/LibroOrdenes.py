from  appCorredor.logic.Orden import Orden
from appBolsa.utils import singleton
from xml.etree import  ElementTree as ET



@singleton.Singleton
class LibroOrdenes():

    def __init__(self):
        self.ordenes = []
        self.ultimoValorAccionEmpresa = {}

    def nuevaOrden(self,empresa,operacion,precio,inversor,cantidad,corredores):
        print("Creando orden de "+operacion+" para "+empresa+" >> Inversor: ["+inversor+"]")
        orden = Orden(empresa,operacion,precio,inversor,cantidad)
        self.ordenes.append(orden)
        print("Se creo la orden: "+str(orden.idOrden))
        return orden

    def tramitarOrden(self,orden,corredores=None):
        #todo: enviar orden a la Bolsa
        pass

    def comunicarInversor(self, orden, wayTwoInversor=None):
        # todo: se debe comunicar al inversor que ya se cumplio con la orden.
        # todo: way 2
        if wayTwoInversor is not None:
            wayTwoInversor["wayTwo"].sendMessage("orden_procesada "+str(orden.idOrden)+" ")
            print("<Comunicar Orden procesada: ", orden, " orden>")
        else:
            print("<Comunicar Orden procesada: ", orden, " orden sin coneccion con inversor>")

    def eliminarOrden(self, orden):
        print("--------------------------------------------")
        print("Remover: ", orden)
        #todo: notificar a la bolsa de la Eliminacion de la orden
        #todo: cuando la bolsa elimine se debe notificar al inversor y eliminar en local
        print("--------------------------------------------")

    def cancelarOrdenes(self,id_orden):
        #todo: Realizar la consulta a la bolsa y entre gar el valor
        pass

    def consultarUltimoPrecioAccionPorEmpresa(self, empresa):
        #todo: Realizar la consulta a la bolsa y entre gar el valor
        pass






