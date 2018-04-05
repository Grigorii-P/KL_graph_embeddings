import numpy as np

def FP_without_pua(y_pred, y_test):
    fp = 0
    for i in range(len(y_pred)):
        if y_pred[i] == 2 and y_test[i] == 0:
            fp += 1
    return fp / len(y_pred)


def FP_with_pua(y_pred, y_test):
    fp = 0
    for i in range(len(y_pred)):
        if (y_pred[i] == 1 or y_pred[i] == 2) and y_test[i] == 0:
            fp += 1
    return fp / len(y_pred)


pred = np.array([1,1,2,1,0,0,2,2,0,1])
test = np.array([1,1,0,0,0,0,2,2,0,1])
print(FP_without_pua(pred,test))
print(FP_with_pua(pred,test))