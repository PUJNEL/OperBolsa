import xml.etree.ElementTree as ET
import uuid
from appInversor.entity.Accion import Accion
from appInversor.entity.OrdenInversor import Orden
from collections import defaultdict
from appBolsa.utils import singleton

#Definicion del objeto InversorObject (Singleton)
@singleton.Singleton
class InversorObject():
    #Init con valores vacios
    def __init__(self, nombre="", puertoCorredor=0, hostCorredor="", pathArchivoAcciones="", puertoInversor=0):
        self.efectivo = 0
        self.acciones = []
        self.nombre = nombre
        self.puertoCorredor = puertoCorredor
        self.hostCorredor = hostCorredor
        self.pathArchivoAcciones = pathArchivoAcciones
        self.puertoInversor = puertoInversor
        self.ordenes = []
        self.disponible = 0

    #Carga los datos con los parametros
    def cargarDatos(self, nombre, puertoCorredor, hostCorredor, pathArchivoAcciones, puertoInversor):
        self.efectivo = 0
        self.acciones = []
        self.nombre = nombre[0]
        self.puertoCorredor = puertoCorredor[0]
        self.hostCorredor = hostCorredor[0]
        self.pathArchivoAcciones = pathArchivoAcciones
        self.puertoInversor = puertoInversor
        self.ordenes = []
        self.disponible = 0

    #Carga los valores del XML en el listado Acciones del Objeto InversorObject
    def cargarXml(self):
        tree = ET.parse(self.pathArchivoAcciones)
        root = tree.getroot()

        efectivoXml = root.find('efectivo')
        accionesXml = root.find('acciones')
        self.efectivo = float(efectivoXml.text)
        self.disponible = self.efectivo

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
        if self.disponible <= float(cantidad * valor):
            print("Efectivo no es suficiente " + str(cantidad * valor))
            return -1
        #print("Resto Efectivo " + str(cantidad * valor))
        self.disponible = self.disponible - (cantidad * valor)

    #Realiza la logica de venta de Acciones, Disminuyendo el numero de acciones disponibles
    def ventaAcciones(self, empresa, cantidad, valor):
        indexAccion = self.buscarAccionEmpresa(empresa)
        if indexAccion == -1:
            print("No cuenta con acciones para esta empresa " + empresa)
            return -1
        elif cantidad > self.acciones[indexAccion].cantidad:
            print("Ud no tiene acciones suficientes para vender: Solo tiene " + str(self.acciones[indexAccion].cantidad))
        else:
            print("Restar acciones de la empresa " + empresa)
            self.acciones[indexAccion].cantidad -= cantidad
            print(self.acciones[indexAccion].cantidad)

    #Busca por Empresa y retorna el indice en el cual esta ubicada en la lista Acciones
    def buscarAccionEmpresa(self, empresa):
        count = 0
        for accion in self.acciones:
            if accion.empresa == str(empresa).upper():
                return count
            count += 1
        return -1

    def buscarOrden(self, tipo, empresa, cantidad, valor):
        for orden in self.ordenes:
            if orden.tipo == tipo and orden.cantidad == cantidad and orden.empresa == empresa and orden.valor == valor:
                return orden.id
        return "No encontrado"

    def eliminarOrden(self, idOrden):
        for index, orden in enumerate(self.ordenes):
            if orden.id == idOrden:
                break
        else:
            index = -1
        #print("INDICE : " + str(index))
        if index == -1:
            print("No se encontro el objeto")
        else:
            operacion = self.ordenes[index].tipo
            empresa = self.ordenes[index].empresa
            cantidad = self.ordenes[index].cantidad
            valor = self.ordenes[index].valor
            print(str(self.ordenes[index]))
            if(operacion == "COMPRA"):
                print("ENTRA COMPRA DEVOLVER DISPONIBLE")
                self.disponible = self.disponible + (valor * cantidad)
            if(operacion == "VENTA"):
                accion = Accion(str(empresa), cantidad)
                self.sumarAccion(accion)
            self.ordenes.pop(index)

    def crearOrden(self, id, tipo, empresa, cantidad, valor):
        orden = Orden(id, tipo, empresa,cantidad,valor)
        print("Crea Orden " + str(orden))
        self.ordenes.append(orden)

    def sumarAccion(self, accion):
        self.acciones.append(accion)
        accionesLista = []
        for accionItem in self.acciones:
            tup1 = (str(accionItem.empresa).upper(), int(accionItem.cantidad))
            accionesLista.append(tup1)
        self.acciones = []
        self.validarAcciones(accionesLista)

    def procesoAsincrono(self, mensaje):
        operacion = str(mensaje[0])
        idProc = uuid.UUID(mensaje[1])
        cantidadProc = int(mensaje[2])
        valorProc = int(mensaje[3])
        print("Mensaje Asincrono " + str(mensaje))
        if operacion == "orden_procesada":
            print("INVERSOR : ORDEN PROCESADA")
            for index, orden in enumerate(self.ordenes):
                if orden.id == idProc:
                    break
            else:
                index = -1
            #print("INDICE : " + str(index))
            if index == -1:
                print("No se encontro la Orden a Procesar")
            else:
                operacion = self.ordenes[index].tipo
                empresa = self.ordenes[index].empresa
                cantidad = self.ordenes[index].cantidad
                valor = self.ordenes[index].valor
                print(str(self.ordenes[index]))
                if(operacion == "COMPRA"):
                    print("ENTRA COMPRA DEVOLVER DISPONIBLE")
                    self.efectivo = self.efectivo - (valorProc * cantidadProc)
                    self.disponible = self.efectivo + (valor * cantidad)
                    self.disponible = self.disponible - (valorProc * cantidadProc)
                    self.ordenes[index].cantidad = self.ordenes[index].cantidad - cantidadProc
                    accion = Accion(str(empresa), cantidadProc)
                    self.sumarAccion(accion)
                if(operacion == "VENTA"):
                    self.efectivo = self.efectivo + (valorProc * cantidadProc)
                    self.ordenes[index].cantidad = self.ordenes[index].cantidad - cantidadProc
                self.ordenes.pop(index)
                return 1
            return -1