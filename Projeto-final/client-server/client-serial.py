import time
import pandas as pd
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

    vectorizer = TfidfVectorizer(stop_words="english", max_features=5000,
                                 preprocessor=clean_text, ngram_range=(1,2))

    training_features = vectorizer.fit_transform(train_data["text"])
    test_features = vectorizer.transform(test_data["text"])

    kf = KFold(n_splits=10)
    kf.get_n_splits(training_features)
    kf.get_n_splits(test_features)

    labels_train = train_data["sentiment"]
    labels_test = test_data["sentiment"]

    print(kf)
    '''
    accuracy = []
    precision = []
    recall = []
    f1 = []
    '''
    k_fold=1

    start_time = time.time()

    for train_index, test_index in kf.split(training_features):

            X_train, X_label = training_features[train_index], labels_train[train_index]
            y_test, y_label = test_features[test_index], labels_test[test_index]

            '''
            model = LinearSVC()
            model.fit(X_train, X_label)
            y_pred = model.predict(y_test)
            '''
            X_train = X_train.toarray()
            y_test = y_test.toarray()

            obj = {
                "idx_train": X_train.tolist(),
                "train_labels": X_label,
                "idx_test": y_test.tolist(),
                "test_labels": y_label
            }

            msg = json.dumps(obj)
            client_socket.send(msg.encode())
            data = client_socket.recv(1024).decode()

            print("Accuracy (fold = {}): {:.2f}".format(k_fold,data["acc"]))
            print("Precision: {:.2f}".format(k_fold,data["pre"]))
            print("Recall: {:.2f}".format(k_fold,data["rec"]))
            print("F1 Score: {:.2f}".format(k_fold,data["f1"]))

            k_fold += 1


    print("--- %s seconds ---" % (round(time.time() - start_time,2)))


if __name__ == '__main__':
    client()