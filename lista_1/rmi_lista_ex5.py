# saved as greeting-client.py
import Pyro4

uri = "PYRO:obj_9e2ee75f88f54cc08729b8963fe5deb3@localhost:60473"

greeting_maker = Pyro4.Proxy(uri)

nb = input("Qual a idade do nadador? ")
idade = int(nb)

print("A categoria do nadador é: ", greeting_maker.classe_nadador(idade))