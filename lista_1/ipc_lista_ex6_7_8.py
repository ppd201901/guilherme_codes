import socket
import json

host = "localhost"
port = 5000

server_socket = socket.socket()
server_socket.bind((host, port))

server_socket.listen(2)
conn, address = server_socket.accept()

def salarioLiquido(obj):
    msg = ""
    if (obj["nivel"] == "A"):
        descontos = 3;
        if (obj["numDependentes"] > 0):
            descontos = 8;
        descontos = obj["salario"] * descontos / 100
    elif (obj["nivel"] == "B"):
        descontos = 5;
        if (obj["numDependentes"] > 0):
            descontos = 10;
        descontos = obj["salario"] * descontos / 100
    elif (obj["nivel"] == "C"):
        descontos = 8;
        if (obj["numDependentes"] > 0):
            descontos = 15;
        descontos = obj["salario"] * descontos / 100
    elif (obj["nivel"] == "D"):
        descontos = 10;
        if (obj["numDependentes"] > 0):
            descontos = 17;
        descontos = obj["salario"] * descontos / 100

    msg = msg + "O Salario bruto de " + obj["nome"] + " é " + str(obj["salario"]) + "\n" + "Descontos: " + str(
        descontos) + "\n" + "Salario Liquido: " + str(obj["salario"] - descontos)

    conn.send(msg.encode())

def aposentadoria(obj):
    idade = obj["idade"]
    tempoServico = obj["tempoServico"]


    if(tempoServico>=30):
        msg = "Funcionario pode se aposentar"
    elif(idade>=60):
        if(idade>=65):
            msg = "Funcionario pode se aposentar"
        elif(tempoServico>=25):
            msg = "Funcionario pode se aposentar"
        else:
            msg = "Funcionario não pode se aposentar"
    else:
        msg = "Funcionario não pode se aposentar"

    conn.send(msg.encode())


def credito(obj):
    media = int(obj["media"])

    msg="Seu saldo médio é: "+str(media)+", você não tem crédito disponível"
    if(media>200 and media<=400):
        msg="Seu saldo médio é: "+str(media)+", seu crédito disponível é "+str(media*20/100)
    elif(media>400 and media<=600):
        msg = "Seu saldo médio é: " + str(media) + ", seu crédito disponível é " + str(media * 30 / 100)
    elif (media > 600):
        msg = "Seu saldo médio é: " + str(media) + ", seu crédito disponível é " + str(media * 40 / 100)

    conn.send(msg.encode())

def server():

    print("Connection from: " + str(address))
    while True:
        data = conn.recv(1024).decode()
        data = data[2:]
        if not data:
            break
        obj = json.loads(data)

        if(obj["func"]=="salarioLiquido"):
            salarioLiquido(obj)
        elif(obj["func"]=="aposentadoria"):
            aposentadoria(obj)
        elif(obj["func"]=="credito"):
            credito(obj)
        else:
            msg="Função não encontrada"
            conn.send(msg.encode())

    conn.close()


if __name__ == '__main__':
    server()