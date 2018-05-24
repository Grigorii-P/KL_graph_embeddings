import pickle

l = [1,5,3]
l = {'a':1,'b':5,'c':3}
sort_vocab = sorted(l.items(),key=lambda x: x[1], reverse=True)
sort_vocab = [x[0] for x in sort_vocab]

print(sort_vocab)