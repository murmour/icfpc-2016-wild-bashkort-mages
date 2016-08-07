'''
Created on Aug 7, 2016

@author: linesprower
'''

from geom import crossp, dotp, vec, getDistance, getDistance2, fr_sqrt, parseNum
from fractions import Fraction
from geom import getfirst
import io, os 

class Line:
    def __init__(self, p1, p2):
        self.a = p2[1] - p1[1]
        self.b = p1[0] - p2[0]
        self.c = -(self.a * p1[0] + self.b * p1[1])
        
    def at(self, p):
        return self.a * p[0] + self.b * p[1] + self.c
    
    def normal(self):
        return self.a, self.b
    
    def reflect(self, p):
        d = self.a * self.a + self.b * self.b
        n = self.normal()
        t = self.at(p)
        return p[0] - Fraction(2 * t * n[0], d), p[1] - Fraction(2 * t * n[1], d)
    
    def invert(self):
        self.a = -self.a
        self.b = -self.b
        self.c = -self.c        
        
def sign(x):
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0

# def getCos(v1, v2):
#    return dotp(v1, v2) / getDistance(v1, v2) / getDistance(v1, v2)

def getComps(edges, n, bad):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    res = [None] * n
    num = 0
    
    def go(v):
        res[v] = num
        for u in adj[v]:
            if res[u] == None:
                go(u)                
    
    for i in range(n):
        if i in bad:
            continue
        if res[i] == None:
            go(i)
            num += 1
    return num, res
        
def getColors(edges, n):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    res = [None] * n
    
    def go(v, col):
        if res[v] != None and res[v] != col:
            return False
        if res[v] != None:
            return True
        res[v] = col
        for u in adj[v]:
            if not go(u, 1 - col):
                return False
        return True
            
    for i in range(n):
        if res[i] == None:
            if not go(i, 0):
                return None
            
    return res
    
    

def nagibate(pts, edges):
    n = len(pts)
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)        
    
    
    for u, v in edges:
        line = Line(pts[u], pts[v])
        lpts = set()  # indices of points on the line
        
        def checkOnSide():
            cur = 0
            for i, a in enumerate(pts):
                t = line.at(a)
                st = sign(t)
                if st != 0:
                    if st != cur and cur != 0:
                        return False
                    cur = st
                else:
                    lpts.add(i)
            return True
        
        if not checkOnSide():
            continue
        
        print('try %d %d' % (u, v))
        
        pp = {}
        
        def checkAngles():
            for i in lpts:
                exits = [j for j in adj[i] if line.at(pts[j]) != 0]
                if len(exits) != 2:
                    return False
                # print(exits)
                v1 = vec(pts[i], pts[exits[0]])
                v2 = vec(pts[i], pts[exits[1]])
                # print(v1, v2)
                if crossp(v1, v2) == 0:
                    return False
                # print(line.normal())
                sqlen1 = dotp(v1, v1)
                sqlen2 = dotp(v2, v2)                
                qq = fr_sqrt(Fraction(sqlen2, sqlen1))
                if qq == None:
                    return False
                pr1 = dotp(line.normal(), v1)
                pr2 = dotp(line.normal(), v2)
                if qq != Fraction(pr2, pr1):
                    return False
                pp[i] = (exits[0], exits[1])
            return True
        
        if not checkAngles():
            continue
                
        edges1 = [(a, b) for a, b in edges if a not in lpts and b not in lpts]
        cn, comps = getComps(edges1, n, lpts)
        
        cedges = []
        for a, b in pp.values():
            c1 = comps[a]
            c2 = comps[b]
            cedges.append((c1, c2))
        compscolor = getColors(cedges, cn)
        if not compscolor:
            continue
                
        # print(cn, comps)
        # assert(cn == 2)
        # compscolor = [0, 1]
        print('compscolor: ', compscolor)
        
        # get reflected set
        refl1 = set()
        refl2 = set()
        for i in range(n):
            if not i in lpts:
                if compscolor[comps[i]] == 0:
                    refl1.add(i)
                else:
                    refl2.add(i)
        print(refl1)
        if len(refl2) < len(refl1):
            refl2, refl1 = refl1, refl2
        
        # pts1 = list(pts)
        # for idx in refl1:
        #    pts1[idx] = line.reflect(pts[idx])
        idxmap = {}
        pts1 = []
        for i, v in enumerate(pts):
            if not i in lpts:
                idxmap[i] = len(pts1)
                pts1.append(line.reflect(v) if i in refl1 else v)
        if line.at(pts[getfirst(refl1)]) < 0:
            line.invert()
        
        edges1.extend(pp.values())
        edges1 = [(idxmap[a], idxmap[b]) for a, b in edges1]
        return pts1, edges1, line
    
    return None

def loadLines(idx):
    linesname = '../data/nagibated/%d.lines' % idx 
    if not os.path.exists(linesname):
        print('%s not exists!' % linesname)
        return None
        
    with io.open(linesname, 'r') as f:
        
        def getint():
            return int(f.readline())
        
        def getfrs():
            return list(map(parseNum, f.readline().split()))
        
        def readl():
            a, b, c = getfrs()
            r = Line((0, 0), (0, 0))
            r.a = a
            r.b = b
            r.c = c
            return r
            
        n = getint()
        return [readl() for _ in range(n)]

def solve_linear(a, b, c, d, e, f):
    det = a * e - b * d
    assert(det != 0)
    detx = c * e - b * f
    dety = a * f - c * d
    return detx / det, dety / det

def addp(a, b):
    return a[0] + b[0], a[1] + b[1]

def mulp(a, k):
    return a[0] * k, a[1] * k

def process(line, pts0, pts, facets):
    
    def normalize(x):
        return x
    
    newfacets = []
    to_flip = set()
    ptsi = { v : i for i, v in enumerate(zip(pts, pts0)) }
    for f in facets:
        tpos = []
        tneg = []            
        for i, j in zip(f, f[1:] + f[:1]):
            v = pts[i]
            if line.at(v) < 0:
                tpos.append(i)
            else:
                tneg.append(i)
                #tneg.append(len(pts))
                #pts.append(line.reflect(pts[i]))                
            u = pts[i]
            v = pts[j]
            if line.at(u) * line.at(v) < 0:
                l2 = Line(u, v)
                # pt = solve_linear(line.a, line.b, line.c, l2.a, l2.b, l2.c)
                
                tn = line.c + line.a * u[0] + line.b * u[1]
                td = line.a * (u[0] - v[0]) + line.b * (u[1] - v[1])
                t = tn / td
                print(t)
                pt = addp(u, mulp(vec(u, v), t))
                u0 = pts0[i]
                v0 = pts0[j]
                pt0 = addp(u0, mulp(vec(u0, v0), t))
                assert(line.at(pt) == 0)
                assert(l2.at(pt) == 0)
                
                if (pt, pt0) not in ptsi:
                    ni = len(pts)                    
                    pts.append(pt)
                    pts0.append(pt0)
                    ptsi[(pt, pt0)] = ni
                else:
                    ni = ptsi[(pt, pt0)]
                    
                tpos.append(ni)
                tneg.append(ni)
        print(tpos)
        print(tneg)
        to_flip.update(tpos)
        #for i in tpos:
        #    pts[i] = line.reflect(pts[i])
        if tpos:
            newfacets.append(normalize(tpos))
        if tneg:
            newfacets.append(normalize(tneg))
    
    for i in to_flip:
        pts[i] = line.reflect(pts[i])
    print(newfacets)
    print('Done')
    return pts0, pts, newfacets
            
        
            
         
                
                
                
            
                        
                
def denagibate(idx):
    solname = '../data/nagibated/%d_oxy_1.out' % idx
    if not os.path.exists(solname):
        print('%s not exists!' % solname)
        return False
    with io.open(solname, 'r') as f:
        
        def getint():
            return int(f.readline())
        
        def getpt(s):
            s = s.split(',')                
            return (parseNum(s[0]), parseNum(s[1]))
        
        def getints():
            return list(map(int, f.readline().split()))
        
        def readfacet():
            t = getints()
            assert(t[0] == len(t) - 1)
            return t[1:]                
        
        n = getint()
        pts0 = [getpt(f.readline()) for _ in range(n)]
        m = getint()
        facets = [readfacet() for _ in range(m)]
        pts = [getpt(f.readline()) for _ in range(n)]
        print(pts0, facets, pts)
        
    lines = loadLines(idx)
    if lines == None:
        return False
    print(lines)
    
    for l in lines:
        pts0, pts, facets = process(l, pts0, pts, facets)
        
    return (pts0, pts, facets)
        
        
                


def main():
    # l = Line((0, 0), (3, 3))
    # print(l.reflect((3, 1)))
    # print(getComps([(0, 5), (5, 4)], 6, {1, 2}))
    # t = nagibate([(0, 3), (2, 3), (3, 2), (2, 2), (3, 0), (0, 0)], [(0, 1), (1, 2), (2, 3), (2, 4), (1, 3), (4, 5), (5, 0)])
    # print(t)
    denagibate(1945)


if __name__ == '__main__':
    main()
