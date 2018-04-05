from time import time
import json
import pandas as pd
import numpy
import os

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

def foo():
    with open('all_labels.txt', 'r') as file:
        all_labels = json.loads(file.read())

    new_dic = {}
    c0,c1,c2=0,0,0
    num_category = 10000


    for key in all_labels:
        if c0 == num_category and c1 == num_category and c2 == num_category:
            break

        if all_labels[key] == 0 and c0 < num_category:
            new_dic[key] = 0 # though we can use list here
            c0 += 1
        if all_labels[key] == 1 and c1 < num_category:
            new_dic[key] = 1
            c1 += 1
        if all_labels[key] == 2 and c2 < num_category:
            new_dic[key] = 2
            c2 += 1

    with open('labels_30000.txt', 'w') as file:
        file.write(json.dumps(new_dic))

def copy_files(which_files_dict, src, dst):
    with open(which_files_dict, 'r') as file:
        files = json.loads(file.read())

    for key in files:
        os.system('cp ' + src + key + '.gexf ' + dst)