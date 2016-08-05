'''
Created on Aug 5, 2016

@author: linesprower
'''

import io, os, json
import itertools
from fractions import Fraction
from math import sqrt

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

class Quad:
    def __init__(self, idxs, interiors):
        self.idxs = idxs
        self.interiors = interiors

class Interior:
    def __init__(self, v, others):
        self.v = v
        self.others = others

def loadP(idx):
    fname = '../data/problems/%d.p' % idx
    with io.open(fname) as f:
            
        def getline():
            while True:
                s = f.readline().strip()
                if s:
                    return s
            
        def getint():            
            return int(getline())
        
        def getints():
            return list(map(int, getline().split()))
        
        def readpath():
            t = getints()
            assert(t[0] + 1 == len(t))
            return t[1:]
        
        def readinterior():
            t = getints()
            v = t[0]
            assert(t[1] == len(t) - 2)
            others = t[2:]
            return Interior(v, others)
        
        def readquad(q):
            n_inter = getint()
            inters = [readinterior() for _ in range(n_inter)]
            return Quad(q, inters)            
        
        n_pathes = getint()
        patches = [readpath() for _ in range(n_pathes)]
        _n_quads = getint()
        quads = []
        while True:
            q = getints()
            if q[0] == -1:
                break
            quads.append(readquad(q))
            
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
        #allpts.append(getpt('1,1'))
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

class FrameEdge:
    def __init__(self, idxs, pts):
        a, b = idxs
        self.idxs = min(a, b), max(a, b)
        self.pts = pts
        
class QuadResult:
    def __init__(self, fr_edges, np):
        self.fr_edges = fr_edges
        self.np = np

def getDistance2(v1, v2):
    a = v1[0] - v2[0]
    b = v1[1] - v2[1]
    return a * a + b * b

def getDistance(v1, v2):
    return fr_sqrt(getDistance2(v1, v2))
        
def getfirst(s):
    for x in s:
        return x
    
def in_square(p):
    return 0 < p[0] < 1 and 0 < p[1] < 1
    
    
def testQuad(paths, verts, interiors):
    n = len(verts)
    #new_pts = [None] * n
    new_pts = [set() for _ in range(n)]    
    
    def getlen(i1, i2):
        return getDistance(verts[i1], verts[i2])
    
    fr_edges = []
    def addFrameEdge(i1, i2, p1, p2):
        fr_edges.append(FrameEdge((i1, i2), (p1, p2)))
        
    cur = (Fraction(0), Fraction(0))
    p = paths[0]
    new_pts[p[0]].add(cur)
    for i1, i2 in zip(p, p[1:]):
        old = cur
        cur = (cur[0] + getlen(i1, i2), cur[1])
        new_pts[i2].add(cur)
        addFrameEdge(i1, i2, old, cur)
    #print(cur)
    assert(cur == (Fraction(1), Fraction(0)))
    
    p = paths[1]
    new_pts[p[0]].add(cur)
    for i1, i2 in zip(p, p[1:]):
        old = cur
        cur = (cur[0], cur[1] + getlen(i1, i2))
        new_pts[i2].add(cur)
        addFrameEdge(i1, i2, old, cur)
    #print(cur)    
    assert(cur == (Fraction(1), Fraction(1)))
    
    p = paths[2]
    new_pts[p[0]].add(cur)
    for i1, i2 in zip(p, p[1:]):
        old = cur
        cur = (cur[0] - getlen(i1, i2), cur[1])
        new_pts[i2].add(cur)
        addFrameEdge(i1, i2, old, cur)
    assert(cur == (Fraction(0), Fraction(1)))
    
    p = paths[3]
    new_pts[p[0]].add(cur)
    for i1, i2 in zip(p, p[1:]):
        old = cur
        cur = (cur[0], cur[1] - getlen(i1, i2))
        new_pts[i2].add(cur)
        addFrameEdge(i1, i2, old, cur)
    assert(cur == (Fraction(0), Fraction(0)))
    
    for ip in interiors:
        c = verts[ip.v]
        assert(1 < len(ip.others) < 3)
        ia = ip.others[0]
        ib = ip.others[1]
        a = verts[ia]
        b = verts[ib]
        r1s = getDistance2(c, a)
        r2s = getDistance2(c, b)
        if len(new_pts[ia]) > 1:
            print(ia)
            print(new_pts[ia])
        #assert(len(new_pts[ia]) == 1)
        assert(len(new_pts[ib]) == 1)
        pts = getDistPoints(getfirst(new_pts[ia]), r1s, getfirst(new_pts[ib]), r2s)
        pts = [p for p in pts if in_square(p)]
        assert(pts)
        print(pts)
        assert(not new_pts[ip.v])
        new_pts[ip.v].add(pts[0])
        
    
    for i, t in enumerate(new_pts):
        if not t:
            print('Vertex %d is missing' % i)
            return None
    return QuadResult(fr_edges, new_pts)
    

# pts are [(Fraction, Fraction)], edges [(int, int)]
def extractFacets(pts, edges):
    #return [[0,5,6,1], [1,6,7,2], [2,7,9,8,3], [3,8,4]]
    #return [[3,5,4], [3,4,8,2], [1,2,8,9,7], [1,7,6,0]]
    #return [[4,5,3], [3,5,9,7,1], [1,7,8,2], [2,8,6,0]]
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
    def checkSanity(res):
        sum = Fraction(0)
        for poly in res:
            p0 = pts[poly[0]]
            t = Fraction(0)
            for a, b in zip(poly[1:], poly[2:]):
                va = vec(p0, pts[a])
                vb = vec(p0, pts[b])
                t += abs(crossp(va, vb))
            sum += t
        if sum != Fraction(2):
            return None
        
        
        
        return res
                
    
    
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
            return checkSanity(res)
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
            #assert(best != -1)
            if best == -1:
                return None
            eactive[ebest] -= 1
            if best == start_pt:
                break
            cur.append(best)
            v = best
        res.append(cur)
        
def extractFacetsX(pts0, pts, edges):
    n = len(pts)
    seen = set()
    sets = []
    print('pts=%s' % printverts(pts))
    for a, b in edges:
        if a in seen or b in seen:
            continue
        v1 = vec(pts[a], pts[b])
        t = set()
        for i in range(n):
            if i != a and i != b and crossp(vec(pts[a], pts[i]), v1) == 0:
                t.add(i)
        if t:
            t.add(a)
            t.add(b)
            sets.append(sorted(t))
            seen.update(t)
    
    print('sets = %s' % sets)
    if not sets:
        return extractFacets(pts0, edges)
    
    def testedge(a, b):
        for s in sets:
            if (a in s) and (b in s):
                return False
        return True
    
    edges0 = [(a, b) for a, b in edges if testedge(a, b)]
    
    sets = [getPartitions(s) for s in sets]    
    
    mm = itertools.product(*sets)    
    for zzz in mm:
        eee = list(edges0)
        for t in zzz:
            for u, v in t:
                eee.append((u, v))
        #saveFacets(pts0, eee, 'facets.json')
        ret = extractFacets(pts0, eee)
        if ret:
            saveFacets(pts0, eee, 'facets.json')
            return ret
    
    assert(False)
    
                

def getPartitions(a):
    print('a = %s' % a)
    n = len(a)
    used = [False] * n
    res = []
    cur = []
    def go(i, last):
        j = i
        while j < n and used[j]:
            j += 1
        if j == n:
            res.append([(a[q], a[p]) for q, p in cur])
            return
        if j > last:
            cur.append((last, j))
        used[j] = True
        if j + 1 < n:
            for k in range(j+1, n):
                if used[k]:
                    continue
                cur.append((j, k))
                used[k] = True
                go(j+1, max(last, k))
                cur.pop()
                used[k] = False            
        else:
            res.append([(a[q], a[p]) for q, p in cur])
        if j > last:
            cur.pop()
        used[j] = False
        
    go(0, 1)
    return res        




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

def saveFacets(np2, edges2, fname):
    j = {'v': [(float(a), float(b)) for a, b in np2], 'e': edges2}
    with io.open(fname, 'wt') as f: 
        f.write(json.dumps(j))
                
def test(idx):
    verts = loadVerts(idx)
    pat = loadP(idx)
    edges = loadEdges(idx)
    if not pat.quads:
        print('No way!')
    for q in pat.quads:
        print('Trying %s' % q.idxs)
        print('verts=%s' % printverts(verts))
        np = testQuad([pat.paths[i] for i in q.idxs], verts, q.interiors)
        if not np:
            continue
        #print(np)
        verts2 = []
        np2 = []
        emap = {}
        vidx = {}
        
        for i, se in enumerate(np.np):
            for v in se:
                emap[i] = len(verts2)
                vidx[v] = len(verts2)
                verts2.append(verts[i])
                np2.append(v)       
        
        frame = { fe.idxs for fe in np.fr_edges }
        edges2 = [(vidx[fe.pts[0]], vidx[fe.pts[1]]) for fe in np.fr_edges]
        def convertEdge(a, b):
            if (min(a, b), max(a, b)) in frame:
                return
            edges2.append((emap[a], emap[b]))
        
        for a, b in edges:
            convertEdge(a, b)
        
        print('np = %s' % printverts(np2))
        print('edges = %s' % edges2)
        
        saveFacets(np2, edges2, 'facets.json')
        
        facets = extractFacetsX(np2, verts2, edges2)
        #return
        saveSol(idx, np2, verts2, facets)
        print('Done!')
        break

def fr_sqrt(x):
    #return sqrt(float(x))
    #print(x)
    t1 = get_square(x.numerator)
    assert(t1 != None) 
    t2 = get_square(x.denominator)
    assert(t2 != None)
    return Fraction(t1, t2)    

def getDistPoints(p1, r1s, p2, r2s):    
    dx = Fraction(p2[0] - p1[0])
    dy = Fraction(p2[1] - p1[1])
    d2 = dx * dx + dy * dy
    q = r1s - r2s + d2
    ld = q / (2 * d2)
    l2 = q * q / (4 * d2)
    hd = (r1s - l2) / d2
    hd = fr_sqrt(hd)
        
    ax = p1[0] + ld * dx + hd * dy
    ay = p1[1] + ld * dy - hd * dx
    bx = p1[0] + ld * dx - hd * dy
    by = p1[1] + ld * dy + hd * dx
    return (ax, ay), (bx, by)
    

def test_distpoints():
    q = getDistPoints((2, 1), 2 * 2, (7, 5), 5 * 5)
    print(q)

def test_facets():
    global kSz
    kSz = 6
    pts = [(0, 0), (6, 6), (6, 2), (6, 0), (0, 3), (0, 6), (1, 6), (3, 6), (3, 4), (2, 2), (4, 2)]
    edges = [(5, 6), (6, 7), (7, 1), (5, 4), (6, 4), (7, 8), (1, 2), (8, 9), (8, 10), (4, 0), (9, 10), (10, 2), (9, 0), (9, 3), (2, 3), (0, 3)]
    facets = extractFacets(pts, edges)
    print(facets)

if __name__ == '__main__':
    #test_facets()
    #test_distpoints()
    test(16)
    #p = getPartitions([0, 1, 2, 3, 4, 6, 8, 9])
    #print([(0, 8), (1, 6), (2, 9), (3, 4)] in p)
    #for i in range(73, 102):
    #    if os.path.exists('../data/problems/%d.p' % i):
    #        test(i)
    
    