import threading
import socket
wayOne = None

class WayOne(threading.Thread):
    def __init__(self,hostBolsa,portBolsa, portWay2, nombreCorredor):
        threading.Thread.__init__(self)
        self.runState = True
        self.portWay2 = portWay2
        self.nombreCorredor = nombreCorredor
        self.hostBolsa = hostBolsa
        self.portBolsa = portBolsa
        self.conn = None

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.hostBolsa, int(self.portBolsa)))
        s.sendall(str(self.portWay2).encode())
        s.sendall(str(self.nombreCorredor).encode())
        self.conn = s
        while self.runState: pass

    def comprar(self,nombre_empresa,cantidad,valor):
        comand = "compra "+nombre_empresa+" "+cantidad+" "+valor
        print(comand)
        self.conn.sendall(comand.encode())
        data = self.conn.recv(1024)
        return data.decode()
    def vender(self,nombre_empresa,cantidad,valor):
        comand = "venta "+nombre_empresa+" "+cantidad+" "+valor
        print(comand)
        self.conn.sendall(comand.encode())
        data = self.conn.recv(1024)
        return data.decode()
    def nocompra(self,id_orden):
        comand = "nocompra "+id_orden
        print(comand)
        self.conn.sendall(comand.encode())
        data = self.conn.recv(1024)
        return data.decode()
    def noventa(self,id_orden):
        comand = "noventa "+id_orden
        print(comand)
        self.conn.sendall(comand.encode())
        data = self.conn.recv(1024)
        return data.decode()
    def consultar(self,nombre_empresa):
        comand = "consulta "+nombre_empresa
        print(comand)
        self.conn.sendall(comand.encode())
        data = self.conn.recv(1024)
        return data.decode()

    def closeSock(self):
        self.conn.close()
        self.runState = False
