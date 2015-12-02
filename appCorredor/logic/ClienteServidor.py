__author__ = 'luu'
import os
import sys
import socket
import threading
import socketserver
import time
import random
import socket
import uuid
import appCorredor.logic.wayOne as WO
import appCorredor.logic.ordenCorredor as ordenCorredor

from appInversor.entity.InversorObject import InversorObject

os.chdir('..')
sys.path.append(os.getcwd())

threadLock_libroDeOrdenes = threading.Lock()


def getInversorByOrdenId(idOrden):
    return ("127.0.0.1",5555)


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print("Entrandp al handle")
        id = uuid.uuid4()
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        mensaje = data.split(" ")
        operacion = mensaje[0]

        print(mensaje)
        response = bytes("Default", 'ascii')
        if operacion == "nocompra":
            idOrden = mensaje[1]
            respuesta = WO.wayOne.nocompra(idOrden)
            response = bytes(str(respuesta), 'ascii')
        if operacion == "noventa":
            idOrden = mensaje[1]
            #print(str(mensaje[0]) + " " +  str(mensaje[1]))
            respuesta = WO.wayOne.noventa(idOrden)
            response = bytes(str(respuesta), 'ascii')
        if operacion == "compra":
            nombre_empresa = mensaje[1]
            cantidad       = mensaje[2]
            valor          = mensaje[3]
            ipClient=self.client_address[0]
            puertoClient = int(mensaje[4])
            idOrden = WO.wayOne.comprar(nombre_empresa,cantidad,valor)

            Orden = ordenCorredor.Orden(idOrden,ipClient,puertoClient)
            ordenCorredor.ordenes.append(Orden)

            response = bytes(str(idOrden), 'ascii')
        if operacion == "venta":
            nombre_empresa = mensaje[1]
            cantidad       = mensaje[2]
            valor          = mensaje[3]
            ipClient=self.client_address[0]
            puertoClient = int(mensaje[4])
            idOrden = WO.wayOne.vender(nombre_empresa,cantidad,valor)

            Orden = ordenCorredor.Orden(idOrden,ipClient,puertoClient)
            ordenCorredor.ordenes.append(Orden)
            print("VENTA IDORDEN " + str(idOrden))
            response = bytes(str(idOrden), 'ascii')
        if operacion == "consulta":
            empresa = mensaje[1]
            respuesta = WO.wayOne.consultar(empresa)
            response = bytes(str(respuesta), 'ascii')

        if( operacion == "orden_procesada"):
            idOrden     = mensaje[1]
            cantidad    = mensaje[2]
            valor       = mensaje[3]


            print(ordenCorredor.ordenes)
            ordenes = [orden for orden in ordenCorredor.ordenes if orden.idOrden == idOrden ]
            print(ordenes," ",idOrden)
            if(len(ordenes) > 0):
                orden = ordenes[0]


                inversorIP      = orden.ip
                InversorPuerto  = orden.port

                clientInversor(inversorIP,InversorPuerto,data)
                #print("Enviando Asincrono: ["+data+">]")

            else:
                print("<Orden no encontrada: ",idOrden,">")

        #if operacion != "orden_procesada":
        self.request.sendall(response)


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def clientInversor(ip, port, message):
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







