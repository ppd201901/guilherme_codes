import time

from sklearn.externals.joblib import Parallel, delayed
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.manifold import SpectralEmbedding
from sklearn.metrics import accuracy_score
import keras.models
from keras.layers import Dense
from sklearn.model_selection import KFold
# noinspection PyUnresolvedReferences
from preparation.load_data import train_data, test_data
# noinspection PyUnresolvedReferences
from preparation.preprocessing import clean_text
from sklearn.metrics import precision_score, recall_score, f1_score


vectorizer = CountVectorizer(stop_words="english",max_features=5000,
                             preprocessor=clean_text)

training_features = vectorizer.fit_transform(train_data["text"])
test_features = vectorizer.transform(test_data["text"])


kf = KFold(n_splits=10)
kf.get_n_splits(training_features)
kf.get_n_splits(test_features)

labels_train = train_data["sentiment"]
labels_test = test_data["sentiment"]

print(kf)

k_fold=1

accuracy = []
precision = []
recall = []
f1 = []

for iterations in range(0,30):
    start_time = time.time()
    for train_index, test_index in kf.split(training_features):
        # Training
        model = keras.models.Sequential()

        model.add(Dense(16, input_dim=5000, activation='relu', kernel_initializer="uniform"))

        # Creating a 8 neuron hidden layer.
        model.add(Dense(8, activation='relu', kernel_initializer="uniform"))
        # Creating a 8 neuron hidden layer.
        model.add(Dense(8, activation='relu', kernel_initializer="uniform"))

        # Adding a output layer.
        model.add(Dense(1, activation='sigmoid', kernel_initializer="uniform"))

        # Compiling the model
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

        X_train, X_label = training_features[train_index], labels_train[train_index]
        y_test, y_label = test_features[test_index], labels_test[test_index]

        model.fit(X_train, X_label, nb_epoch=1, batch_size=10, verbose=0)
        y_pred = model.predict(y_test)

        scores = model.evaluate(y_test, y_label, verbose=5)

        yy_score=[]
        indice=0

        for i in y_pred:
            if i < 0.5:
                yy_score.append(0)
            else:
                yy_score.append(1)
            indice += 1

        # Metrics
        # print("Accuracy: {:.2f}".format(scores[1] * 100))
        # print("Precision: {:.2f}".format(precision_score(y_label, yy_score, average="macro") * 100))
        # print("Recall: {:.2f}".format(recall_score(y_label, yy_score, average="macro") * 100))
        # print("F1 Score: {:.2f}".format(f1_score(y_label, yy_score, average="macro") * 100))

        k_fold += 1
    print("--- %s seconds ---" % (round(time.time() - start_time,2)))