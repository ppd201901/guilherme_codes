import zerorpc

class HelloRPC(object):
    def hello(self, name, number):
        return "Hello, {} {}".format(name, number)

s = zerorpc.Server(HelloRPC())
s.bind("tcp://0.0.0.0:4242")
s.run()