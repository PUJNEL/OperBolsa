import ipaddress
import os
import sys
import argparse
#Carga de los import para que se puedan ejecutar desde linea de Comandos
os.chdir('..')
sys.path.append(os.getcwd())
from appInversor.logic.CmdInversor import CmdInversor
from appInversor.entity.ClienteServidor import *
from appInversor.entity.InversorObject import InversorObject

#Main del programa
def main():
    #Obtener la ip Local
    #s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.connect(("google.com",80))
    #ipLocal = s.getsockname()[0]
    #s.close()
    #Se obtienen los parametros del programa
    parser = argparse.ArgumentParser(description='Process some files.',add_help=False)
    parser.add_argument('-n', nargs=1, help='Nombre del Inversor', metavar='<Nombre Inversor>', required=True)
    parser.add_argument('-p', nargs=1, help='Puerto local del corredor', metavar='<Puerto Corredor>', required=True)
    parser.add_argument('-h', nargs=1, help='Host Corredor', metavar='<Host Corredor>', required=True)
    parser.add_argument('-a', nargs=1, help='Archivo datos iniciales', metavar='<Archivo Datos Iniciales>', required=True)
    parser.add_argument('-l', nargs=1, help='Puerto local del inversor', metavar='<Puerto Inversor>', required=True)
    parser.add_argument("-?", action="help", help="show this help message and exit")
    args = parser.parse_args()
    #Inicia el Servidor para escuchar siempre
    print(args)
    HOST, PORT = "localhost", int(args.l[0])
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    #Inicia la consola del sistema para recibir los comandos e instancia el InversorObject (Singleton)
    inversorObject = CmdInversor()
    inversorObject.ip = HOST
    inversorObject.port = port
    inversorObject.inversor = InversorObject.Instance()
    #Carga los datos de los parametros en el inversor
    inversorObject.inversor.cargarDatos(args.n, args.p, args.h, args.a[0], args.l)
    #Carga el XML
    inversorObject.inversor.cargarXml()
    #Inicia el CMDloop
    inversorObject.cmdloop()

if __name__ == '__main__':
    main()