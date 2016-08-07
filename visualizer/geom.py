'''
Created on Aug 7, 2016

@author: linesprower
'''
from fractions import Fraction
import math


def getDistance2(v1, v2):
    a = v1[0] - v2[0]
    b = v1[1] - v2[1]
    return a * a + b * b

def get_square2(t):
    if t == 0 or t == 1:
        return t
    l = 0
    r = t
    while l + 1 < r:
        m = (l + r) // 2
        if m * m > t:
            r = m
        else:
            l = m
    if l * l == t:
        return l
    return None

def getfirst(s):
    for x in s:
        return x

def fr_sqrt(x):
    #return math.sqrt(float(x))
    #print(x)
    assert(x >= 0)
    t1 = get_square2(x.numerator)
    if t1 == None:
        return None 
    t2 = get_square2(x.denominator)
    if t2 == None:
        return None
    return Fraction(t1, t2)

def getDistance(v1, v2):
    return fr_sqrt(getDistance2(v1, v2))

def crossp(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dotp(a, b):
    return a[0] * b[0] + a[1] * b[1]

def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])

def parseNum(s):
    t = s.split('/')
    if len(t) == 1:
        t.append('1')    
    t = list(map(int, t))
    return Fraction(t[0], t[1])

if __name__ == '__main__':
    pass