import zerorpc

class HelloRPC(object):
    def hello(self, name, number):
        return "Hello, {} {}".format(name, number)

    def calc_peso(self, alt, sex):
        peso = 0
        alt = float(alt)

        if sex == "masculino":
            peso = (72.7*alt)-58
        elif sex == "feminino":
            peso = (62.1 * alt) - 44.7
        return peso

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()