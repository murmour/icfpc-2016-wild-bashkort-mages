'''
Created on Aug 5, 2016

@author: linesprower
'''

import io
from fractions import Fraction
from macpath import curdir

kSz = 1


def transp(p, p0):
    return (float(p[0] - p0[0]), float(p[1] - p0[1]))

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def floatize(self, p0):
        self.a = transp(self.a, p0)
        self.b = transp(self.b, p0)

def is_external(a, b):
    ax, ay = a
    bx, by = b
    if ax == bx and (ax == 0 or ax == kSz):
        return True
    if ay == by and (ay == 0 or ay == kSz):
        return True
    return False

def compare(c, a, b):
    ax = a[0] - c[0]
    ay = a[1] - c[1]
    bx = b[0] - c[0]
    by = b[1] - c[1]
    return ax * by - ay * bx > 0

def crossp(a, b):
    return a[0] * b[1] - a[1] * b[0]

def dotp(a, b):
    return a[0] * b[0] + a[1] * b[1]

def vec(a, b):
    return (b[0] - a[0], b[1] - a[1])

def is_inside(c, a, b):
    if crossp(vec(a, b), vec(a, c)) != 0:
        return False
    if dotp(vec(a, b), vec(a, c)) <= 0:
        return False
    if dotp(vec(b, a), vec(b, c)) <= 0:
        return False
    return True
    

def splitEdges(pts, edges):
    res = []    
    for e in edges:
        inner = []
        for p in pts:
            if is_inside(p, e.a, e.b):
                inner.append(p)
        if inner:
            inner.append(e.a)
            inner.append(e.b)
            inner.sort()
            #print(inner)
            for p1, p2 in zip(inner, inner[1:]):
                res.append(Edge(p1, p2))
        else:
            res.append(e)
    return res


class Paths:
    def __init__(self, paths, quads):
        self.paths = paths
        self.quads = quads

def loadP(idx):
    fname = '../data/problems/%d.p' % idx
    with io.open(fname) as f:
            
        def getint():
            return int(f.readline())
        
        def getints():
            return list(map(int, f.readline().split()))
        
        def readpath():
            t = getints()
            assert(t[0] + 1 == len(t))
            return t[1:]
        
        n_pathes = getint()
        patches = [readpath() for _ in range(n_pathes)]
        n_quads = getint()
        quads = [getints() for _ in range(n_quads)]
        return Paths(patches, quads)

def loadEdges(idx):
    fname = '../data/problems/%d.ind' % idx
    with io.open(fname) as f:
            
        def getint():
            return int(f.readline())
        
        def getints():
            return tuple(map(int, f.readline().split()))
        
        def readpath():
            t = getints()
            assert(t[0] + 1 == len(t))
            return t[1:]
        
        n_verts = getint()
        for _ in range(n_verts):
            f.readline()
        n_edges = getint()
        return [getints() for _ in range(n_edges)]

def parseNum(s):
    t = s.split('/')
    if len(t) == 1:
        t.append('1')    
    t = list(map(int, t))
    return Fraction(t[0], t[1])
    
def loadVerts(idx):
    fname = '../data/problems/%d.in' % idx
    with io.open(fname) as f:
            
        def getint():
            return int(f.readline())
        
        def getpt(s):
            s = s.split(',')                
            return (parseNum(s[0]), parseNum(s[1]))
        
        def readpoly():
            n = getint()
            return [getpt(f.readline()) for _ in range(n)]
        
        allpts = set()
        
        def readedge():
            t = list(map(getpt, f.readline().split()))
            allpts.update(t)
            return Edge(t[0], t[1])                
        
        n_polys = getint()
        _polys = [readpoly() for _ in range(n_polys)]
        n_edges = getint()
        
        _edges = [readedge() for _ in range(n_edges)]
        allpts = sorted(list(allpts))
        return allpts


def get_square(t):
    #print(t)
    if t == 0 or t == 1:
        return t
    x = t // 2
    seen = set([x])
    while x * x != t:
        x = (x + (t // x)) // 2
        if x in seen: return None
        seen.add(x)
    return x
    
def testQuad(paths, verts):
    n = len(verts)
    new_pts = [None] * n    
    
    def getlen(i1, i2):
        a = verts[i1][0] - verts[i2][0]
        b = verts[i1][1] - verts[i2][1]
        sq = a * a + b * b
        t1 = get_square(sq.numerator)
        assert(t1 != None) 
        t2 = get_square(sq.denominator)
        assert(t2 != None)
        r = Fraction(t1, t2)
        #print(r)
        return r
        
    cur = (Fraction(0), Fraction(0))
    p = paths[0]
    new_pts[p[0]] = cur
    for i1, i2 in zip(p, p[1:]):
        cur = (cur[0] + getlen(i1, i2), cur[1])
        new_pts[i2] = cur
    #print(cur)
    assert(cur == (Fraction(1), Fraction(0)))
    
    p = paths[1]
    new_pts[p[0]] = cur
    for i1, i2 in zip(p, p[1:]):
        cur = (cur[0], cur[1] + getlen(i1, i2))
        new_pts[i2] = cur
    #print(cur)    
    assert(cur == (Fraction(1), Fraction(1)))
    
    p = paths[2]
    new_pts[p[0]] = cur
    for i1, i2 in zip(p, p[1:]):
        cur = (cur[0] - getlen(i1, i2), cur[1])
        new_pts[i2] = cur
    assert(cur == (Fraction(0), Fraction(1)))
    
    p = paths[3]
    new_pts[p[0]] = cur
    for i1, i2 in zip(p, p[1:]):
        cur = (cur[0], cur[1] - getlen(i1, i2))
        new_pts[i2] = cur
    assert(cur == (Fraction(0), Fraction(0)))
    
    for i, t in enumerate(new_pts):
        if t == None:
            print('Vertex %d is missing' % i)
            return None
    return new_pts
    

# pts are [(Fraction, Fraction)], edges [(int, int)]
def extractFacets(pts, edges):
    n = len(pts)
    m = len(edges)
    res = []
    active = [True] * n
    eactive = [1] * m
    ed = [[] for _ in range(n)]
    for i, (a, b) in enumerate(edges):
        if not is_external(pts[a], pts[b]):
            eactive[i] += 1
        ed[a].append((i, b))
        ed[b].append((i, a))
    
    #print(eactive)
    
    while True:
        # find a point with min x
        minx = None
        start_pt = -1
        for i, p in enumerate(pts):
            if active[i]:
                ok = False
                for e, _ in ed[i]:
                    if eactive[e]:
                        ok = True
                if not ok:
                    active[i] = False
                    continue                
                if start_pt == -1 or p[0] < minx:
                    minx = p[0]
                    start_pt = i
        #print('start_pt = %d' % start_pt)
        if start_pt == -1:
            return res
        cur = [start_pt]
        v = start_pt
        while True:
            best = -1
            ebest = None
            for e, to in ed[v]: # e is the number of edge, to is where it leads 
                if not eactive[e]:
                    continue                
                if len(cur) > 1:
                    if to == cur[-2]:
                        continue
                    #print("try %d vs %d" % (to, best))
                    if best == -1 or not compare(pts[cur[-2]], pts[best], pts[to]):
                        best = to
                        ebest = e
                else:
                    if best == -1 or compare(pts[v], pts[best], pts[to]):
                        best = to
                        ebest = e
            #print('best = %d' % best)
            assert(best != -1)
            eactive[ebest] -= 1
            if best == start_pt:
                break
            cur.append(best)
            v = best
        res.append(cur)    

def saveSol(idx, np, verts, facets):
    fname = '../data/solutions/%d.out' % idx
    with io.open(fname, 'wt') as f:
        f.write('%d\n' % len(np))
        for v in np:
            f.write('%s,%s\n' % (v[0], v[1]))
        f.write('%d\n' % len(facets))
        for fac in facets:
            s = ' '.join(map(str, [len(fac)] + fac))
            f.write('%s\n' % s)
        for v in verts:
            f.write('%s,%s\n' % (v[0], v[1]))        

def printverts(verts):
    s = [' '.join('%s,%s' % (v[0], v[1]) for v in verts)]
    return s
                
def test(idx):
    verts = loadVerts(idx)
    pat = loadP(idx)
    edges = loadEdges(idx)
    for q in pat.quads:
        print('Trying %s' % q)
        np = testQuad([pat.paths[i] for i in q], verts)
        if not np:
            continue
        print('np = %s' % printverts(np))
        print('edges = %s' % edges)
        facets = extractFacets(np, edges)
        saveSol(idx, np, verts, facets)
        print('Done!')
        


def test_facets():
    global kSz
    kSz = 6
    pts = [(0, 0), (6, 6), (6, 2), (6, 0), (0, 3), (0, 6), (1, 6), (3, 6), (3, 4), (2, 2), (4, 2)]
    edges = [(5, 6), (6, 7), (7, 1), (5, 4), (6, 4), (7, 8), (1, 2), (8, 9), (8, 10), (4, 0), (9, 10), (10, 2), (9, 0), (9, 3), (2, 3), (0, 3)]
    facets = extractFacets(pts, edges)
    print(facets)

if __name__ == '__main__':
    #test_facets()
    test(16)
    
    