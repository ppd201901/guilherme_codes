import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.externals.joblib import Parallel, delayed
from sklearn.metrics import precision_score, recall_score, f1_score

# noinspection PyUnresolvedReferences
from preparation.load_data import train_data, test_data
# noinspection PyUnresolvedReferences
from preparation.preprocessing import clean_text
import time



vectorizer = TfidfVectorizer(stop_words="english", max_features=5000,
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
        acc = accuracy_score(y_label,y_pred.round())

        print("Accuracy on the IMDB dataset (fold = {}): {:.2f}".format(k_fold, acc * 100))
        print("Precision: {:.2f}".format(precision_score(y_label, y_pred, average="macro") * 100))
        print("Recall: {:.2f}".format(recall_score(y_label, y_pred, average="macro") * 100))
        print("F1 Score: {:.2f}".format(f1_score(y_label, y_pred, average="macro") * 100))

        k_fold += 1


start_time = time.time()


Parallel(n_jobs=10)(delayed(treino)(k_fold,train_index, test_index, training_features) for train_index, test_index in kf.split(training_features))
print("--- %s seconds ---" % (round(time.time() - start_time,2)))