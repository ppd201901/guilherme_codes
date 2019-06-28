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
# noinspection PyUnresolvedReferences
from preparation.load_data import train_data, test_data
# noinspection PyUnresolvedReferences
from preparation.preprocessing import clean_text

def client():
    host = "localhost" #socket.gethostname()
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    vectorizer = TfidfVectorizer(stop_words="english", max_features=100,
                                 preprocessor=clean_text, ngram_range=(1,2))

    training_features = vectorizer.fit_transform(train_data["text"])
    test_features = vectorizer.transform(test_data["text"])

    kf = KFold(n_splits=10)
    kf.get_n_splits(training_features)
    kf.get_n_splits(test_features)

    labels_train = train_data["sentiment"]
    labels_test = test_data["sentiment"]

    print(kf)

    k_fold=1

    start_time = time.time()

    for train_index, test_index in kf.split(training_features):

            X_train, X_label = training_features[train_index], labels_train[train_index]
            y_test, y_label = test_features[test_index], labels_test[test_index]

            X_train = X_train.toarray()
            df = pd.DataFrame(X_train)
            X = df.values.tolist()

            for z in range(0, 22500):
                X_train = X[z]
                #dfObj = pd.DataFrame(X_train)
                #X_train = dfObj.to_json(orient="records")
                obj = {
                    "idx_train": X_train
                }

                msg = json.dumps(obj)
                client_socket.send(msg.encode())
                data = client_socket.recv(90000000).decode()
            print(z)

            obj = {
                "train_labels": X_label.tolist()
            }
            msg = json.dumps(obj)
            client_socket.send(msg.encode())
            data = client_socket.recv(90000000).decode()


            y_test = y_test.toarray()
            df = pd.DataFrame(y_test)
            X = df.values.tolist()

            z = 0
            for z in range(0, 2500):
                #print(X[z])
                y_test = X[z]
                #dfObj = pd.DataFrame(X_train)
                #X_train = dfObj.to_json(orient="records")
                obj = {
                    "idx_test": y_test
                }

                msg = json.dumps(obj)
                client_socket.send(msg.encode())
                data = client_socket.recv(90000000).decode()

            obj = {
                "test_labels": y_label.tolist()
            }
            msg = json.dumps(obj)
            client_socket.send(msg.encode())
            data = client_socket.recv(90000000).decode()
            result = json.loads(data)

            # Unconvert matrix to csr_matrix
            #X_train = sparse.csr_matrix(X_train)


            print("Accuracy (fold = {}): {:.2f}".format(k_fold, float(result["acc"])))
            print("Precision (fold = {}): {:.2f}".format(k_fold, float(result["pre"])))
            print("Recall (fold = {}): {:.2f}".format(k_fold, float(result["rec"])))
            print("F1 Score(fold = {}): {:.2f}".format(k_fold, float(result["f1"])))

            k_fold += 1

            print("--- %s seconds ---" % (round(time.time() - start_time, 2)))
            print(" ")




if __name__ == '__main__':
      client()