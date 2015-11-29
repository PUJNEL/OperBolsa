from appBolsa.utils import singleton
from appBolsa.logic.LibroOrdenes import LibroOrdenes
import threading

@singleton.Singleton
class PoolConexiones():
    def __init__(self):
        self.conexiones = []



threadLock_libroDeOrdenes = threading.Lock()

class CorredorThread(threading.Thread):
    def __init__(self,threadID,name,counter,socket):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.socket = socket
    def run(self):
        print("Starting " + self.name)
        self.consultarCostoAccion("kokorico")

    def consultarCostoAccion(self,empresa):

        # Get lock to synchronize threads
        threadLock_libroDeOrdenes.acquire()
        libroOrdenes = LibroOrdenes.Instance()
        valor = libroOrdenes.consultarUltimoPrecioAccionPorEmpresa(empresa)
        # Free lock to release next thread
        threadLock_libroDeOrdenes.release()

        #todo: enviar valor al socket corredor
