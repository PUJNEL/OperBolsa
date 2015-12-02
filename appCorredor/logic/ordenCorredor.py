ordenes = []
class Orden():
    def __init__(self,idOrden, ip, port):
        self.idOrden = idOrden
        self.ip = ip
        self.port = port
    def __str__(self):
        return "[<"+str(self.idOrden)+"> "+self.ip+":"+str(self.port)+" ]"
    def __repr__(self):
        return "[<"+str(self.idOrden)+"> "+self.ip+":"+str(self.port)+" ]"