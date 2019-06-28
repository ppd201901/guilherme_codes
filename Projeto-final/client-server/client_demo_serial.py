import codecs

import time
import pandas as pd
import numpy as np
from scipy import sparse
from scipy.sparse import csr_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.externals.joblib import Parallel, delayed
from sklearn.metrics import precision_score, recall_score, f1_score
import socket
import json


def client():
    host = "localhost" #socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    dataset = []

    for i in range(5000,55000):
        dataset.append(i)

    k_fold=1

    start_time = time.time()

    dataset = [dataset[x:x + 5000] for x in range(0, len(dataset), 5000)]

    for train_index in range(0, 10):
            X_train =  dataset[train_index]

            # convert csr_matrix to array
            #X_train = X_train.toarray()

            #X_train = np.asarray(X_train)

            # convert ndarray in json
            #df = pd.DataFrame(X_train)
            #X_train = df.to_json(orient="records")

            # Unconvert matrix to csr_matrix
            #X_train = sparse.csr_matrix(X_train)

            for i in range(0,2500000):
                i += 1


            for h in range(0,250000):
                h += 1


            obj = {
                "idx_train": X_train
            }

            msg = json.dumps(obj)

            client_socket.send(msg.encode())
            data = client_socket.recv(10000000).decode()
            obj = json.loads(data)

            print("Sum (fold = {}): {:.2f}".format(k_fold,obj["result"]))

            k_fold += 1

    print("--- %s seconds ---" % (round(time.time() - start_time,2)))


if __name__ == '__main__':
    client()