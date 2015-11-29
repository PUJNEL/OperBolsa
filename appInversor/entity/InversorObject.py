import os
import sys
import xml.etree.ElementTree as ET
from appInversor.entity.Accion import Accion
from collections import defaultdict


class InversorObject():
    def __init__(self, nombre, puertoCorredor, hostCorredor, pathArchivoAcciones):
        self.efectivo = 0
        self.acciones = []
        self.nombre = nombre
        self.puertoCorredor = puertoCorredor
        self.hostCorredor = hostCorredor
        self.pathArchivoAcciones = pathArchivoAcciones

    def cargarDatos(self, nombre, puertoCorredor, hostCorredor, pathArchivoAcciones):
        self.efectivo = 0
        self.acciones = []
        self.nombre = nombre
        self.puertoCorredor = puertoCorredor
        self.hostCorredor = hostCorredor
        self.pathArchivoAcciones = pathArchivoAcciones

    def cargarXml(self):
        tree = ET.parse(self.pathArchivoAcciones)
        root = tree.getroot()

        efectivoXml = root.find('efectivo')
        accionesXml = root.find('acciones')
        self.efectivo = float(efectivoXml.text)

        accionesLista = []
        for accionXml in accionesXml.findall('accion'):
            print("----------------------------------------")
            print("Empresa  : " + accionXml.find('empresa').text)
            print("Cantidad : " + accionXml.find('cantidad').text)
            empresaXml = accionXml.find('empresa').text
            cantidadXml = int(accionXml.find('cantidad').text)
            tup1 = (str(empresaXml).upper(), int(cantidadXml))
            accionesLista.append(tup1)
        self.validarAcciones(accionesLista)

    def validarAcciones(self, accionesLista):
        d = defaultdict(list)
        for tag, num in accionesLista:
            d[tag].append(num)
        self.sumarAccionesPorEmpresa(d)

    def sumarAccionesPorEmpresa(self, d):
        for empresa, cantidad in d.iteritems():
            accionObject = Accion(empresa, sum(cantidad))
            self.acciones.append(accionObject)

    def compraAcciones(self, empresa, cantidad, valor):
        if self.efectivo <= cantidad * valor:
            print("Efectivo no es suficiente " + str(cantidad * valor))
            return False
        print("Resto Efectivo " + str(cantidad * valor))
        self.efectivo = self.efectivo - (cantidad * valor)

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

    def buscarAccionEmpresa(self, empresa):
        count = 0
        print(empresa)
        for accion in self.acciones:
            print(accion.empresa)
            if accion.empresa == str(empresa).upper():
                print("Elemento : " +  str(count))
                return count
            count += 1
        return -1
