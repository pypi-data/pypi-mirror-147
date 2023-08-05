import numpy as np

## Class reweighting strategies for class imbalance 

def ClsBalW(labels, LargeN):
    import numpy as np
    #Get frequency and number of classes
    ni = np.bincount(labels)
    Nclass= len(np.unique(labels))

    #calculate class-balanced weight followed by Cui et al. "Class-balanced loss based on effective number of samples"
    Ni = LargeN #given hyper parameter, as LagerN -> inf, the equqation returns compute_class_weight("balanced") from sklearn. 
    beta = (Ni-1)/(Ni)
    Effn= (1 - beta)/(1 - beta**(ni))
    SumW = np.sum(Effn)
    return Effn * Nclass/SumW #reweight so sum of all weights equals to number of classes. 


def GetDictCls(GivenWeight, labels):
    class_weight = dict()
    i = 0
    for id in np.unique(labels):
        class_weight[id] = round(GivenWeight[i],2)
        i = i+1
    return class_weight


def ConvertLabelsToInt(ls_labels):
  if type(ls_labels) is not list:
    print("error!")
  Ordered = sorted(set(ls_labels))
  i = 0
  LookUp = dict()
  for label in Ordered:
    LookUp[label] = i
    i += 1

  RevLookUp = dict()
  ls_labels_int = [LookUp[item] for item in ls_labels]
  RevLookUp = zip(ls_labels_int, ls_labels)

  return ls_labels_int, dict(RevLookUp)
