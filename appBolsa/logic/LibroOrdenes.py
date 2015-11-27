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
         #si operación es compra, retorna venta (operador ternario). Condición lpogica, 0 o 1
        operacionContraria = ("compra","venta")[orden.operacion=="compra"]

        #Lista por comprensión
        #recorrido ordenes, sacando las de la operación contraria, misma empresa
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

            #Calculando el Precio de la transaccion:
            valorTransaccion = 0
            if(orden.operacion == "compra"):
                    valorTransaccion = orden.precio
            elif(orden.operacion == "venta"):
                    if orden.precio <= ordenp.precio:
                        valorTransaccion = ordenp.precio
                    else:
                        print("valor de venta superior al precio, saltar orden")
                        continue

            #descontando las cantidades en las ordenes afectadas
            if(ordenp.cantidad >= orden.cantidad):
                ordenp.cantidad -=  orden.cantidad
                orden.cantidad = 0
                #todo: se debe comunicar al corredor que ya se cumplio con la orden.
                print("<Comunicar Orden procesada: ", orden," orden>")
                self.ordenes.remove(orden)
                break
            elif(ordenp.cantidad < orden.cantidad):
                orden.cantidad -= ordenp.cantidad
                ordenp.cantidad = 0
                #todo: se debe comunicar al corredor que ya se cumplio con la orden.
                print("<Comunicar Orden procesada: ", ordenp," ordenpx>")
                self.ordenes.remove(ordenp)

            #registrar el valor de la acción procesada
            self.ultimoValorAccionEmpresa[orden.empresa] = valorTransaccion

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