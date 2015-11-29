from  appBolsa.logic.Orden import Orden
from appBolsa.utils import singleton
from xml.etree import  ElementTree as ET



@singleton.Singleton
class LibroOrdenes():

    def __init__(self):
        self.ordenes = []
        self.ultimoValorAccionEmpresa = {}

    def cargar(self, pathAchivoAcciones):
        tree = ET.parse(pathAchivoAcciones)
        root = tree.getroot()
        for accion in root.findall('accion'):
            empresa = accion.find('empresa').text
            operacion = accion.find('operacion').text
            precio = int(accion.find('precio').text)
            corredor = accion.find('corredor').text
            cantidad = int(accion.find('cantidad').text)


            # crea una nueva instancia de orden por cada orden encuentra en el xml
            ordenObject = Orden(empresa,operacion,precio,corredor,cantidad)
            self.ordenes.append(ordenObject)
            self.tramitarOrden(ordenObject)

    def tramitarOrden(self,orden):
         #si operaci�n es compra, retorna venta (operador ternario). Condici�n lpogica, 0 o 1
        operacionContraria = ("compra","venta")[orden.operacion=="compra"]

        #Lista por comprensi�n
        #recorrido ordenes, sacando las de la operaci�n contraria, misma empresa
        ordenesProceso = [ordenp for ordenp in self.ordenes
                              if ordenp.operacion == operacionContraria
                              and ordenp.empresa == orden.empresa
                              and (
                                  (ordenp.operacion == "venta" and orden.precio >= ordenp.precio)
                                or
                                  (ordenp.operacion == "compra" and orden.precio <= ordenp.precio)
                              )
                          ]
        print("Orden: ",orden,"------")
        print("Procesar con: ",ordenesProceso,"------")

        for ordenp in ordenesProceso:

          #detectar el precio de la transaccion
            if orden.operacion == "compra":
                valorTransaccion = orden.precio
            if orden.operacion == "venta":
                valorTransaccion = ordenp.precio

            #descontando las cantidades en las ordenes afectadas
            if(ordenp.cantidad >= orden.cantidad):
                ordenp.cantidad -=  orden.cantidad
                orden.cantidad = 0
                self.eliminarOrden(orden)
                if ordenp.cantidad == 0:
                    self.eliminarOrden(ordenp)

                self.registrarUltimoValorAccion(orden.empresa,valorTransaccion)
                self.comunicarCorredor(orden)
                self.comunicarCorredor(ordenp)
                break
            elif(ordenp.cantidad < orden.cantidad):
                orden.cantidad -= ordenp.cantidad
                ordenp.cantidad = 0
                self.eliminarOrden(ordenp)

            self.registrarUltimoValorAccion(orden.empresa,valorTransaccion)
            self.comunicarCorredor(orden)
            self.comunicarCorredor(ordenp)


    def comunicarCorredor(self, orden):
        # todo: se debe comunicar al corredor que ya se cumplio con la orden.
        print("<Comunicar Orden procesada: ", orden, " orden>")

    def eliminarOrden(self, orden):
        print("--------------------------------------------")
        print("Remover: ", orden)
        print(self.ordenes)
        self.ordenes.remove(orden)
        print(self.ordenes)
        print("--------------------------------------------")

    def registrarUltimoValorAccion(self,empresa,valor):
        self.ultimoValorAccionEmpresa[empresa]= valor


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




#for orden in libro.ordenes:
 #   print(orden.empresa + " " + orden.operacion  + " " + orden.precio  + " " + orden.corredor  + " " + orden.cantidad)