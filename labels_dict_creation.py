import joblib
import os
from time import time
import json
import pickle
from random import shuffle

path_chunks = '/home/pogorelov/data/chunks/data/'
path_to_output = '/home/pogorelov/output.txt'
path_to_all_labels = '/home/pogorelov/work/KL_graph_embeddings/all_labels.txt'
path_to_save_dict = '/home/pogorelov/dict.txt'

# path_chunks = 'C:\Users\pogorelov_g\Desktop\work\chunks\\'
# path_to_all_labels = 'all_labels.txt'
# path_to_save_dict = 'dict.txt'
# path_to_output = 'output.txt'

def dict_of_unique_labels(graph_dict, count_subgraphs={}):
    for key in graph_dict:
        if type(graph_dict[key]) is dict:
            if key not in count_subgraphs:
                count_subgraphs[key] = 1
            else:
                count_subgraphs[key] += 1
            dict_of_unique_labels(graph_dict[key], count_subgraphs)
        else:
            if graph_dict[key] not in count_subgraphs:
                count_subgraphs[graph_dict[key]] = 1
            else:
                count_subgraphs[graph_dict[key]] += 1
    return count_subgraphs

def word_and_label(item, all_labels):
    word = dict_of_unique_labels(item[1], {})
    label = all_labels[item[0]]
    del all_labels[item[0]]
    return word, label

def add_to_matrix(pca_matrix, count_subgraphs, sorted_vocab_list):
    l = [0 for i in xrange(len(sorted_vocab_list))]
    for key in count_subgraphs:
        ind = sorted_vocab_list.index(key)
        l[ind] = count_subgraphs[key]
    pca_matrix.append(l)


files = []
portion = 0.1
num_chunks_to_print = int(float(len(files)) * portion)
failed_jbls = {}
count_jbl = 0
pca_mat = []
targets = []

for filename in os.listdir(path_chunks):
    files.append(filename)
# shuffle(files)
# num_chunks_to_read = int(float(len(files))*portion)
# files = files[:num_chunks_to_read]

f = open(path_to_output, "w")
start = time()
with open(path_to_all_labels, 'r') as file:
    all_labels = json.loads(file.read())

dict_ = {}
for file_ in files:
    try:
        chunk = joblib.load(path_chunks + file_)
    except:
        continue
    for i, item in enumerate(chunk):
        dict_of_unique_labels(item[1], count_subgraphs=dict_)
    count_jbl += 1
    try:
        if count_jbl % num_chunks_to_print == 0:
            print >> f, '[%d] chunks are read' % count_jbl
    except ZeroDivisionError:
        pass

end = time()
print >> f, 'created dict from %d chunks in %0.2f min' % (len(files), (end - start) / 60)
with open(path_to_save_dict, 'wb') as fp:
    pickle.dump(dict_, fp)
f.close()