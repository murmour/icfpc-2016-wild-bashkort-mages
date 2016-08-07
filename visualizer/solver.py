'''
Created on Aug 6, 2016

@author: linesprower
'''
import os, re, io, json, subprocess, datetime, traceback
from facets import Poly, Edge, transp, parseNum, splitEdges
import facets
import icfp_api

soldirname = '../data/solutions'
probdirname = '../data/problems'

def checkOk(idx):
    try:        
        test = re.compile(r'solution_%d_.*response' % idx)
        fnames = [f for f in os.listdir(soldirname) if re.match(test, f)]
        for fname in fnames:
            with io.open(soldirname + '/' + fname) as f:
                j = json.loads(f.read())
                if ('resemblance' in j) and j['resemblance'] == 1:
                    return True
                #print(j)
        return False
    except:
        return False
    
    
def getAllSolved():
    test = re.compile(r'solution_(\d+)_(.*)\.out\.response')
    fnames = [f for f in os.listdir(soldirname) if re.match(test, f)]
    
    
    print(fnames)

#kVersion = '_defiler_1'
kBorderVersion = 1
kBorderSubversion = 1


def ensureInd(idx):
    fname = probdirname + '/%d.ind' % idx
    if os.path.exists(fname):
        return
    infname = probdirname + '/%d.in' % idx
    with io.open(infname) as f:
            
        def getint():
            return int(f.readline())
        
        def getpt(s):
            s = s.split(',')                
            return (parseNum(s[0]), parseNum(s[1]))
        
        def readpoly():
            n = getint()
            return Poly([getpt(f.readline()) for _ in range(n)])
        
        allpts = set()
        
        def readedge():
            t = list(map(getpt, f.readline().split()))
            allpts.update(t)
            return Edge(t[0], t[1])
                
            
        n_polys = getint()
        _polys = [readpoly() for _ in range(n_polys)]
        n_edges = getint()
            
        edges = [readedge() for _ in range(n_edges)]
        allpts = sorted(list(allpts))            
        p0 = allpts[0]
        
                
    with io.open(fname, 'wt') as f:
        f.write('%d\n' % len(allpts))
        for p in allpts:
            t = transp(p, p0)
            f.write('%.15f %.15f\n' % (t[0], t[1]))
            
        xedges = splitEdges(allpts, edges)
        
        f.write('%d\n' % len(xedges))
        for e in xedges:
            u, v = allpts.index(e.a), allpts.index(e.b)            
            f.write('%d %d\n' % (u, v))

def runBorder(idx):
    metafname = probdirname + '/%d.pm%d' % (idx, kBorderVersion)
    pfname = probdirname + '/%d.p%d' % (idx, kBorderVersion)
    dfname = probdirname + '/%d.ind' % idx
    if os.path.exists(pfname):
        return True
    if os.path.exists(metafname):
        print('Found %s' % metafname)
        return False
    args = ['../bordersearcher/bordersearcher', '-in', dfname, '-out', pfname, '-t', '20']
    print(' '.join(args))
    try:
        code = subprocess.call(args, timeout=22)
    except subprocess.TimeoutExpired:
        code = -66
    #out = subprocess.check_output(args)
    #code = 0
    if code == 0:
        if not os.path.exists(pfname):
            code = -42
    else:
        if os.path.exists(pfname):
            os.remove(pfname)
    
    logEvent(idx, 'BorderSearcher returned %d' % code)
    with io.open(metafname, 'wt') as meta:
        data = {'code' : code, 'subver' : kBorderSubversion} 
        meta.write(json.dumps(data))
    return code == 0    
    

def logEvent(task, s):
    with io.open('solver.log', 'a') as f:
        ss = '%s: Task %d: %s' % (str(datetime.datetime.now().time()), task, s)
        print(ss)
        f.write(ss + '\n')        
        
def logSolved(task):
    with io.open('solved.log', 'a') as f:
        ss = '%s: Task %d solved!' % (str(datetime.datetime.now().time()), task)
        print(ss)
        f.write(ss + '\n')

def do_send(idx):
    resp = icfp_api.send_solution_logged(idx, facets.getSolName(idx))
    logEvent(idx, 'Response: %s' % resp)
    if checkOk(idx):
        logSolved(idx)


def hasBeenTried(idx):
    metafname = probdirname + '/%d.pm%d' % (idx, kBorderVersion)
    pfname = probdirname + '/%d.p%d' % (idx, kBorderVersion)
    if os.path.exists(metafname) or os.path.exists(pfname):
        return True
    return False

def trySolve(idx, send):
    if checkOk(idx):
        print('%d is already solved' % idx)
        return True
    
    respfile = facets.getSolName(idx) + '.response'
    if os.path.exists(respfile):
        print('found response file %s. Skip' % respfile)
        return True
    
    ensureInd(idx)
    if not runBorder(idx):
        return False
    try:
        if facets.test(idx, kBorderVersion):
            solname = facets.getSolName(idx)
            print(solname)
            if os.path.exists(solname):
                if send:
                    do_send(idx)
                else:
                    print('Not sending')                
            else:
                logEvent(idx, 'returned True, but no solution file')
                return False
            
    except facets.ESolverFailure as sf:
        logEvent(idx, sf.msg)
    except Exception:
        logEvent(idx, traceback.format_exc())
    return True

def problemExists(idx):
    infname = probdirname + '/%d.in' % idx    
    return os.path.exists(infname)

def trySolveIfExists(idx, send=False):    
    if not problemExists(idx):
        print('%d does not exist' % idx)
        return False
    return trySolve(idx, send)

def isFailedInd(idx):
    if not problemExists(idx):
        return False
    ind_name = probdirname + '/%d.ind' % idx
    if not os.path.exists(ind_name):
        metafname = probdirname + '/%d.pm%d' % (idx, kBorderVersion)
        pfname = probdirname + '/%d.p%d' % (idx, kBorderVersion)
        if os.path.exists(metafname):
            os.remove(metafname)
        if os.path.exists(pfname):
            os.remove(pfname)
        return True
    return False        
        
def updateInd():
    #for idx in range(589, 590):
    for idx in range(3417, 6000):
        if isFailedInd(idx):
            print(" ========== %d ========= " % idx)
            trySolve(idx, True)
            
def isBSCode(idx, code):
    metafname = probdirname + '/%d.pm%d' % (idx, kBorderVersion)
    if not os.path.exists(metafname):
        return False
    with io.open(metafname) as f:
        data = json.loads(f.read())
    return data['code'] == code

def killBSMeta(idx):
    metafname = probdirname + '/%d.pm%d' % (idx, kBorderVersion)
    if os.path.exists(metafname):
        os.remove(metafname)    


def update():
    for idx in range(1, 6000):
        if problemExists(idx) and not hasBeenTried(idx) and not checkOk(idx):
            print(" ========== %d ========= " % idx)
            trySolve(idx, True)
    print('Done!')
                

def main():
    #trySolveIfExists(372)
    #return
    #ids = [i for i in range(5000) if isBSCode(i, 3)]
    #for idx in ids:
    #    killBSMeta(idx)
    #return
    
    #print(len(ids))
    #return
    print(getAllSolved())
    
    #update()
    #updateInd()
    return
    
    #for idx in range(788, 1500):
    #for idx in range(102, 500):
    for idx in range(1500, 3600):
        print(" ========== %d ========= " % idx)
        trySolveIfExists(idx, True)

if __name__ == '__main__':
    main()
    
    
