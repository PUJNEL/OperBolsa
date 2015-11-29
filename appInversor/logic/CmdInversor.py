import cmd
import threading
from appInversor.entity.InversorObject import InversorObject


class CmdInversor(cmd.Cmd, InversorObject):
    intro = 'Bienvenido a la aplicacion Inversor.   Type help or ? to list commands.\n'
    prompt = '(Inversor) '

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
        #print("Empresa  : " + str(empresa))
        #print("Cantidad : " + str(cantidad))
        #print("Valor  : " + str(valor))
        self.compraAcciones(empresa, cantidad, valor)

    def do_venta(self, args):
        "Coloca una orden de venta Ej: VENTA <EMPRESA> <CANTIDAD> <VALOR>"
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
        #print("Empresa  : " + str(empresa))
        #print("Cantidad : " + str(cantidad))
        #print("Valor  : " + str(valor))
        self.ventaAcciones(empresa, cantidad, valor)

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

    def do_noventa(self, args):
        "Cancela una orden de Venta Ej: NOVENTA <EMPRESA> <CANTIDAD> <VALOR>"
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

    def do_consulta(self, args):
        "Consulta el precio de las acciones de la empresa Ej: CONSULTA <EMPRESA>"
        parametros = args.split()
        if len(parametros) != 1:
            print("Numero Invalido de Argumentos")
            return
        empresa = str(parametros[0]).upper()
        for i in self.acciones:
          if str(i.empresa).upper() == empresa:
            print("Empresa  : " + str(empresa))
            print("Acciones : " + str(i.cantidad))

    def do_portafolio(self, args):
        "Muestra la cantidad de dinero en Efectivo que posee un inversor y l alista de acciones y sus cantidades"
        print("--------------Efectivo--------------")
        print("Efectivo : " + str(self.efectivo))
        print("--------------Acciones--------------")
        for accion in self.acciones:
            print("Empresa  : " + accion.empresa + " Cantidad : " + str(accion.cantidad))
        print("------------------------------------")

    def do_quit(self, line):
        "Termina la conexion con el corredor."
        return True

    def precmd(self, line):
        line = line.lower()
        return line

    def cmdloop(self, intro=None):
        print(self.efectivo)
        print(intro)
        return cmd.Cmd.cmdloop(self)
