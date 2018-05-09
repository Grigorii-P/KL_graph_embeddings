from __future__ import division
from time import time
import json
import pandas as pd
import numpy
import os
import random

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

def create_csv_features(ready_md5, paths_to_datasets):
    with open(ready_md5, 'r') as file:
        md5 = json.loads(file.read())

    clean_g = pd.read_csv(paths_to_datasets[0])
    malw_g = pd.read_csv(paths_to_datasets[1])
    pua_g = pd.read_csv(paths_to_datasets[2])

    res_dict = {}
    for key in md5:
        slice_ = clean_g.iloc[:, 1579] == key
        if slice_.any():
            res_dict[key] = clean_g[slice_].iloc[0, 1:1579].tolist()
            continue
        slice_ = malw_g.iloc[:, 1579] == key
        if slice_.any():
            res_dict[key] = malw_g[slice_].iloc[0, 1:1579].tolist()
            continue
        slice_ = pua_g.iloc[:, 1579] == key
        if slice_.any():
            res_dict[key] = pua_g[slice_].iloc[0, 1:1579].tolist()
            continue

    with open('labels_30000_with_csv_features.txt', 'w') as file:
        file.write(json.dumps(res_dict))

def create_equal_portions(dst_file):
    with open('all_labels.txt', 'r') as file:
        all_labels = json.loads(file.read())

    new_dic = {}
    c0, c1, c2 = 0, 0, 0
    num_category = 10000

    keys =  list(all_labels.keys())
    random.shuffle(keys)
    
    for key in keys:
        if c0 == num_category and c2 == num_category:
            break

        if all_labels[key] == 0 and c0 < num_category:
            new_dic[key] = 0
            c0 += 1
#        if all_labels[key] == 1 and c1 < num_category:
#            new_dic[key] = 1
#            c1 += 1
        if all_labels[key] == 2 and c2 < num_category:
            new_dic[key] = 2
            c2 += 1

    with open(dst_file, 'w') as file:
        file.write(json.dumps(new_dic))

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


def X_Y_from_embeddings_and_csv(all_labels_file, embeddings_file, csv_features_file):
    with open(all_labels_file, 'r') as file:
        all_labels = json.loads(file.read())

    with open(embeddings_file, 'r') as file:
        embeddings = json.loads(file.read())

    with open(csv_features_file, 'r') as file:
        csv_features = json.loads(file.read())

    x, y = [], []
    for key in embeddings:
        md5 = key.split('/')[-1].split('.')[0]
        x.append(embeddings[key] + csv_features[md5])
        y.append(all_labels[md5])

    X = numpy.array([numpy.array(xi) for xi in x])
    Y = numpy.array([numpy.array(xi) for xi in y])
    return X, Y


def test_proportions_Y(Y):
    c0, c1, c2 = 0, 0, 0
    for item in Y:
        if item == 0:
            c0 += 1
        if item == 1:
            c1 += 1
        if item == 2:
            c2 += 1
            
def test_proportions_from_dict(dict_):
    c0, c2 = 0, 0
    for key in dict_.keys():
        if dict_[key] == 0:
            c0 += 1
        if dict_[key] == 2:
            c2 += 1

    print('clean %.1f, malw %.1f' % ((c0 / (c0 + c2)), (c2 / (c0 + c2))))

def copy_files(which_files_dict, src, dst):
    with open(which_files_dict, 'r') as file:
        files = json.loads(file.read())

    for key in files:
        os.system('cp ' + src + key + '.gexf ' + dst)