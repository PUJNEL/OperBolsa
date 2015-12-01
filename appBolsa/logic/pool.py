from appBolsa.utils import singleton
from appBolsa.logic.LibroOrdenes import LibroOrdenes
import threading
import time
import random
import socket

corredores = {}

@singleton.Singleton
class PoolConexiones():
    def __init__(self):
        self.serverBolsa = ServerBolsa()
    def start(self):
        self.serverBolsa.start()


class ServerBolsa(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        self.lock = threading.Lock()
        self.port = 50007
        self.host = ''
    def run(self):
        while True:

            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.host, self.port))
            s.listen(1)
            print("Inicio LaBolsa Server 1.0 - Esperando Corredores en el puerto: ",self.port)
            conn, addr = s.accept()
            wayOne = WayOne(conn,addr,self.lock)
            wayOne.start()

#comunicacion desde el corredor
class WayOne(threading.Thread):

    def __init__(self, conn, addr, lock):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.runState = True
        self.lock = lock
    def run(self):
        portWay2 = int(self.conn.recv(1024).decode())
        nombreCorredor = str(self.conn.recv(1024).decode())
        print ('Conectado con el Corredor: ',nombreCorredor,"[",self.addr,"]")
        global corredores
        corredores[nombreCorredor]={}
        wayTwo = WayTwo(self.conn,self.addr,portWay2,nombreCorredor,self.lock)
        wayTwo.start()
        corredores[nombreCorredor]["wayTwo"]= wayTwo

        while self.runState:
            data = self.conn.recv(1024)
            print(data)
            if not data: break

            #Interpretando comando recibido desde el Corredor
            mensaje = data.decode().split(" ")
            operacion = mensaje[0]
            args = mensaje[1:]

            procesar = process(nombreCorredor,operacion,args,self.conn)
            procesar.exec()

        print ('Desconnected: ', self.addr)
        wayTwo.closeWay2()
        self.conn.close()
        self.runState = False

#comunicacion hacia el corredor
class WayTwo(threading.Thread):
    def __init__(self,conn, addr, portWay2,nombreCorredor, lock):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.portWay2 = portWay2
        self.connWay2 = None
        self.runState = True
        self.lock = lock
        self.corredor = nombreCorredor
    def run(self):
        print(self.conn," ",self.addr," ")
        print("Se establecio segundo canal con ", self.corredor,"[",self.addr[0],":",self.addr[1], "] -----" )
        self.connWay2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connWay2.connect((self.addr[0], self.portWay2))

        while self.runState:
            pass

        self.closeWay2()
    def closeWay2(self):
        self.connWay2.close()
        self.runState = False

    def sendMessage(self, msg):
        if self.runState:
            #self.lock.acquire() #INICIA EL BLOQUEO DE conteo COMO RECURSO COMPARTIDO
            print("Enviando a ",self.addr,">> ")
            try:
                self.connWay2.sendall(str(msg).encode())
                #self.lock.release() #INDICA QUE YA SE TERMINO DE UTILIZAR EL USO DE conteo Y SE LIBERA EL RECUSO
                return True
            except:
                return False
        return False


class process():
    def __init__(self,corredor, operacion,args, conn):
        self.operacion = operacion
        self.args = args
        self.corredor = corredor
        self.librodeOrdenes = LibroOrdenes.Instance()
        self.conn = conn
    def exec(self):
        if(self.operacion == "compra"):
             self.compra()
        elif(self.operacion == "venta"):
             self.venta()
        elif(self.operacion == "nocompra"):
             self.nocompra()
        elif(self.operacion == "noventa"):
             self.noventa()
        elif(self.operacion == "consulta"):
             self.consulta()
        elif(self.operacion == "sumar"):
            self.sumar()
        elif(self.operacion == "restar"):
            self.restar()
        else:
            print(self.operacion, " no es una operacion valida")

    def compra(self):
        global corredores
        corredor    = self.corredor
        operacion   = self.operacion
        empresa     = self.args[0]
        cantidad    = self.args[1]
        precio      = self.args[2]
        orden = self.librodeOrdenes.nuevaOrden(empresa,operacion,precio,corredor,cantidad,corredores)
        self.conn.sendall(str(orden.idOrden).encode())
        self.librodeOrdenes.tramitarOrden(orden,corredores)

    def venta(self):
        global corredores
        corredor    = self.corredor
        operacion   = self.operacion
        empresa     = self.args[0]
        cantidad    = self.args[1]
        precio      = self.args[2]
        orden = self.librodeOrdenes.nuevaOrden(empresa,operacion,precio,corredor,cantidad,corredores)
        self.conn.sendall(str(orden.idOrden).encode())
        self.librodeOrdenes.tramitarOrden(orden,corredores)

    def nocompra(self):
        id_orden     = self.args[0]
        stateCancel = self.librodeOrdenes.cancelarOrdenes(id_orden)
        msg = ""
        if(stateCancel):
            msg="nocompra_exitoso "
        else:
            msg="nocompra_noexistencia "
        print(msg+" "+str(id_orden))
        self.conn.sendall((msg+" "+str(id_orden)).encode())

    def noventa(self):
        id_orden     = self.args[0]
        stateCancel = self.librodeOrdenes.cancelarOrdenes(id_orden)
        msg = ""
        if(stateCancel):
            msg="noventa_exitoso "
        else:
            msg="noventa_noexistencia "
        print(msg+" "+str(id_orden))
        self.conn.sendall((msg+" "+str(id_orden)).encode())

    def consulta(self):
        empresa = self.args[0]
        valor = self.librodeOrdenes.consultarUltimoPrecioAccionPorEmpresa(empresa)
        if  valor == -1:
            print("valor_ultima_accion "+empresa+" no_data")
            self.conn.sendall("valor_ultima_accion "+empresa+" no_data")
        else:
            print("valor_ultima_accion "+empresa+" "+str(valor))
            self.conn.sendall(("valor_ultima_accion "+empresa+" "+str(valor)).encode())

    def sumar(self):
        a = self.args[0]
        b = self.args[1]
        respuesta = int(a)+int(b)
        self.conn.sendall(str(respuesta).encode())

    def restar(self):
        a = self.args[0]
        b = self.args[1]
        respuesta = int(a)-int(b)
        self.conn.sendall(str(respuesta).encode())










# threadLock_libroDeOrdenes = threading.Lock()
#
# class CorredorThread(threading.Thread):
#     def __init__(self,threadID,name,counter,socket):
#         threading.Thread.__init__(self)
#         self.threadID = threadID
#         self.name = name
#         self.counter = counter
#         self.socket = socket
#     def run(self):
#         print("Starting " + self.name)
#         self.consultarCostoAccion("kokorico")
#
#     def consultarCostoAccion(self,empresa):
#
#         # Get lock to synchronize threads
#         threadLock_libroDeOrdenes.acquire()
#         libroOrdenes = LibroOrdenes.Instance()
#         valor = libroOrdenes.consultarUltimoPrecioAccionPorEmpresa(empresa)
#         # Free lock to release next thread
#         threadLock_libroDeOrdenes.release()
#
#         #todo: enviar valor al socket corredor
