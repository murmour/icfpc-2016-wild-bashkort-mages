'''
Created on Aug 5, 2016

@author: linesprower
'''

import io, os, json
import itertools
from fractions import Fraction
from math import sqrt
from time import clock
from geom import getDistance2, getfirst
from nagibator import nagibate


kSz = 1


def transp(p, p0):
    return (float(p[0] - p0[0]), float(p[1] - p0[1]))

kFailNoQuads = 'NoQuads'
kFailFacetsNotFound = 'NoFacets'
kFailNegativeRoot = 'NegRoot'
kFailIrrationalRoot = 'IrrRoot'
kFailMissingVertices = 'MissVer'
kFailCombinationExceeded = 'CombTooMany'

class ESolverFailure(Exception):
    
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg = msg
        
class ESolverFailureRecv(ESolverFailure):
    pass

class Edge:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        
    def floatize(self, p0):
        self.a = transp(self.a, p0)
        self.b = transp(self.b, p0)
        
class Poly:
    def __init__(self, pts):
        self.pts = pts
        sum = 0
        if pts:
            for a, b in zip(pts, pts[1:] + [pts[0]]):
                sum += a[0] * b[1] - a[1] * b[0]
        #print(sum)
        self.hole = sum < 0
        
    def floatize(self, p0):
        self.pts = [transp(p, p0) for p in self.pts]

def is_external(a, b, xlen):
    ax, ay = a
    bx, by = b
    if ax == bx and (ax == 0 or ax == kSz * xlen):
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

def loadP(idx, bord_version):
    if idx < 0:
        fname = '../data/nagibated/%d.p%s' % (-idx, bord_version)
    else:
        fname = '../data/problems/%d.p%s' % (idx, bord_version)
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
    if idx < 0:
        fname = '../data/nagibated/%d.ind' % (-idx)
    else:
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
    if idx < 0:
        fname = '../data/nagibated/%d.in' % (-idx)
    else:
        fname = '../data/problems/%d.in' % idx
    with io.open(fname) as f:
            
        def getint():
            return int(f.readline())
        
        def getpt(s):
            s = s.split(',')                
            return (parseNum(s[0]), parseNum(s[1]))
        
        allpts = set()
        
        def readpoly():
            n = getint()
            t = [getpt(f.readline()) for _ in range(n)]
            #allpts.update(t)
            return t
                
        
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


class FrameEdge:
    def __init__(self, idxs, pts):
        a, b = idxs
        self.idxs = min(a, b), max(a, b)
        self.pts = pts
        
class QuadResult:
    def __init__(self, fr_edges, np, xlen):
        self.fr_edges = fr_edges
        self.np = np
        self.xlen = xlen

def getDistance(v1, v2):
    return fr_sqrt(getDistance2(v1, v2))
    
def getsecond(s):
    t = 0
    for x in s:
        t += 1
        if t == 2:
            return x
    
def in_square(p, xlen):
    return 0 < p[0] < xlen and 0 < p[1] < 1
    
    
def testQuad(paths, verts, interiors):
    n = len(verts)
    #new_pts = [None] * n
    new_pts = [set() for _ in range(n)]    
    
    def getlen(i1, i2):
        return getDistance(verts[i1], verts[i2])
    
    fr_edges = []
    def addFrameEdge(i1, i2, p1, p2):
        fr_edges.append(FrameEdge((i1, i2), (p1, p2)))
    
    allowed = {Fraction(1, n) for n in range(1, 120)}
        
    cur = (Fraction(0), Fraction(0))
    p = paths[0]
    new_pts[p[0]].add(cur)
    for i1, i2 in zip(p, p[1:]):
        old = cur
        cur = (cur[0] + getlen(i1, i2), cur[1])
        new_pts[i2].add(cur)
        addFrameEdge(i1, i2, old, cur)
    print(cur)
    assert(cur[0] in allowed)
    xlen = cur[0]
    #assert(cur == (Fraction(1), Fraction(0)))    
    
    
    p = paths[1]
    new_pts[p[0]].add(cur)
    for i1, i2 in zip(p, p[1:]):
        old = cur
        cur = (cur[0], cur[1] + getlen(i1, i2))
        new_pts[i2].add(cur)
        addFrameEdge(i1, i2, old, cur)
    #print(cur)    
    assert(cur == (xlen, Fraction(1)))
    
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
        if len(ip.others) < 2:
            continue
        if not (1 < len(ip.others) < 3):
            print('others=', ip.others)
        #assert(1 < len(ip.others) < 3)
        #ia = ip.others[0]
        #ib = ip.others[1]
        
        def getInt(ia, ib):        
            a = verts[ia]
            b = verts[ib]
            r1s = getDistance2(c, a)
            r2s = getDistance2(c, b)
            if len(new_pts[ia]) > 1:
                print('Multiple ia')
                print(ia)
                print(new_pts[ia])            
            #assert(len(new_pts[ia]) == 1)
            if len(new_pts[ib]) > 1:
                print('Multiple ib')
                print(ib, ip.v)
                print(c)
                print(new_pts[ib])
            #assert(len(new_pts[ib]) == 1)
            pts = getDistPoints(getfirst(new_pts[ia]), r1s, getfirst(new_pts[ib]), r2s)
            #print('intpts0', pts)
            pts = [p for p in pts if in_square(p, xlen)]
            #if not pts:
            #    return []
            #assert(pts)
            print('intpts=%s' % pts)
            
            #if len(pts) > 1: 
            #    #assert(pts[0] == pts[1])
            #    if pts[0] != pts[1]:
            #        return []
            #return pts[0]
            return pts
        
        assert(not new_pts[ip.v])    
        #for ia, ib in itertools.combinations(ip.others, 2):
        for ia, ib in [(ip.others[0], ip.others[1])]:
            #new_pts[ip.v].add(getInt(ia, ib))
            new_pts[ip.v].update(getInt(ia, ib))
            
        if len(new_pts[ip.v]) == 4:
            t = sorted(new_pts[ip.v])
            new_pts[ip.v] = {t[0], t[3]}
                        
            
    #print(new_pts)
    for i, t in enumerate(new_pts):
        if not t:
            #print('Vertex %d is missing' % i)
            return None
    return QuadResult(fr_edges, new_pts, xlen)
    

# pts are [(Fraction, Fraction)], edges [(int, int)]
def extractFacets(pts, edges, xlen, logg=False):
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
        if not is_external(pts[a], pts[b], xlen):
            eactive[i] += 1
        ed[a].append((i, b))
        ed[b].append((i, a))
        
    for i, v in enumerate(pts):
        if in_square(v, xlen) and len(ed[i]) % 2 == 1:
            #print('Oddity failure: %d' % i)
            return None
        
    #print('=======')
    
    #print(eactive)
    def checkSanity(res):
        if logg:
            print('Sanity')
        sum = Fraction(0)
        for poly in res:
            p0 = pts[poly[0]]
            t = Fraction(0)
            for a, b in zip(poly[1:], poly[2:]):
                va = vec(p0, pts[a])
                vb = vec(p0, pts[b])
                ac = abs(crossp(va, vb))
                #if ac == 0:
                #    return None
                t += ac
            sum += t
        #print(sum)
        if sum != 2 * xlen:
            return None        
        return res
                
    
    
    while True:
        # find a point with min x
        minp = None
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
                if start_pt == -1 or p < minp:
                    minp = p
                    start_pt = i
        if logg:
            print('start_pt = %d' % start_pt)
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
                    vgo = vec(pts[v], pts[cur[-2]])
                    vnext = vec(pts[v], pts[to])
                    if crossp(vgo, vnext) < 0:
                        continue                    
                    #print("try %d vs %d" % (to, best))
                    if best == -1 or not compare(pts[v], pts[best], pts[to]):
                        best = to
                        ebest = e
                else:
                    if best == -1 or compare(pts[v], pts[best], pts[to]):
                        best = to
                        ebest = e
            if logg:
                print('best = %d' % best)
            #assert(best != -1)
            if best == -1:
                return None
            eactive[ebest] -= 1
            if best == start_pt:
                break
            cur.append(best)
            v = best
        res.append(cur)

manual = []

def checkUnique(pts):
    pts = sorted(pts)
    for a, b in zip(pts, pts[1:]):
        if a == b:
            print(a)
            assert(a != b)
            
def checkCongrunce(pts, pts0, facets):
    for f in facets:
        for a, b in zip(f, f[1:] + f[:1]):
            if getDistance2(pts[a], pts[b]) != getDistance2(pts0[a], pts0[b]):
                return False
        for a, b, c in zip(f, f[1:] + f[:1], f[2:] + f[:2]):
            if dotp(vec(pts[b], pts[a]), vec(pts[b], pts[c])) != dotp(vec(pts0[b], pts0[a]), vec(pts0[b], pts0[c])):
                return False
    return True            

        
def extractFacetsX(pts0, pts, edges, xlen):
    
    
    
    if manual:
        return manual
    #return [[5,4,3,7], [4,8,3], [3, 8, 9, 6, 1, 0], [3, 0, 2, 7]]
    #return [[1, 4, 7, 6, 0], [7, 5, 6], [5, 9, 10, 6], [6, 10, 8, 3, 2, 0]]
    n = len(pts)
    seen = set()
    
    neibs = [set() for _ in range(n)]
    for a, b in edges:
        neibs[a].add(b)
        neibs[b].add(a)
    
    sets = []
    #checkUnique(pts)
    print('pts=%s' % printverts(pts))
    for a, b in edges:
        if a in seen or b in seen:
            continue
        v1 = vec(pts[a], pts[b])
        assert(v1[0] != 0 or v1[1] != 0)
        #t = set()
        t = {a, b}
        
        def hasNeibInT(v):
            for u in neibs[v]:
                if u in t:
                    return True
            return False
        
        for i in range(n):
            if i != a and i != b and crossp(vec(pts[a], pts[i]), v1) == 0 and hasNeibInT(i):
                t.add(i)
        if len(t) > 2:
            #t.add(a)
            #t.add(b)
            sets.append(sorted(t))
            seen.update(t)
    
    print('sets = %s' % sets)
    if not sets:
        t = extractFacets(pts0, edges, xlen)
        if not t:
            print(pts0)
            print(edges)
        assert(t)
        return t
    
    def testedge(a, b):
        for s in sets:
            if (a in s) and (b in s):
                return False
        return True
    
    edges0 = [(a, b) for a, b in edges if testedge(a, b)]
    
    sets0 = sets
            
    for skip in range(3):
        sets = [getPartitions(s, skip) for s in sets0]
        mm = itertools.product(*sets)
        ctr = 0
        start_t = clock()     
        for zzz in mm:
            ctr += 1
            if clock() - start_t > 5:
                print('Tried %.2f per second' % (ctr / 5))
                #raise ESolverFailure(kFailCombinationExceeded)
                break
            if ctr % 1000 == 0:
                print('ctr=', ctr)
            
            eee = []
            for t in zzz:
                for u, v in t:
                    eee.append((u, v))
            #print('eee=%s' % eee)
            eee.extend(edges0)
            #saveFacets(pts0, eee, 'facets.json')        
            ret = extractFacets(pts0, eee, xlen)            
            if ret:
                if checkCongrunce(pts, pts0, ret):                
                    saveFacets(pts0, eee, 'facets.json')
                    return ret
                else:
                    print('no congruence!')
        
    #mane = [ [(2,4), (4, 8), (8, 5), (1, 7)] ]
    mane = []
    for zzz in mane:
        eee = []
        for u, v in zzz:
            eee.append((u, v))        
        eee.extend(edges0)
        print('eee2=%s' % eee)
        #saveFacets(pts0, eee, 'facets.json')        
        ret = extractFacets(pts0, eee, xlen)
        if ret:
            saveFacets(pts0, eee, 'facets.json')
            return ret    
    
    #assert(False)
    raise ESolverFailure(kFailFacetsNotFound)
    
                

def getPartitions(a, skip0):
    #print('a = %s' % a)
    n = len(a)
    used = [False] * n
    res = []
    cur = []
    
    def add(cur):
        res.append([(a[q], a[p]) for q, p in cur])
    
    def go(i, last, skip):
        if len(res) > 1000:
            return
        j = i
        while j < n and used[j]:
            j += 1
        if j == n:
            add(cur)
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
                go(j+1, max(last, k), skip)
                cur.pop()
                used[k] = False            
        else:
            add(cur)
        if j > last:
            cur.pop()
        if skip:
            go(j+1, last, skip-1)
        used[j] = False
        
    if n > 4:
        aa = list(range(1, n-2))#  a[1:-2]
        for t in getPartitions(aa, skip0):
            q = t + [(0, n-2), (0, n-1)]            
            add(q)            
            #print(res[-1])
    
    if n == 3:
        add([(0, 1), (0, 2)])
        #add([(1, 0), (1, 2)])
        add([(0, 2), (1, 2)])
        
    if n == 4:
        add([(0, 1), (2, 3)])
        
    go(0, 1, skip0)    
    # todo: optimize out invalid
    return res


def optimizeSol(np, verts, facets):
    n = len(np)
    assert(n == len(verts))
    counts = [0] * n
    for fac in facets:
        for v in fac:
            counts[v] += 1
    pairs = [(t, i) for i, t in enumerate(counts)]
    pairs.sort(reverse=True)
    imap = { i1 : i for i, (_, i1) in enumerate(pairs) }
    np2 = [np[i] for _, i in pairs]
    verts2 = [verts[i] for _, i in pairs]
    
    def trans(f):
        return [imap[v] for v in f]
     
    facets2 = [trans(f) for f in facets]
    #print(pairs)    
    return np2, verts2, facets2


#def optimizeExtraV(np, verts, facets):
#    n = len(np)
#    e = [[] for _ in range(n)]
#    for  
    

def getSolName(idx):
    #return '../data/solutions/solution_%d_interior_%d.out' % (idx, kVersion)
    if idx < 0:
        return '../data/nagibated/%d_oxy_%d.out' % (-idx, kVersion)
    else:
        return '../data/solutions/solution_%d_nagibator_%d.out' % (idx, kVersion)

def saveSol(idx, np, verts, facets):
    fname = getSolName(idx)    
    np, verts, facets = optimizeSol(np, verts, facets)
    
    sz = [0]
    def fwrite(s):
        sz[0] += len(s.replace(' ', '').replace('\n', ''))
        f.write(s)
    
    with io.open(fname, 'wt') as f:
        fwrite('%d\n' % len(np))
        for v in np:
            fwrite('%s,%s\n' % (v[0], v[1]))
        fwrite('%d\n' % len(facets))
        for fac in facets:
            s = ' '.join(map(str, [len(fac)] + fac))
            fwrite('%s\n' % s)
        for v in verts:
            fwrite('%s,%s\n' % (v[0], v[1]))
            
    print('Solution size = %d' % sz[0])        

def printverts(verts):
    s = [' '.join('%s,%s' % (v[0], v[1]) for v in verts)]
    return s

def saveFacets(np2, edges2, fname):
    j = {'v': [(float(a), float(b)) for a, b in np2], 'e': edges2}
    with io.open(fname, 'wt') as f: 
        f.write(json.dumps(j))

def on_same_line(a, b, c):
    return crossp(vec(a, b), vec(a, c)) == 0

def simplify(sqv, tgtv, edges):
    n = len(sqv)
    e = [[] for _ in range(n)]
    for u, v in edges:
        e[u].append(v)
        e[v].append(u)
    bad = set()
    xedges = []
    for i, v in enumerate(sqv):
        if len(e[i]) == 2:
            x, y = e[i][0], e[i][1]
            if on_same_line(v, sqv[x], sqv[y]):
                bad.add(i)
                xedges.append((x, y))
    #print(bad)
    imap = {}
    xsqv = []
    xtgtv = []
    for i, (sv, tv) in enumerate(zip(sqv, tgtv)):
        if i in bad:
            continue
        imap[i] = len(xsqv)
        xsqv.append(sv)
        xtgtv.append(tv)
    edges2 = []
    for u, v in edges + xedges:
        if u not in imap or v not in imap:
            continue
        edges2.append((imap[u], imap[v]))
    return xsqv, xtgtv, edges2
    

def duplicateX(sqv, tgtv, edges, cnt):
    sqv1 = []
    tgt1 = []
    edges1 = []
    n = len(sqv)
    for i in range(cnt):
        add = Fraction(i if i % 2 == 0 else i+1 , cnt)
        mul = 1 if i % 2 == 0 else -1
        for v in sqv:
            vv = (v[0] * mul + add, v[1])
            sqv1.append(vv)
        for v in tgtv:
            tgt1.append(v)
        for a, b in edges:
            edges1.append((a + n * i, b + n * i))
            
    sqv2 = []
    tgtv2 = []
    idxs = {} # v -> new idx    
    for v, tv in zip(sqv1, tgt1):
        if v not in idxs:
            idxs[v] = len(sqv2)
            sqv2.append(v)
            tgtv2.append(tv)
    def mi(x, y):
        return min(x, y), max(x, y)
    edges2 = { mi(idxs[sqv1[a]], idxs[sqv1[b]]) for a, b in edges1 }
    return sqv2, tgtv2, list(edges2)
    
    
#def testQuadX(verts):
    

def savenagib(idx, iter, verts, edges):
    #n = len(verts)
    m = len(edges)
    num = idx * 100 + iter if iter > 0 else idx
    fname = '../data/nagibated/%d.in' % num
    with io.open(fname, 'wt') as f:
        f.write('1\n')
        f.write('0\n')
        f.write('%d\n' % m)
        for a, b in edges:
            f.write('%s,%s %s,%s\n' % (verts[a][0], verts[a][1], verts[b][0], verts[b][1]))
    

def resolveNagib(idx):
    print('TODO: resolve nagib!')

def make_nagib(idx):
    verts = loadVerts(idx)
    edges = loadEdges(idx)
    lines = []
    while True:
        t = nagibate(verts, edges)
        if not t:
            break
        verts, edges, l = t
        lines.append(l)
        savenagib(idx, len(lines), verts, edges)
        
    lines.reverse()
    with io.open('../data/nagibated/%d.lines' % idx, 'wt') as f:
        f.write('%d\n' % len(lines))
        for l in lines:
            f.write('%s %s %s\n' % (l.a, l.b, l.c))
    
    savenagib(idx, 0, verts, edges)
    print(lines)
    return True
         
        
    

def test(idx, bord_version=''):
    verts = loadVerts(idx)
    pat = loadP(idx, bord_version)
    edges = loadEdges(idx)
    if not pat.quads:
        print('No way!')
        raise ESolverFailure(kFailNoQuads)
    qlen = len(pat.quads[:500])
    print('Trying %d quads...' % qlen)
    for q in pat.quads[:500]:
        #print('Trying %s' % q.idxs)
        #print('verts=%s' % printverts(verts))
        try:
            np = testQuad([pat.paths[i] for i in q.idxs], verts, q.interiors)
        except ESolverFailureRecv:
            continue
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
        print('xlen=%s' % np.xlen)
        
        saveFacets(np2, edges2, 'facets.json')
        
        facets = extractFacetsX(np2, verts2, edges2, np.xlen)
        if np.xlen < 1:
            np2, verts2, edges2 = simplify(np2, verts2, edges2)
            #print('Simplify:')
            #print(np2)
            #print(verts2)
            #print(edges2)
            np2, verts2, edges2 = duplicateX(np2, verts2, edges2, int(1 / np.xlen))
            saveFacets(np2, edges2, 'facets.json')
            #print('!')
            facets = extractFacets(np2, edges2, 1)
            assert(facets)
        
        #print(facets)
        
        #return
        saveSol(idx, np2, verts2, facets)
        print('Done!')
        return True
    
    raise ESolverFailure(kFailMissingVertices)

def approx_sqrt(x):
    t = sqrt(float(x))
    res = Fraction.from_float(t)
    res.limit_denominator(10000000000000000000000000000000000000000000000000000000000000000000)
    return res

def fr_sqrt(x):
    #return sqrt(float(x))
    #print(x)
    if x < 0:
        raise ESolverFailureRecv(kFailNegativeRoot)
    t1 = get_square2(x.numerator)
    if t1 == None:        
        print(x.numerator)
        return approx_sqrt(x)
    if t1 == None:
        raise ESolverFailureRecv(kFailIrrationalRoot)
    assert(t1 != None) 
    t2 = get_square2(x.denominator)
    if t2 == None:
        print(x.denominator)
        return approx_sqrt(x)
    assert(t2 != None)
    return Fraction(t1, t2)  

def getDistPoints(p1, r1s, p2, r2s):
    print(p1, r1s, p2, r2s)
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

kVersion = 1
#kSkip = 1

def test_facets():
    global kSz
    #kSz = 6
    #pts = [(0, 0), (6, 6), (6, 2), (6, 0), (0, 3), (0, 6), (1, 6), (3, 6), (3, 4), (2, 2), (4, 2)]
    #edges = [(5, 6), (6, 7), (7, 1), (5, 4), (6, 4), (7, 8), (1, 2), (8, 9), (8, 10), (4, 0), (9, 10), (10, 2), (9, 0), (9, 3), (2, 3), (0, 3)]    
    pts = [(Fraction(1, 10), Fraction(13, 20)), (Fraction(0, 1), Fraction(0, 1)), (Fraction(0, 1), Fraction(3, 5)), (Fraction(1, 10), Fraction(0, 1)), (Fraction(1, 10), Fraction(1, 1)), (Fraction(0, 1), Fraction(2, 5)), (Fraction(0, 1), Fraction(1, 1)), (Fraction(1, 10), Fraction(7, 20))]
    edges = [(1, 3), (3, 7), (7, 0), (0, 4), (4, 6), (6, 2), (2, 5), (5, 1), (0, 2), (7, 5)]
    facets = extractFacets(pts, edges, Fraction(1, 10))
    print(facets)

if __name__ == '__main__':
    #test_facets()
    #test_distpoints()
    #manual.extend([[12,13,6,5], [5,6,7,9], [9,7,0,1], [13,3,2,6], [6,2,4,8,11,7], [7,11,10,0]]) # 23 todo: fix
    #manual.extend([[5,4, 8,6], [4,7,8], [7,2,1,3,8], [6,8,3,0]]) # 45 todo: fix 
    #manual.extend([[7,9,5], [9,12,11,6,3,5], [3,6,4], [4,6,2], [2,6,11,10,1], [1,10,8,0]]) # 56 todo: fix
    #manual.extend([[17, 14, 15, 16], [16,15,11,13], [13,11,10,9], [9,10,8,1], [1,8,6,3], [3,6,12,2], [2,12,5,4], [4,5,7,0]])
    make_nagib(1945)
    
    #test(25, '1')
    exit()
    #p = getPartitions([0, 1, 2, 3, 4, 6, 8, 9])
    #print([(0, 8), (1, 6), (2, 9), (3, 4)] in p)
    for i in range(70, 102):
        print(' === %d === ' % i)
        if os.path.exists('../data/problems/%d.p' % i):
            test(i)
    
    