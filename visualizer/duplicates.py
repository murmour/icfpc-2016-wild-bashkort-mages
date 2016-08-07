'''
Created on Aug 7, 2016

@author: linesprower
'''

import hashlib, os, io

def getinname(idx):
    return '../data/problems/%d.in' % idx

def gethash(idx):
    fname = getinname(idx)
    md5 = hashlib.md5()
    with io.open(fname, 'rb') as f:
        md5.update(f.read())
    return md5.hexdigest()

def findem():
    fnames = [f for f in os.listdir('../data/problems') if f.endswith('.in')]        
    idxs = sorted([int(f.split('.')[0]) for f in fnames])
    m = {}
    for i in idxs:
        h = gethash(i)
        if h in m:
            m[h].append(i)
        else:
            m[h] = [i]
    for v in sorted(m.values()):
        if len(v) > 1:
            print(' '.join(str(i) for i in v))
            

if __name__ == '__main__':
    findem()