import os
import sys
import socket
import threading
import socketserver

from appInversor.entity.InversorObject import InversorObject

os.chdir('..')
sys.path.append(os.getcwd())

threadLock_libroDeOrdenes = threading.Lock()

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        response = bytes("{}: {}".format(cur_thread.name, data), 'ascii')
        mensaje = data.split(" ")
        self.request.sendall(response)
        threadLock_libroDeOrdenes.acquire()
        inversor = InversorObject.Instance()
        inversor.procesoAsincrono(mensaje)
        threadLock_libroDeOrdenes.release()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    # print(ip + " " + str(port) + " " + message)
    response = -1
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        #print(str(response))
    except ConnectionRefusedError:
        print("No se puede conectar con el cliente, Por favor inicielo o verifique los parametros de conexion...")
        return -1
    finally:
        sock.close()
        return response