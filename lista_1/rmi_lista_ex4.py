import Pyro4

uri = "PYRONAME:server.calcPeso"

server_test = Pyro4.Proxy(uri)  # get a Pyro proxy to the server test

nb = input("Qual sua altura? ")
altura = float(nb)

nb = input("Qual seu sexo? ")
sexo = str(nb)

print("Seu peso ideal deve ser: ", server_test.calc_peso(altura,sexo))