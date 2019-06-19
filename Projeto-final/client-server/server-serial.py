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
        data = conn.recv(1024).decode()
        data = data[2:]
        if not data:
            break
        obj = json.loads(data)

        X_train = obj["idx_train"]
        X_label = obj["train_labels"]
        y_test = obj["idx_test"]
        y_label = obj["test_labels"]

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

        conn.send(ret.encode())
    

if __name__ == '__main__':
    treino()