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
        self.request.sendall(response)
        threadLock_libroDeOrdenes.acquire()
        inversor = InversorObject.Instance()
        #TODO: Logica para poder realizar acciones sobre el InversorObject
        #TODO: COMPRA Realizad Exitosamente
        #TODO: VENTA Realizada Exitosamente

        threadLock_libroDeOrdenes.release()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    print(ip + " " + str(port) + " " + message)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
    finally:
        sock.close()
        return "OK"