import xml.etree.ElementTree as ET
from appInversor.entity.Accion import Accion
from collections import defaultdict
from appBolsa.utils import singleton

#Definicion del objeto InversorObject (Singleton)
@singleton.Singleton
class InversorObject():
    #Init con valores vacios
    def __init__(self, nombre="", puertoCorredor=0, hostCorredor="", pathArchivoAcciones=""):
        self.efectivo = 0
        self.acciones = []
        self.nombre = nombre
        self.puertoCorredor = puertoCorredor
        self.hostCorredor = hostCorredor
        self.pathArchivoAcciones = pathArchivoAcciones

    #Carga los datos con los parametros
    def cargarDatos(self, nombre, puertoCorredor, hostCorredor, pathArchivoAcciones):
        self.efectivo = 0
        self.acciones = []
        self.nombre = nombre[0]
        self.puertoCorredor = puertoCorredor[0]
        self.hostCorredor = hostCorredor[0]
        self.pathArchivoAcciones = pathArchivoAcciones

    #Carga los valores del XML en el listado Acciones del Objeto InversorObject
    def cargarXml(self):
        tree = ET.parse(self.pathArchivoAcciones)
        root = tree.getroot()

        efectivoXml = root.find('efectivo')
        accionesXml = root.find('acciones')
        self.efectivo = float(efectivoXml.text)

        accionesLista = []
        for accionXml in accionesXml.findall('accion'):
            #print("----------------------------------------")
            #print("Empresa  : " + accionXml.find('empresa').text)
            #print("Cantidad : " + accionXml.find('cantidad').text)
            empresaXml = accionXml.find('empresa').text
            cantidadXml = int(accionXml.find('cantidad').text)
            tup1 = (str(empresaXml).upper(), int(cantidadXml))
            accionesLista.append(tup1)
        self.validarAcciones(accionesLista)

    #Valida las acciones para totalizar por empresa
    def validarAcciones(self, accionesLista):
        d = defaultdict(list)
        for tag, num in accionesLista:
            d[tag].append(num)
        self.sumarAccionesPorEmpresa(d)

    #Suma las acciones por empresa y totaliza
    def sumarAccionesPorEmpresa(self, d):
        for empresa, cantidad in d.items():
            accionObject = Accion(empresa, sum(cantidad))
            self.acciones.append(accionObject)

    #Realiza la logica de compra de Acciones, disminuyendo el Efectivo
    def compraAcciones(self, empresa, cantidad, valor):
        if self.efectivo <= float(cantidad * valor):
            print("Efectivo no es suficiente " + str(cantidad * valor))
            return False
        #print("Resto Efectivo " + str(cantidad * valor))
        self.efectivo = self.efectivo - (cantidad * valor)

    #Realiza la logica de venta de Acciones, Disminuyendo el numero de acciones disponibles
    def ventaAcciones(self, empresa, cantidad, valor):
        indexAccion = self.buscarAccionEmpresa(empresa)
        if indexAccion == -1:
            print("No cuenta con acciones para esta empresa " + empresa)
            return False
        elif cantidad > self.acciones[indexAccion].cantidad:
            print("Ud no tiene acciones suficientes para vender: Solo tiene " + str(self.acciones[indexAccion].cantidad))
        else:
            print("Restar acciones de la empresa " + empresa)
            self.acciones[indexAccion].cantidad -= cantidad
            print(self.acciones[indexAccion].cantidad)
        pass

    #Busca por Empresa y retorna el indice en el cual esta ubicada en la lista Acciones
    def buscarAccionEmpresa(self, empresa):
        count = 0
        for accion in self.acciones:
            if accion.empresa == str(empresa).upper():
                return count
            count += 1
        return -1
