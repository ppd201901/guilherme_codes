# Rodar o servidor: python rmi_server_ex4_5.py
import Pyro4

@Pyro4.expose
class ServerTest(object):
    # Exercício 4 da lista 1
    def calc_peso(self, alt, sex):
        peso = 0
        if sex == "masculino":
            peso = (72.7*alt)-58
        elif sex == "feminino":
            peso = (62.1 * alt) - 44.7
        return peso

    # Exercício 5 da lista 1
    def classe_nadador(self, idade):
        if idade >= 5 and idade <= 7:
            return "infantil A"
        elif idade >= 8 and idade <= 10:
            return "infantil B"
        elif idade >= 11 and idade <= 13:
            return "juvenil A"
        elif idade >= 14 and idade <= 17:
            return "juvenil B"
        elif idade >= 18:
            return "adulto"
        else:
            return "sem categoria definida"

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(ServerTest)   # register the server test as a Pyro object
ns.register("server.calcPeso", uri)
print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
daemon.requestLoop()                   # start the event loop of the server to wait for calls