
# coding: utf-8

# ## gexf graphs creation

# ### for python 2.7

# In[2]:


import joblib
import os
import networkx as nx
from time import time
import json
import random
from random import shuffle
import pandas as pd
import string


# In[3]:


def word_generator(len_):
    return "".join(random.choice(string.ascii_letters) for j in range(len_))

def count_non_unique_names(dic, non_uniques={}):
    for key in dic:
        if key in non_uniques:
                non_uniques[key] += 1
        else:
            non_uniques[key] = 0
        if type(dic[key]) is dict:
            count_non_unique_names(dic[key], non_uniques)
    res = {}
    for key in non_uniques:
        if non_uniques[key] > 0:
            res[key] = non_uniques[key]
    return res

def how_many_non_uniques(d, counts={}):
    for key in d:
        if key not in counts:
            counts[key] = 0
        else:
            counts[key] += 1
        
        if type(d[key]) is dict:
            _ = how_many_non_uniques(d[key], counts)
            
    return sum(counts.values())
            
def change_non_unique_names(dic, non_uniques, new_dic={}):
    for key in dic:
        if key in non_uniques:
                split = key.split('.')
                if len(split) > 1:
                    before_dot = ''.join(split[:len(split)-1])
                    new_key = before_dot + word_generator(5) + '.' + split[-1]
                else:
                    whole_name = split[0]
                    new_key = whole_name + word_generator(5)
                non_uniques[key] -= 1
                if non_uniques[key] == -1:
                    del non_uniques[key]
        else:
            new_key = key
        
        if type(dic[key]) is dict:
            temp = change_non_unique_names(dic[key], non_uniques, {})
            new_dic[new_key] = temp
        else:
            new_dic[new_key] = dic[key]
    return new_dic  
                        
def create_nodes_and_edges(G, dic, root):
    for key in dic:
        if type(dic[key]) is dict:
            G.add_node(key, label=key)
            G.add_edge(root, key)
            G = create_nodes_and_edges(G, dic[key], key)
        else:
            G.add_node(key, label=dic[key])
            G.add_edge(root, key)
    return G


# In[4]:


# path_chunks = '/home/pogorelov/data/'
# path_to_save = '/home/pogorelov/gexf_graphs/'
path_chunks = '/Users/grigoriipogorelov/Desktop/chunks/'
path_to_save = '/Users/grigoriipogorelov/Desktop/graphs/'
path_to_output = '/Users/grigoriipogorelov/Desktop/output.txt'

files = []
portion = 0.1
for filename in os.listdir(path_chunks):
    files.append(filename)
# shuffle(files)
# num_chunks_to_read = int(float(len(files))*portion)
# files = files[:num_chunks_to_read]

num_chunks_to_print = int(float(len(files))*portion)
failed_jbls = {}
count_jbl = 0
f=open(path_to_output,"w")
start = time()

for file_ in files:
    try:
        chunk = joblib.load(chunks_path + file_)
    except:
        continue
    for i, item in enumerate(chunk):
        non_unique_nodes = count_non_unique_names(item[1], {})
        before.append(how_many_non_uniques(item[1],{}))
        if any(non_unique_nodes):
            graph_dict = change_non_unique_names(item[1], non_unique_nodes, {})
        else:
            graph_dict = item[1]
        after.append(how_many_non_uniques(graph_dict,{}))
        G = nx.Graph()
        G.add_node('APK_ROOT', label='APK_ROOT')
        G = create_nodes_and_edges(G, graph_dict, 'APK_ROOT')
        nx.write_gexf(G, path_to_save + item[0] + '.gexf')
    count_jbl += 1
    try:
        if count_jbl % num_chunks_to_print == 0:
            print >> f, '[%d] chunks are read' % count_jbl
    except ZeroDivisionError:
        pass

end = time()
    
print >> f, 'downloading and creating %d gexfs is %0.2f min' % (len(files), (end - start)/60)
print >> f, ' '

_,_,chunks_num = os.walk(path_chunks).next()
print >> f, '%d chunks in %s ' % (len(chunks_num),path_chunks)
_,_,gexf_num = os.walk(path_to_save).next()
print >> f, '%d gexf graphs in %s ' % (len(gexf_num),path_to_save)

f.close()


# In[ ]:


with open('/Users/grigoriipogorelov/Desktop/test/degrees/initial_relab.txt', 'w') as file:
    pickle.dump(to_file_dict, file)


# In[24]:


# d = {u'AndroidManifest.xml': 'AXML_PLUS',
#  u'abc': {u'assets': u'CERT_NORM',
#   u'CERT.SF': u'SIG_PLUS', u'asd':{'asd':'qwe'},
#   u'MANIFEST.MF': u'MANIF_PLUS'},
#  u'assets': {u'AndroidManifest.xml': u'PNG_NORM',
#   u'assets': u'PNG_NORM'},
#     u'MANIFEST.MF': u'MANIF_PLUS'}

# r = count_non_unique_names(d, {})
# new_d = change_non_unique_names(d, r, {})
# how_many_non_uniques(d, {}), how_many_non_uniques(new_d, {})


# In[19]:


# import matplotlib.pyplot as plt
# fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

# # We can set the number of bins with the `bins` kwarg
# n_bins = 60
# axs[0].hist(before, bins=n_bins)
# axs[1].hist(after, bins=n_bins)


# ## Labels

# In[1]:


from time import time
import json
import ast
import utils as u


# create only malware and benign (without pua)

# In[2]:


u.create_equal_portions(dst_file='labels_30000.txt')


# In[3]:


a = json.load(open('labels_30000.txt'))
u.test_proportions_from_dict(a)


# In[1]:


# common_path = '/Users/grigoriipogorelov/Desktop/KL/v7/'
# datasets = [common_path + 'clean_g.csv', common_path + 'malw_g.csv', common_path + 'pua_g.csv']
# path_to_all_labels_file = '/Users/grigoriipogorelov/Desktop/KL_graph_embeddings/KL_graph_embeddings/all_labels.txt'
# u.create_all_labels_dict_file_from_csv(datasets, path_to_all_labels_file)


# In[2]:


# path_to_gexf = '/Users/grigoriipogorelov/Desktop/KL/gexf_graphs/'
# path_to_labels_file = '/Users/grigoriipogorelov/Desktop/KL/labels.Labels'

# _,_,files = os.walk(path_to_gexf).next()

# with open(path_to_labels_file, 'w') as f:
#     for file_ in files:
#         clean, malw, pua = False, False, False
#         count +=1
#         spl = file_.split('.')
#         name = spl[0]
#         if name in clean_g_list:
#             clean = True
#         if name in malw_g_list:
#             malw = True
#         if name in pua_g_list:
#             pua = True
            
#         if clean and pua:
#             f.write(file_+' '+'2'+'\n')
#             continue
#         if malw and pua:
#             f.write(file_+' '+'1'+'\n')
#             continue
#         if clean:
#             f.write(file_+' '+'0'+'\n')
#         if malw:
#             f.write(file_+' '+'1'+'\n')
#         if pua:
#             f.write(file_+' '+'2'+'\n')

# len(missed), len(files), count


# In[3]:


# with open('/Users/grigoriipogorelov/Desktop/KL/clean_g.txt') as f:
#     clean_g_list = f.readlines()
# clean_g_list = [x.strip() for x in clean_g_list]

# with open('/Users/grigoriipogorelov/Desktop/KL/malw_g.txt') as f:
#     malw_g_list = f.readlines()
# malw_g_list = [x.strip() for x in malw_g_list]

# with open('/Users/grigoriipogorelov/Desktop/KL/pua_g.txt') as f:
#     pua_g_list = f.readlines()
# pua_g_list = [x.strip() for x in pua_g_list]

