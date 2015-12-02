# coding=UTF8
import os
import sys
import argparse

os.chdir('..')
sys.path.append(os.getcwd())

from appBolsa.logic.LibroOrdenes import LibroOrdenes
from appBolsa.logic.Pool import PoolConexiones, corredores
class Bolsa():
    def __init__(self,path='appBolsa\\xmlRepository\\base_bolsa2.xml'):
        self.pathAchivoAcciones = path
        #obtiene la instancia del libro de ordenes
        self.libroOrdenes = LibroOrdenes.Instance()
        #obtiene la instancia del Pool de Conexiones
        self.poolConexiones = PoolConexiones.Instance()

    def cargarLibroOrdenes(self):
        """
        Carga el archivo de xmlRepository con la información base del libro de ordenes
        """
        self.libroOrdenes.cargar(self.pathAchivoAcciones)

    def cargarPool(self):
        self.poolConexiones.start()



#ejecución cuando la bolsa.py es el archivo principal invocado
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some files.',add_help=False)
    parser.add_argument('-f', nargs=1, help='Archivo datos iniciales', metavar='<Archivo Datos Iniciales>', required=True)
    args = parser.parse_args()
    path = args.f[0]

    app = Bolsa(path)
    app.cargarLibroOrdenes()
    app.cargarPool()#server forever

#   print(app.libroOrdenes.ordenes)
#  print(app.libroOrdenes.ultimoValorAccionEmpresa)