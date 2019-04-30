import socket
import json

SERVER = "127.0.0.1"
PORT = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((SERVER, PORT))
#client.sendall(bytes("This is from Client",'UTF-8'))

while True:
    saldo = input("Saldo Medio -> ")

    if (saldo == ""):
        break;

    obj = {
        "func": "credito",
        "media": float(saldo)
    }
    msg = json.dumps(obj)
    client_socket.send(msg.encode())
    data = client_socket.recv(1024).decode("utf8")

    print("\n" + data)

client_socket.close()