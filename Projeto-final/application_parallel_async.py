import threading
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.metrics import precision_score, recall_score, f1_score

# noinspection PyUnresolvedReferences
from preparation.load_data import train_data, test_data
# noinspection PyUnresolvedReferences
from preparation.preprocessing import clean_text
import time



vectorizer = CountVectorizer(stop_words="english", max_features=5000,
                             preprocessor=clean_text)

training_features = vectorizer.fit_transform(train_data["text"])
test_features = vectorizer.transform(test_data["text"])

kf = KFold(n_splits=10)
kf.get_n_splits(training_features)
kf.get_n_splits(test_features)

labels_train = train_data["sentiment"]
labels_test = test_data["sentiment"]

print(kf)

accuracy = []
precision = []
recall = []
f1 = []
k_fold=1


def treino(k_fold, train_index, test_index, training_features):
        X_train, X_label = training_features[train_index], labels_train[train_index]
        y_test, y_label = test_features[test_index], labels_test[test_index]

        model = MultinomialNB()
        model.fit(X_train, X_label)
        y_pred = model.predict(y_test)

        # Evaluation
        #acc = accuracy_score(y_label,y_pred.round())
        #print("Accuracy (fold = {}): {:.2f}".format(k_fold, acc * 100))
        #print("Precision (fold = {}): {:.2f}".format(k_fold, precision_score(y_label, y_pred, average="macro") * 100))
        #print("Recall (fold = {}): {:.2f}".format(k_fold, recall_score(y_label, y_pred, average="macro") * 100))
        #print("F1 Score (fold = {}): {:.2f}".format(k_fold, f1_score(y_label, y_pred, average="macro") * 100))


for iterations in range(0,30):
    start_time = time.time()
    thread_list = []
    train_index = 0
    test_index = 0

    for train_index, test_index in kf.split(training_features):
        t = threading.Thread(target=treino, args=(k_fold, train_index, test_index, training_features))
        # t.daemon = True
        # t.start()
        # t.join()
        k_fold += 1
        thread_list.append(t)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("--- %s seconds ---" % (round(time.time() - start_time,2)))