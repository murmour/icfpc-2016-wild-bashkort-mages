'''
Created on Aug 5, 2016

@author: linesprower
'''

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
    
    print(eactive)
    
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
        print('start_pt = %d' % start_pt)
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
                    print("try %d vs %d" % (to, best))
                    if best == -1 or not compare(pts[cur[-2]], pts[best], pts[to]):
                        best = to
                        ebest = e
                else:
                    if best == -1 or compare(pts[v], pts[best], pts[to]):
                        best = to
                        ebest = e
            print('best = %d' % best)
            assert(best != -1)
            eactive[ebest] -= 1
            if best == start_pt:
                break
            cur.append(best)
            v = best
        res.append(cur)    
                

def test():
    global kSz
    kSz = 6
    pts = [(0, 0), (6, 6), (6, 2), (6, 0), (0, 3), (0, 6), (1, 6), (3, 6), (3, 4), (2, 2), (4, 2)]
    edges = [(5, 6), (6, 7), (7, 1), (5, 4), (6, 4), (7, 8), (1, 2), (8, 9), (8, 10), (4, 0), (9, 10), (10, 2), (9, 0), (9, 3), (2, 3), (0, 3)]
    facets = extractFacets(pts, edges)
    print(facets)

if __name__ == '__main__':
    test()