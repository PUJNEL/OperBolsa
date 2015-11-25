from appBolsa.utils import singleton
import xml.etree.ElementTree as ET
from  appBolsa.logic.Orden import Orden

@singleton.Singleton
class LibroOrdenes():

    def __init__(self):
        self.ordenes = []

    def cargar(self, pathAchivoAcciones):
        tree = ET.parse(pathAchivoAcciones)
        root = tree.getroot()
        for accion in root.findall('accion'):
            empresa = accion.find('empresa').text
            operacion = accion.find('operacion').text
            precio = accion.find('precio').text
            corredor = accion.find('corredor').text
            cantidad = accion.find('cantidad').text
            ordenObject = Orden(empresa,operacion,precio,corredor,cantidad)
            self.ordenes.append(ordenObject)
        self.validarOrdenesIniciales()

    def validarOrdenesIniciales(self):
        print('........................')
        print(self.ordenes)
        pass

    def tramitarOrdenVenta(self):
        pass

    def tramitarOrdenCompra(self):
        pass

    def cancelarOrdenes(self):
        pass

    def consultarPreciosAccionesporEmpresa(self, orden):
        pass

    def consultarValorUltimaCompraVenta(self):
        pass

    def notificacionesCorredores(self):
        pass

    def consultarPortafolio(self):
        pass

    def consultarCompraAcciones(self):
        pass

    def consultarVentaAcciones(self):
        pass


libro = LibroOrdenes.Instance()
libro.cargar('..\\xml\\base_bolsa.xml')


#for orden in libro.ordenes:
 #   print(orden.empresa + " " + orden.operacion  + " " + orden.precio  + " " + orden.corredor  + " " + orden.cantidad)