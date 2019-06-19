import os
import numpy as np
import pandas as pd


def load_train_test_imdb_data(data_dir):
    """
    Carrega o IMDB train/test de uma uma pasta.

    Input:
    data_dir: caminho para a pasta  "aclImdb".

    Returns:
    retorna os cojuntos de dados de train/test como pandas dataframes.

    """
    data = {}
    for split in ["train", "test"]:
        data[split] = []
        for sentiment in ["neg", "pos"]:
            score = 1 if sentiment == "pos" else 0

            path = os.path.join(data_dir, split, sentiment)
            file_names = os.listdir(path)
            for f_name in file_names:
                with open(os.path.join(path, f_name), "r") as f:
                    review = f.read()
                    data[split].append([review, score])

    np.random.shuffle(data["train"])
    data["train"] = pd.DataFrame(data["train"],
                                 columns=['text', 'sentiment'])

    np.random.shuffle(data["test"])
    data["test"] = pd.DataFrame(data["test"],
                                columns=['text', 'sentiment'])

    return data["train"], data["test"]


train_data, test_data = load_train_test_imdb_data(data_dir="/Users/guilherme/Dropbox/Doutorado-UFG/Disciplinas/Processamento de Linguagem Natural/Trabalho/Datasets/aclImdb/")