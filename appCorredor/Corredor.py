import os
import sys
import argparse
#Carga de los import para que se puedan ejecutar desde linea de Comandos
os.chdir('..')
sys.path.append(os.getcwd())
from appCorredor.logic.ClienteServidor import *
import appCorredor.logic.wayOne as WO

class Corredor():
    def __init__(self):
        pass

    def start(self):
        parser = argparse.ArgumentParser(description='Process some files.',add_help=False)
        parser.add_argument('-n', nargs=1, help='Nombre del Corredor', metavar='<Nombre Corredor>', required=True)
        parser.add_argument('-p', nargs=1, help='Puerto Labolsa', metavar='<Puerto Labolsa>', required=True)
        parser.add_argument('-h', nargs=1, help='Host Labolsa', metavar='<Host Labolsa>', required=True)
        parser.add_argument('-l', nargs=1, help='Puerto local del corredor', metavar='<Puerto Corredor>', required=True)
        parser.add_argument("-?", action="help", help="show this help message and exit")
        args = parser.parse_args()
        print(args)

        hostBolsa       = args.h[0]
        portBolsa       = args.p[0]
        portWay2        = args.l[0]
        nombreCorredor  = args.n[0]


        WO.wayOne          = WO.WayOne(hostBolsa,portBolsa,portWay2,nombreCorredor)
        #crear el server canal 2
        HOST, PORT = "", int(args.l[0])
        server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()
        WO.wayOne.start()

        (args.h[0], int(args.p[0]), "")
        while True: pass


if __name__ == "__main__":
    corredor = Corredor()
    corredor.start()