import socket
from  appBolsa.logic.Orden import Orden
from appBolsa.utils import singleton
from xml.etree import  ElementTree as ET
import time


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
    def nuevaOrden(self,empresa,operacion,precio,corredor,cantidad,corredores):
        print("Creando orden de "+operacion+" para "+empresa+" >> Corredor: ["+corredor+"]")
        orden = Orden(empresa,operacion,precio,corredor,cantidad)
        self.ordenes.append(orden)
        print("Se creo la orden: "+str(orden.idOrden))
        return orden

    def tramitarOrden(self,orden,corredores=None):
         #si operación es compra, retorna venta (operador ternario). Condición logica, 0 o 1
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
        print("Libro: ",self.ordenes,"------")

        for ordenp in ordenesProceso:
            cantidad = 0

          #detectar el precio de la transaccion
            if orden.operacion == "compra":
                valorTransaccion = orden.precio
            if orden.operacion == "venta":
                valorTransaccion = ordenp.precio

            #descontando las cantidades en las ordenes afectadas
            if(ordenp.cantidad >= orden.cantidad):
                ordenp.cantidad -=  orden.cantidad
                cantidad = orden.cantidad
                orden.cantidad = 0

                self.eliminarOrden(orden)
                if ordenp.cantidad == 0:
                    self.eliminarOrden(ordenp)

                self.registrarUltimoValorAccion(orden.empresa,valorTransaccion)

                if corredores is not None and orden.corredor in list(corredores.keys()):
                    self.comunicarCorredor(orden,cantidad,valorTransaccion,corredores[orden.corredor])
                    time.sleep(2)
                if corredores is not None and ordenp.corredor in list(corredores.keys()):
                    self.comunicarCorredor(ordenp,cantidad,valorTransaccion,corredores[ordenp.corredor])
                    time.sleep(2)
                break
            elif(ordenp.cantidad < orden.cantidad):
                orden.cantidad -= ordenp.cantidad
                cantidad = ordenp.cantidad
                ordenp.cantidad = 0
                self.eliminarOrden(ordenp)

            self.registrarUltimoValorAccion(orden.empresa,valorTransaccion)


            if corredores is not None and orden.corredor in list(corredores.keys()):
                    self.comunicarCorredor(orden,cantidad,valorTransaccion,corredores[orden.corredor])
                    time.sleep(2)
            if corredores is not None and ordenp.corredor in list(corredores.keys()):
                    self.comunicarCorredor(ordenp,cantidad,valorTransaccion,corredores[ordenp.corredor])
                    time.sleep(2)

    def comunicarCorredor(self, orden,cantidad,valor, wayTwoCorredor=None):
        # se debe comunicar al corredor que ya se cumplio con la orden.
        # way 2
        # orden_procesada id_orden cantidad valor
        if wayTwoCorredor is not None:
            #wayTwoCorredor["wayTwo"].sendMessage("orden_procesada "+str(orden.idOrden)+" "+str(cantidad)+" "+str(valor))

            ip = wayTwoCorredor["wayTwo"].addr[0]
            puerto = wayTwoCorredor["wayTwo"].portWay2

            clientCorredor(ip,puerto,str("orden_procesada "+str(orden.idOrden)+" "+str(cantidad)+" "+str(valor)))

            print("<Comunicar Orden procesada: ", orden, " orden>")
        else:
            print("<Comunicar Orden procesada: ", orden, " orden sin coneccion con corredor>")

    def eliminarOrden(self, orden):
        print("--------------------------------------------")
        print("Remover: ", orden)
        print(self.ordenes)
        self.ordenes.remove(orden)
        print(self.ordenes)
        print("--------------------------------------------")

    def registrarUltimoValorAccion(self,empresa,valor):
        self.ultimoValorAccionEmpresa[empresa]= valor


    def consultarUltimoPrecioAccionPorEmpresa(self, empresa):
        try:
            return self.ultimoValorAccionEmpresa[empresa]
        except:
            return -1

    def cancelarOrdenes(self,id_orden):
        print("Eliminando Orden: ",id_orden)
        for orden in self.ordenes:
            if(str(orden.idOrden) == id_orden):
                try:
                    self.ordenes.remove(orden)
                except:
                    print("Orden no se puede eliminar: ",id_orden)
                    return False
                del(orden)
                print("Orden Eliminada: ",id_orden)
                return True
        print("Orden no encontrada: ",id_orden)
        return False


    def tramitarOrdenVenta(self):
        pass

    def notificacionesCorredores(self):
        pass

    def consultarPortafolio(self):
        pass

def clientCorredor(ip, port, message):
    # print(ip + " " + str(port) + " " + message)
    response = -1
    try:
        print("Enviando Asincrono: ["+str(ip)+":"+str(port)+" <"+str(message)+">]")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print(str(response))
    except ConnectionRefusedError:
        print("No se puede conectar con el cliente, Por favor inicielo o verifique los parametros de conexion...")
        return -1
    finally:
        sock.close()
        return response





#for orden in libro.ordenes:
 #   print(orden.empresa + " " + orden.operacion  + " " + orden.precio  + " " + orden.corredor  + " " + orden.cantidad)