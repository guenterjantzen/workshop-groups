DEBUG1 = False
DEBUG2 = False
DEBUG3 = False
DEBUG4 = False
DEBUG5 = False

def ordered_pairs(sequence):
    ret = {(i,j) for i in sequence for j in sequence if i<j}
    #if DEBUG1: print(f'ordered_pairs: {type(ret)}{ret}')
    return ret
