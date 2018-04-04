from time import time
import json
import pandas as pd
import numpy

def create_all_labels_dict_file_from_csv(paths_to_datasets, path_to_all_labels_file):
    clean_g = pd.read_csv(paths_to_datasets[0])
    malw_g = pd.read_csv(paths_to_datasets[1])
    pua_g = pd.read_csv(paths_to_datasets[2])

    clean_g_list = clean_g.iloc[:, -1].tolist()
    malw_g_list = malw_g.iloc[:, -1].tolist()
    pua_g_list = pua_g.iloc[:, -1].tolist()

    del clean_g
    del malw_g
    del pua_g

    dict_ = {}  # 0 - clean, 1 - pua, 2 - malw

    # we need a good FPP

    for item in clean_g_list:
        if item not in dict_:
            dict_[item] = 0

    for item in pua_g_list:
        if item not in dict_:
            dict_[item] = 1
        else:
            dict_[item] = 1

    for item in malw_g_list:
        if item not in dict_:
            dict_[item] = 2

    with open(path_to_all_labels_file, 'w') as file:
        file.write(json.dumps(dict_))

def X_Y_from_embeddings(all_labels_file, embeddings_file):
    with open(all_labels_file, 'r') as file:
        all_labels = json.loads(file.read())

    with open(embeddings_file, 'r') as file:
        embeddings = json.loads(file.read())

    x, y = [], []
    for key in embeddings:
        md5 = key.split('/')[-1].split('.')[0]
        x.append(embeddings[key])
        y.append(all_labels[md5])

    X = numpy.array([numpy.array(xi) for xi in x])
    Y = numpy.array([numpy.array(xi) for xi in y])
    return X, Y