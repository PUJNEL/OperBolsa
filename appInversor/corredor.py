import socket
import threading
import socketserver
import uuid


class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        id = uuid.uuid4()
        data = str(self.request.recv(1024), 'ascii')
        cur_thread = threading.current_thread()
        mensaje = data.split(" ")
        operacion = mensaje[0]
        print(mensaje)
        response = bytes("Default", 'ascii')
        if operacion == "nocompra":
            #print(str(mensaje[0]) + " " +  str(mensaje[1]))
            respuesta = "nocompra_exitoso " + str(mensaje[1])
            response = bytes(str(respuesta), 'ascii')
        if operacion == "noventa":
            #print(str(mensaje[0]) + " " +  str(mensaje[1]))
            respuesta = "noventa_exitoso " + str(mensaje[1])
            response = bytes(str(respuesta), 'ascii')
        if operacion == "compra":
            response = bytes(str(id), 'ascii')
        if operacion == "venta":
            response = bytes(str(id), 'ascii')
        self.request.sendall(response)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))
    finally:
        sock.close()

