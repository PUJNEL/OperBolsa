# coding=UTF8

from appBolsa.logic.LibroOrdenes import LibroOrdenes
from appBolsa.logic.Pool import PoolConexiones
class Bolsa():
    def __init__(self):
        self.pathAchivoAcciones = 'xmlRepository\\base_bolsa2.xml'
        #obtiene la instancia del libro de ordenes
        self.libroOrdenes = LibroOrdenes.Instance()
        #obtiene la instancia del Pool de Conexiones
        self.poolConexiones = PoolConexiones.Instance()
    def cargarPool(self):
        self.poolConexiones.start()
    def cargarLibroOrdenes(self):
        """
        Carga el archivo de xmlRepository con la información base del libro de ordenes
        """
        self.libroOrdenes.cargar(self.pathAchivoAcciones)


#ejecución cuando la bolsa.py es el archivo principal invocado
if __name__ == "__main__":
    app = Bolsa()
    app.cargarLibroOrdenes()
    print(app.libroOrdenes.ordenes)
    print(app.libroOrdenes.ultimoValorAccionEmpresa)