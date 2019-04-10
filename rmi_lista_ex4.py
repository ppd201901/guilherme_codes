import Pyro4

uri = "PYRONAME:server.calcPeso" #input("What is the Pyro uri of the greeting object? ").strip()
#name = input("What is your name? ")

server_test = Pyro4.Proxy(uri)  # get a Pyro proxy to the greeting object

nb = input("Qual sua altura? ")
altura = float(nb)

nb = input("Qual seu sexo? ")
sexo = str(nb)

print("Seu peso ideal deve ser: ", server_test.calc_peso(altura,sexo))