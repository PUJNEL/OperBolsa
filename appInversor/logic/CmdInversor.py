import cmd
from appInversor.entity.ClienteServidor import *

#Clase CmdInversor (cmd.Cmd) esto inicia una consola CMD para enviar comandos
class CmdInversor(cmd.Cmd):
    intro = 'Bienvenido a la aplicacion Inversor.   Type help or ? to list commands.\n'
    prompt = '(Inversor) '

    #Definicion de Comando COMPRA
    def do_compra(self, args):
        "Coloca una orden de compra Ej: COMPRA <EMPRESA> <CANTIDAD> <VALOR>"
        parametros = args.split()
        if len(parametros) != 3:
            print("Numero Invalido de Argumentos")
            return
        try:
            empresa = str(parametros[0]).upper()
            cantidad = int(parametros[1])
            valor = int(parametros[2])
        except ValueError:
            print("cantidad y/o valor deben ser numericos")
            return
        datos = []
        datos.append(self.inversor.nombre)
        datos.append("COMPRA")
        datos.append(self.ip)
        datos.append(self.port)
        datos.append(empresa)
        datos.append(cantidad)
        datos.append(valor)
        #Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),str(datos))
        #print(clienteRespuesta)
        self.inversor.compraAcciones(empresa, cantidad, valor)

    #Definicion de Comando VENTA
    def do_venta(self, args):
        "Coloca una orden de venta Ej: VENTA <EMPRESA> <CANTIDAD> <VALOR>"
        parametros = args.split()
        if len(parametros) != 3:
            print("Numero Invalido de Argumentos")
            return
        try:
            empresa = str(parametros[0]).upper()
            cantidad = int(parametros[1])
            valor = int(parametros[2])
        except ValueError:
            print("cantidad y/o valor deben ser numericos")
            return
        datos = []
        datos.append(self.inversor.nombre)
        datos.append("VENTA")
        datos.append(self.ip)
        datos.append(self.port)
        datos.append(empresa)
        datos.append(cantidad)
        datos.append(valor)
        #Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),str(datos))
        #print(clienteRespuesta)
        self.inversor.ventaAcciones(empresa, cantidad, valor)

    #Definicion de Comando NOCOMPRA
    def do_nocompra(self, args):
        "Cancela una orden de Compra Ej: NOCOMPRA <EMPRESA> <CANTIDAD> <VALOR>"
        parametros = args.split()
        if len(parametros) != 3:
            print("Numero Invalido de Argumentos")
            return
        try:
            empresa = parametros[0]
            cantidad = int(parametros[1])
            valor = int(parametros[2])
        except ValueError:
            print("cantidad y/o valor deben ser numericos")
            return
        print("Empresa  : " + str(empresa))
        print("Cantidad : " + str(cantidad))
        print("Valor  : " + str(valor))
        datos = []
        datos.append(self.inversor.nombre)
        datos.append("NOCOMPRA")
        datos.append(self.ip)
        datos.append(self.port)
        datos.append(empresa)
        datos.append(cantidad)
        datos.append(valor)
        #Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),str(datos))
        #print(clienteRespuesta)

    #Definicion de Comando NOVENTA
    def do_noventa(self, args):
        "Cancela una orden de Venta Ej: NOVENTA <EMPRESA> <CANTIDAD> <VALOR>"
        parametros = args.split()
        if len(parametros) != 3:
            print("Numero Invalido de Argumentos")
            return
        try:
            empresa = str(parametros[0]).upper()
            cantidad = int(parametros[1])
            valor = int(parametros[2])
        except ValueError:
            print("cantidad y/o valor deben ser numericos")
            return
        datos = []
        datos.append(self.inversor.nombre)
        datos.append("NOVENTA")
        datos.append(self.ip)
        datos.append(self.port)
        datos.append(empresa)
        datos.append(cantidad)
        datos.append(valor)
        print("Empresa  : " + str(empresa))
        print("Cantidad : " + str(cantidad))
        print("Valor  : " + str(valor))
        #Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),str(datos))
        #print(clienteRespuesta)

    #Definicion de Comando CONSULTA
    def do_consulta(self, args):
        "Consulta el precio de las acciones de la empresa Ej: CONSULTA <EMPRESA>"
        parametros = args.split()
        if len(parametros) != 1:
            print("Numero Invalido de Argumentos")
            return
        empresa = str(parametros[0]).upper()
        for i in self.inversor.acciones:
          if str(i.empresa).upper() == empresa:
            print("Empresa  : " + str(empresa))
            print("Acciones : " + str(i.cantidad))
        datos = []
        datos.append(self.inversor.nombre)
        datos.append("CONSULTA")
        datos.append(self.ip)
        datos.append(self.port)
        datos.append(empresa)
        #Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),str(datos))
        #TODO: Muestra al usuario el valor de la acción

        #print(clienteRespuesta)

    #Definicion de Comando PORTAFOLIO
    def do_portafolio(self, args):
        "Muestra la cantidad de dinero en Efectivo que posee un inversor y l alista de acciones y sus cantidades"
        print("--------------Efectivo--------------")
        print("Efectivo : " + str(self.inversor.efectivo))
        print("--------------Acciones--------------")
        for accion in self.inversor.acciones:
            print("Empresa  : " + accion.empresa + " Cantidad : " + str(accion.cantidad))
        print("------------------------------------")

    #Definicion de Comando QUIT
    def do_quit(self, line):
        "Termina la conexion con el corredor."
        return True

    def precmd(self, line):
        line = line.lower()
        return line

    def cmdloop(self, intro=None):
        return cmd.Cmd.cmdloop(self)
