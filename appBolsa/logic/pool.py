from appBolsa.utils import singleton


@singleton.Singleton
class PoolConexiones():


    def start(self):
        self.conexiones = []
