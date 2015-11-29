import os
import sys
import argparse

os.chdir('..')
sys.path.append(os.getcwd())
from appInversor.logic.CmdInversor import CmdInversor


def main():
    print(str(sys.argv))
    parser = argparse.ArgumentParser(description='Process some files.',add_help=False)
    parser.add_argument('-n', nargs=1, help='Nombre del Inversor', metavar='<Nombre Inversor>', required=True)
    parser.add_argument('-p', nargs=1, help='Puerto local del corredor', metavar='<Puerto Corredor>', required=True)
    parser.add_argument('-h', nargs=1, help='Host Corredor', metavar='<Host Corredor>', required=True)
    parser.add_argument('-a', nargs=1, help='Archivo datos iniciales', metavar='<Archivo Datos Iniciales>', required=True)
    parser.add_argument("-?", action="help", help="show this help message and exit")
    args = parser.parse_args()
    inversorObject = CmdInversor()
    inversorObject.cargarDatos(args.n, args.p, args.h, args.a[0])
    inversorObject.cargarXml()
    inversorObject.cmdloop()

if __name__ == '__main__':
    main()