import socket, threading, json


class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("Nova conexão adicionada: ", clientAddress)

    def run(self):
        print ("Conexão vinda do: ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        while True:
            data = self.csocket.recv(1024).decode()

            if not data:
                break
            obj = json.loads(data)

            if (obj["func"] == "credito"):
                media = int(obj["media"])
                msg = "Seu saldo médio é: " + str(media) + ", você não tem crédito disponível"

                if (media > 200 and media <= 400):
                    msg = "Seu saldo médio é: " + str(media) + ", seu crédito disponível é " + str(media * 20 / 100)
                elif (media > 400 and media <= 600):
                    msg = "Seu saldo médio é: " + str(media) + ", seu crédito disponível é " + str(media * 30 / 100)
                elif (media > 600):
                    msg = "Seu saldo médio é: " + str(media) + ", seu crédito disponível é " + str(media * 40 / 100)

                self.csocket.send(msg.encode("utf-8"))
            else:
                msg = "Função não encontrada"
                self.csocket.send(msg.encode())
        print("Cliente do IP ", clientAddress , " desconectado...")


LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Servidor iniciado\nAguardando Requisições...")



while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()