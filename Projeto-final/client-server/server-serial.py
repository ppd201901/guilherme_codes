import pandas as pd
import socket
import json

from scipy import sparse
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
        vec = []
        vec2 = []
        for z in range(0, 22500):
            data = conn.recv(90000000).decode()
            #print(z)
            if not data:
                break

            X_train = []
            x = json.loads(data)
            #X_train = x["idx_train"]

            for element in x["idx_train"]:
                X_train.append(element)

            vec.append(X_train)
            ret={
                "ok": element
            }

            ret = json.dumps(ret)
            conn.send(ret.encode())

        X_train = sparse.csr_matrix(vec)

        data = conn.recv(90000000).decode()
        x = json.loads(data)
        X_label = pd.Series(x["train_labels"])
        ret = json.dumps(ret)
        conn.send(ret.encode())

        z = 0
        for z in range(0, 2500):
            data = conn.recv(90000000).decode()
            if not data:
                break
            y_test = []
            x = json.loads(data)
            #X_train = x["idx_train"]

            for element in x["idx_test"]:
                y_test.append(element)

            vec2.append(y_test)
            ret={
                "ok": element
            }

            ret = json.dumps(ret)
            conn.send(ret.encode())

        y_test = sparse.csr_matrix(vec2)


        data = conn.recv(90000000).decode()
        x = json.loads(data)
        y_label = pd.Series(x["test_labels"])


        model = LinearSVC()
        model.fit(X_train, X_label)
        y_pred = model.predict(y_test)

        # Evaluation
        acc = accuracy_score(y_label, y_pred.round())*100
        pre = precision_score(y_label, y_pred, average="macro") * 100
        rec = recall_score(y_label, y_pred, average="macro") * 100
        f1 = f1_score(y_label, y_pred, average="macro") * 100

        ret={
            "acc": acc,
            "pre": pre,
            "rec": rec,
            "f1": f1
        }

        ret = json.dumps(ret)
        conn.send(ret.encode())


if __name__ == '__main__':
    treino()