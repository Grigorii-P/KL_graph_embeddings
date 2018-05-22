import joblib
import os
from time import time
from random import shuffle
import pickle

path_chunks = '/home/pogorelov/data/chunks/data/'
path_to_output = '/home/pogorelov/output.txt'
path_to_dict = '/home/pogorelov/dict.txt'

def dict_of_unique_labels(graph_dict, labels={}):
    for key in graph_dict:
        if type(graph_dict[key]) is dict:
            dict_of_unique_labels(graph_dict[key], labels)
        else:
            if graph_dict[key] not in labels:
                labels[graph_dict[key]] = 1
            else:
                labels[graph_dict[key]] += 1

    return labels


files = []
portion = 0.1
for filename in os.listdir(path_chunks):
    files.append(filename)
# shuffle(files)
# num_chunks_to_read = int(float(len(files))*portion)
# files = files[:num_chunks_to_read]

num_chunks_to_print = int(float(len(files)) * portion)
failed_jbls = {}
count_jbl = 0
f = open(path_to_output, "w")
start = time()

labels = {}
for file_ in files:
    try:
        chunk = joblib.load(path_chunks + file_)
    except:
        continue
    for i, item in enumerate(chunk):
        dict_of_unique_labels(item[1], labels)
    count_jbl += 1
    try:
        if count_jbl % num_chunks_to_print == 0:
            print >> f, '[%d] chunks are read' % count_jbl
    except ZeroDivisionError:
        pass

end = time()

print >> f, 'created dict from %d chunks in %0.2f min' % (len(files), (end - start) / 60)
print >> f, ' '

with open(path_to_dict, 'w') as file:
    pickle.dump(labels, file)

f.close()