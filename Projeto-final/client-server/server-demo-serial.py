import socket
import json
from sklearn.svm import LinearSVC
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score

host = "localhost"
port = 5000

server_socket = socket.socket()
server_socket.bind((host, port))

server_socket.listen(10)
conn, address = server_socket.accept()


def treino():
    print("Connection from: " + str(address))
    while True:
        data = conn.recv(10000000).decode()
        #data = data[2:]
        if not data:
            break

        obj = json.loads(data)

        for i in range(0, 2500000):
            i += 1


        for h in range(0, 250000):
            h += 1


        # Evaluation
        result = 0
        for element in obj["idx_train"]:
            result += element

        ret={
            "result": result
        }

        msg = json.dumps(ret)

        conn.send(msg.encode())


if __name__ == '__main__':
    treino()