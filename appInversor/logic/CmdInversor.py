import cmd
import uuid
from appInversor.entity.ClienteServidor import *

# Clase CmdInversor (cmd.Cmd) esto inicia una consola CMD para enviar comandos
class CmdInversor(cmd.Cmd):
    intro = 'Bienvenido a la aplicacion Inversor.   Type help or ? to list commands.\n'
    prompt = '(Inversor) '

    # Definicion de Comando COMPRA
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
        comando = "compra " + empresa + " " + str(cantidad) + " " + str(valor) + " " + str(self.port)

        if(self.inversor.compraAcciones(empresa, cantidad, valor)== -1):
            return
        # Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),comando)
        print("Respuesta Cliente: " + str(clienteRespuesta))
        if clienteRespuesta == -1:
            return
        # Crea la orden y resta el disponible hasta que se procese la orden
        id = uuid.UUID(clienteRespuesta)
        self.inversor.crearOrden(id, "COMPRA", empresa, cantidad, valor)

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
        comando = "venta " + empresa + " " + str(cantidad) + " " + str(valor) + " " + str(self.port)
        indexAccion = self.inversor.buscarAccionEmpresa(empresa)
        if indexAccion == -1:
            print("No tiene acciones de esta empresa")
            self.do_portafolio()
            return
        # Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),comando)
        print("Respuesta Cliente: " + str(clienteRespuesta))
        if clienteRespuesta == -1:
            return
        # Crea la orden y resta las acciones porque ya entraron en la bolsa
        id = uuid.UUID(clienteRespuesta)
        self.inversor.crearOrden(id, "VENTA", empresa, cantidad, valor)
        self.inversor.ventaAcciones(empresa, cantidad, valor)

    # Definicion de Comando NOCOMPRA
    def do_nocompra(self, args):
        "Cancela una orden de Compra Ej: NOCOMPRA <EMPRESA> <CANTIDAD> <VALOR>"
        parametros = args.split()
        if len(parametros) != 3:
            print("Numero Invalido de Argumentos")
            return
        try:
            empresa = parametros[0].upper()
            cantidad = int(parametros[1])
            valor = int(parametros[2])
        except ValueError:
            print("cantidad y/o valor deben ser numericos")
            return
        id = self.inversor.buscarOrden("COMPRA",empresa,cantidad,valor)
        print(str(id))
        if str(id) == "No encontrado":
            print("La orden no existe por favor ingrese una orden Valida:")
            self.do_ordenes()
            return
        comando = "nocompra " + str(id)
        # Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),comando)
        print("Respuesta Cliente: " + str(clienteRespuesta))
        if clienteRespuesta == -1:
            return
        mensaje = clienteRespuesta.split(" ")
        operacion = mensaje[0]
        idRespuesta = mensaje[1]
        print(mensaje)
        print(str(idRespuesta) + "---" + str(id) )
        if (mensaje[0] == "nocompra_exitoso" and idRespuesta == str(id) ):
            self.inversor.eliminarOrden(id)
            #TODO: Eliminar la orden local
            print("Venta eliminada exitosamente")

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
        id = self.inversor.buscarOrden("VENTA",empresa,cantidad,valor)
        print(str(id))
        if str(id) == "No encontrado":
            print("La orden no existe por favor ingrese una orden Valida:")
            self.do_ordenes()
            return
        comando = "noventa " + str(id)
        # Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),comando)
        print("Respuesta Cliente: " + str(clienteRespuesta))
        if clienteRespuesta == -1:
            return
        mensaje = clienteRespuesta.split(" ")
        operacion = mensaje[0]
        idRespuesta = mensaje[1]
        print(mensaje)
        print(str(idRespuesta) + "---" + str(id) )
        if (mensaje[0] == "noventa_exitoso" and idRespuesta == str(id) ):
            self.inversor.eliminarOrden(id)
            print("Venta eliminada exitosamente")

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
        comando = "consulta " + empresa
        #Hace la peticion al corredor
        clienteRespuesta = client(self.inversor.hostCorredor, int(self.inversor.puertoCorredor),comando)
        mensaje = clienteRespuesta.split(" ")
        respuesta = mensaje[0]
        empresa = mensaje[1]
        valor = mensaje[2]
        print("Valor de la Accion: " + empresa + " " + valor )
        #print(clienteRespuesta)

    #Definicion de Comando PORTAFOLIO
    def do_portafolio(self, args=0):
        "Muestra la cantidad de dinero en Efectivo que posee un inversor y l alista de acciones y sus cantidades"
        print("--------------Efectivo--------------")
        print("Efectivo  : " + str(self.inversor.efectivo))
        print("Disponible: " + str(self.inversor.disponible))
        print("--------------Acciones--------------")
        for accion in self.inversor.acciones:
            print("Empresa   : " + accion.empresa + " Cantidad : " + str(accion.cantidad))
        print("------------------------------------")

    def do_ordenes(self, args=0):
        count = 1
        for orden in self.inversor.ordenes:
            print("Orden No. " + str(count) + " " + str(orden))
            count += 1
    #Definicion de Comando QUIT
    def do_quit(self, line):
        "Termina la conexion con el corredor."
        return True

    def precmd(self, line):
        line = line.lower()
        return line

    def cmdloop(self, intro=None):
        return cmd.Cmd.cmdloop(self)
