'''
Created on Aug 5, 2016

@author: linesprower
'''

'''
Created on Jul 10, 2016

@author: linesprower
'''

from PyQt4 import QtGui, QtCore
import json, sys, copy, os, re
import io#, time
#import re
import common as cmn

from facets import Edge, transp, splitEdges
import fractions


class TileWidget(QtGui.QWidget):

    
    def __init__(self, owner):
        self.owner = owner
        self.has_data = False
        QtGui.QWidget.__init__(self)
        
        
    def load(self, fname):
        with io.open(fname) as f:
            data = json.loads(f.read())
            self.v = data['v']
            self.e = data['e']    
            self.has_data = True
            #print(self.polys[0].pts)
        
            
        allpts2 = self.v
        
        self.minx0 = min([a[0] for a in allpts2])
        self.maxx0 = max([a[0] for a in allpts2])
        self.miny0 = min([a[1] for a in allpts2])
        self.maxy0 = max([a[1] for a in allpts2])
    
    def mousePressEvent(self, ev):
        '''
        x = ev.x()
        y = ev.y()
        '''
        pass
    
    def transform(self, p):
        x, y = p
        rx = self.x0 + (self.x1 - self.x0) * (x - self.minx) / (self.maxx - self.minx)
        ry = self.y0 + (self.y1 - self.y0) * (y - self.miny) / (self.maxy - self.miny)
        ry = self.height() - ry
        return QtCore.QPointF(rx, ry)

    def paintEvent(self, ev):
        if not self.has_data:
            return
        
        border = 10
        self.x0 = border
        self.x1 = self.width() - border
        self.y0 = border
        self.y1 = self.height() - border
        
        self.minx = self.minx0
        self.miny = self.miny0
        self.maxx = self.maxx0
        self.maxy = self.maxy0
        t = (self.x1 - self.x0) / (self.y1 - self.y0) * (self.maxy - self.miny)
        if t > self.maxx - self.minx:
            t = (t - self.maxx + self.minx) / 2
            self.minx -= t
            self.maxx += t
        else:
            t = (self.y1 - self.y0) / (self.x1 - self.x0) * (self.maxx - self.minx)
            t = (t - self.maxy + self.miny) / 2
            self.miny -= t
            self.maxy += t
        
        p = QtGui.QPainter(self)
            
        # edgges
        p.setPen(QtGui.QColor('black'))
        p.setBrush(QtCore.Qt.NoBrush)
        for e in self.e:
            a = self.v[e[0]]
            b = self.v[e[1]]
            p.drawLine(self.transform(a), self.transform(b))
            
        p.setPen(QtGui.QColor('blue'))
        for i, pp in enumerate(self.v):
            a = self.transform(pp)
            #p.drawText(a, str(i))
            p.drawText(int(a.x() + 4), int(a.y() + 4), str(i))
            

class MoveViewer(QtGui.QMainWindow):

    def __init__(self, arg):
        QtGui.QMainWindow.__init__(self)
        
        self.resize(800, 600)
        self.setWindowTitle('Origami')

        s = QtCore.QSettings('PlatBox', 'Hal0')
        t = s.value("origami2/geometry")
        if t:
            self.restoreGeometry(t)
        t = s.value("origami2/dockstate")
        if t:
            self.restoreState(t, 0)

        #self.data_edit = QtGui.QComboBox()
        #self.data_edit.addItems(['Task %d' % (i+1) for i in range(101)])
        #self.data_edit.currentIndexChanged.connect(self.loadFile)
        self.actr = cmn.Action(self, 'Refrest', None, self.doRefresh, 'F5')
        self.addAction(self.actr)
                
        self.mview = TileWidget(self)
        self.loadFile('facets.json')
                
        layout = cmn.VBox([
                           #self.data_edit,
                           self.mview
                           ])
                
        self.setCentralWidget(cmn.ensureWidget(layout))
        self.statusBar().showMessage('Ready')
        self.show()        
        
    def loadFile(self, fname):
        self.mview.load(fname)
        self.mview.update()   
        
    def doRefresh(self):
        self.loadFile('facets.json')
        print('R!')           
            
        
    def closeEvent(self, event):
        s = QtCore.QSettings('PlatBox', 'Hal0')
        s.setValue("origami2/geometry", self.saveGeometry())
        s.setValue('origami2/dockstate', self.saveState(0))           
            

def main():    
    app = QtGui.QApplication(sys.argv)
    fname = ''
    if len(sys.argv) > 1:
        fname = sys.argv[1]
    _ = MoveViewer(fname)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()