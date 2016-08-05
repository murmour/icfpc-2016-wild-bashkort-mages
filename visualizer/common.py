# coding: utf-8
'''
Created on 19.02.2013

@author: LinesPrower
'''
from PyQt4 import QtGui, QtCore
import os
import sys
import copy
import pickle
import io
import itertools
from datetime import datetime
import urllib.parse
import re
import types

_con_printer = None
_glw = None
_main_window = None

_realfile = os.path.realpath(__file__)
_rootdir = os.path.realpath(os.path.join(os.path.dirname(_realfile), '..'))

DEBUG_BUILD = True
#DEBUG_BUILD = False

class SC:
    def __init__(self, s):
        self.s = s        

_system_shortcuts = {} # str -> QAction

class Box:
    def __init__(self, val=None):
        self.val = val

def setConPrinter(f):
    global _con_printer
    _con_printer = f

def setGLW(glw):
    global _glw
    _glw =  glw

def getGLW():
    return _glw

def setMainWindow(w):
    global _main_window
    _main_window = w
    
def mainWindow():
    return _main_window

def getUndoer():
    return _main_window.undoer

def setStatus(s):
    if mainWindow():
        mainWindow().statusBar().showMessage(s, 5000)

def getPixelSize():
    if not _glw:
        return None
    ci = _glw.getCameraInfo()
    if not ci:
        return None
    return ci.scale / _glw.vport[3]

def getDefaultObjData(ident):
    fields = mainWindow().obj_creator.descrs[ident].fields
    data = {}
    for fld in fields:    
        if fld.mode == 1:#kUserDefined:
            data[fld.name] = fld.userval
        else:
            data[fld.name] = fld.initval
    return data    

def getIdByName(name):
    for ident, d in mainWindow().obj_creator.descrs.items():
        if d.name == name:
            return ident
    raise Exception('Unknown object name: ' % name)
    
def getObjDescription(ident):
    if ident in mainWindow().obj_creator.descrs:
        return mainWindow().obj_creator.descrs[ident]
    return None

def cprint(s):
    print(s)
    if (_con_printer):
        _con_printer(s)

def flatten(l):
    return [item for sublist in l for item in sublist]

def pairs(seq):
    return zip(seq, itertools.islice(seq, 1, None))

def iriToUri(iri):
    url = urllib.parse.urlsplit(iri)
    url = list(url)
    #print(url)
    for i in range(2, len(url)):        
        url[i] = urllib.parse.quote(url[i])
    return urllib.parse.urlunsplit(url)

def isoNow():
    """
    returns current time in ISO format
    """
    return datetime.now().isoformat()

def parseISODate(s):
    if len(s) == 10:
        return datetime.strptime( s, "%Y-%m-%d" )
    elif len(s) == 19: # if the .%f part is zero, isoformat() omits it
        return datetime.strptime( s, "%Y-%m-%dT%H:%M:%S" )
    else:
        return datetime.strptime( s, "%Y-%m-%dT%H:%M:%S.%f" )

def getFilterRegex(s):
    """
    result can be an empty string, in this case
    no filter should be applied
    """
    s = s.split()
    if not s:
        return ''
    
    def escape(s):
        return s.replace('+', '\\+').replace('*', '\\*')
                
    return '.*' +  '.+'.join([escape(x) for x in s]) + '.*'

def describeTimeSpan(cur_date, past_date) -> str:
    d = parseISODate(cur_date) - parseISODate(past_date)
    if d.days < 0:
        return "future"
    
    def f(num, unit):
        if num == 1:
            return '1 ' + unit
        else:
            return '%d %ss' % (num, unit) 
    
    mins = (d.days * 86400 + d.seconds) // 60
    if mins < 60:
        return f(mins, 'min')
    hours = mins // 60
    if hours < 24:
        return f(hours, 'hour')
    days = hours // 24
    if days < 31:
        return f(days, 'day')
    return f(days // 30, 'month')    

def safeUnzip(x):
    return ([t[0] for t in x], [t[1] for t in x])

def arr2d(n, m, initval):
    """
    returns a 2d array of size n by m with each element equal to initval 
    """
    return [ [copy.copy(initval) for _ in range(m) ] for _ in range(n) ]

def split_suffix(s, sep):
    t = s.split(sep)
    if len(t) > 1:
        return ''.join(t[:-1]), t[-1]
    return s, ''
        
def xstr(s):
    """
    returns an empty string if s is None, otherwise returns
    the string representation of s
    """
    if s == None:
        return ''
    return str(s)

def nonefy(s):
    """
    returns None if s is an empty string, otherwise returns s
    """
    if s == '':
        return None
    return s

def allF(lst, f):
    """
    return True if all elements of lst satisfy f
    """
    for x in lst:
        if not f(x):
            return False
    return True

def anyF(lst, f):
    """
    return True if at least one element of lst satisfies f
    """
    for x in lst:
        if f(x):
            return True
    return False

def idxm1(lst, val):
    """
    returns the index of the first occurrence of val in lst
    returns -1 if val is not in lst
    """
    for i, x in enumerate(lst):
        if x == val:
            return i
    return -1

def idxF(lst, f):
    """
    returns the index of first element of lst which satisfies f
    returns None if there's no such element
    """
    for i, x in enumerate(lst):
        if f(x):
            return i
    return None

def idxL(lst, f):
    """
    returns the index of last element of lst which satisfies f
    returns None if there's no such element
    """
    res = None
    for i, x in enumerate(lst):
        if f(x):
            res = i
    return res

def findF(lst, f):
    """
    returns first element of lst which satisfies f
    returns None if there's no such element
    """
    for x in lst:
        if f(x):
            return x
    return None

def findL(lst, f):
    """
    returns last element of lst which satisfies f
    returns None if there's no such element
    """
    res = None
    for x in lst:
        if f(x):
            res = x
    return res

def chainLists(a):
    return list(itertools.chain.from_iterable(a))

def checkIsect(a, b, c, d):
    """
    returns True if ranges [a, b) and [c, d) strictly intersect
    """    
    return max(a, c) < min(b, d)

def isectRanges(a, b, c, d):
    """
    returns the intersection of ranges [a, b) and [c, d)
    """
    return (max(a, c), min(b, d))

def splitRange(a, b, c, d) -> [(int, int)]:
    """
    splits range [a, b) using range [c, d)
    if [a, b) splits into two or more ranges, returns the list of them
    otherwise, return None
    """
    if not checkIsect(a, b, c, d) or isectRanges(a, b, c, d) == (a, b):
        return None
    res = []
    if a < c:
        res.append((a, c))
    res.append(isectRanges(a, b, c, d))
    if d < b:
        res.append((d, b))
    return res

def truncateStr(s, maxlen):
    if len(s) > maxlen:
        return s[:maxlen - 1] + '…'
    return s

def startsWithAny(s, lst):
    """
    returns true if string s starts with any of strings from lst
    """
    return anyF(lst, lambda x: s.startswith(x))

kTopAlign = 1
kBottomAlign = 2

def VBox(items, margin = 0, spacing = 5, align = None, stretch = None):
    box = QtGui.QVBoxLayout()
    box.setMargin(margin)
    box.setSpacing(spacing)
    if stretch == None:
        stretch = [0] * len(items)
    else:
        assert(len(stretch) == len(items))
    if align == kBottomAlign:
        box.setAlignment(QtCore.Qt.AlignBottom)
    elif align == kTopAlign:
        box.setAlignment(QtCore.Qt.AlignTop)
    for x, st in zip(items, stretch):
        if isinstance(x, QtGui.QLayout):
            box.addLayout(x, st)
        else:
            box.addWidget(x, st)
    return box

kLeftAlign = 1
kRightAlign = 2

def HBox(items, margin = 0, spacing = 5, align = None, stretch = None):
    box = QtGui.QHBoxLayout()
    box.setMargin(margin)
    box.setSpacing(spacing)
    if stretch == None:
        stretch = [0] * len(items)
    else:
        assert(len(stretch) == len(items))
    if align == kRightAlign:
        box.setAlignment(QtCore.Qt.AlignRight)
    elif align == kLeftAlign:
        box.setAlignment(QtCore.Qt.AlignLeft)    
    for x, st in zip(items, stretch):
        if isinstance(x, QtGui.QLayout):
            box.addLayout(x, st)
        elif isinstance(x, QtGui.QSpacerItem):            
            box.addSpacerItem(x)
        else:
            box.addWidget(x, st)    
    return box

icons_cache = {}

def GetIcon(fname):
    if not fname:
        fname = ''
    #else:
    #    fname = _rootdir + '/' + fname
    if fname not in icons_cache:
        icons_cache[fname] = QtGui.QIcon(fname)
    return icons_cache[fname] 

def Action(owner, descr, icon, handler = None, shortcut = None, 
           statustip = None, enabled = True, checkable = False,
           checked = None, *, bold = False):
    act = QtGui.QAction(GetIcon(icon), descr, owner)
    act.setIconVisibleInMenu(True)
    
    if bold:
        f = act.font()
        f.setBold(True)
        act.setFont(f)
            
    if shortcut.__class__.__name__ == 'SC':
        act.setShortcut(shortcut.s)
        _system_shortcuts[shortcut.s] = act
    elif not (shortcut is None):
        act.setShortcut(shortcut)
        
    if not (statustip is None):
        act.setStatusTip(statustip)
    if not (handler is None):
        act.triggered.connect(handler)
    act.setEnabled(enabled)
    if checkable:
        act.setCheckable(True)
    if checked != None:
        act.setCheckable(True)
        act.setChecked(checked)
    return act

def Separator(owner):
    res = QtGui.QAction(owner)
    res.setSeparator(True)
    return res

class Grid(QtGui.QTableWidget):
    
    def __init__(self, col_names, widths = None):
        super(Grid, self).__init__(0, len(col_names))
        self.setHorizontalHeaderLabels(col_names)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        if widths:
            self.load(widths)
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return:
            #print('!')
            #if self.currentItem():
            #    self.editItem(self.currentItem())
            return
        return QtGui.QTableWidget.keyPressEvent(self, event)
        
    def load(self, widths):
        for i, w in enumerate(widths):
            self.setColumnWidth(i, w)
    
    def save(self):        
        return [self.columnWidth(i) for i in range(self.columnCount())]
    
    def setRowData(self, row, data, editable=True):
        for j in range(self.columnCount()):                    
            tmp = QtGui.QTableWidgetItem(data[j])
            if not editable:
                tmp.setFlags(tmp.flags() ^ QtCore.Qt.ItemIsEditable)                
            self.setItem(row, j, tmp)
    
    def setTableData(self, data, editable=True, fix_height=None):        
        self.setRowCount(len(data))        
        for i, x in enumerate(data):
            self.setRowData(i, x, editable)
        if fix_height == None:              
            self.resizeRowsToContents()
        else:
            for i in range(len(data)):
                self.setRowHeight(i, fix_height)

class Table(QtGui.QGridLayout):
    
    def __init__(self, items, margin = 0):
        """
        items: [(string, widget)]
        """
        QtGui.QGridLayout.__init__(self)
        self.setMargin(margin)
        for (i, (s, item)) in enumerate(items):
            lbl = QtGui.QLabel(s)
            lbl.setMinimumHeight(20)
            self.addWidget(lbl, i, 0, QtCore.Qt.AlignTop)
            self.addWidget(ensureWidget(item), i, 1)
            self.setAlignment(lbl, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

class ComboBox(QtGui.QComboBox):
    
    def __init__(self, lst = None):
        """
        lst should be a list of tuples (id, string)
        id's can be set or get by calling setDbId/getDbId
        strings are displayed in the combobox        
        """
        super(ComboBox, self).__init__()
        if lst:
            self.updateList(lst)
    
    def updateList(self, lst):
        self.clear()
        self.ids, self.strings = zip(*lst)
        self.addItems(self.strings)
    
    def setDbId(self, dbid):
        self.setCurrentIndex( self.ids.index(dbid) )
        
    def getDbId(self) -> int:
        return self.ids[ self.currentIndex() ]
    
    def setText(self, s):
        """
        if s is not among strings, current index becomes -1
        """
        self.setCurrentIndex(idxm1(self.strings, s))        

def VSplitter(items):
    res = QtGui.QSplitter(QtCore.Qt.Vertical)    
    for x in items:
        res.addWidget(ensureWidget(x))
    return res

def HSplitter(items):
    res = QtGui.QSplitter(QtCore.Qt.Horizontal)    
    for x in items:
        res.addWidget(ensureWidget(x))
    return res

def ToolBar(actions):
    res = QtGui.QToolBar()
    res.setStyleSheet("QToolBar { border: 0px }")
    for x in actions:
        if x:
            if x.__class__.__name__ == 'QAction':
                res.addAction(x)
            else:
                res.addWidget(x)
        else:
            res.addSeparator()
    return res

def ToolBtn(action):
    res = QtGui.QToolButton()
    res.setDefaultAction(action)
    res.setAutoRaise(True)
    return res

def ToolBtnStack(actions):
    items = [ToolBtn(a) for a in actions]
    return HBox(items, spacing=0, align=kLeftAlign)

def Button(caption, handler, *, enabled=True, autodefault=True):
    btn = QtGui.QPushButton(caption)
    btn.setAutoDefault(autodefault)
    btn.clicked.connect(handler)
    btn.setEnabled(enabled)
    return btn

def ensureLayout(widget):
    if isinstance(widget, QtGui.QWidget):
        return VBox([widget])
    return widget
        
def ensureWidget(layout):
    if isinstance(layout, QtGui.QWidget):
        return layout
    tmp = QtGui.QWidget()
    tmp.setLayout(layout)
    return tmp

def msgWarn(widget, s):
    QtGui.QMessageBox.warning(widget, 'PlatBox', s)


def question(msg, owner = None) -> bool:
    if owner == None:
        owner = mainWindow()    
    t = QtGui.QMessageBox.question(None, 'PlatBox', msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
    return t == QtGui.QMessageBox.Yes
    
class Dialog(QtGui.QDialog):
    
    def __init__(self, appname, wndname, title, is_modal=True):
        """
        appname [string]: application name (for saving settings)
        wndname [string]: window name (for saving settings)
        title [string]: window title
        """
        QtGui.QDialog.__init__(self)
        self.appname = appname
        self.wndname = wndname
        self.is_modal = is_modal
        self.setWindowTitle(title)        
        self.setWindowIcon(QtGui.QIcon(_rootdir + '/platbox.ico'))
        self.state_saver = StateSaver(wndname, appname)
        self.old_cur_wnd = None
    
    # to ensure that settings are saved after OK is clicked 
    def done(self, code):
        QtGui.QDialog.done(self, code)
        self.close()
    
    def setCustomLayout(self, layout, has_statusbar, menu = None):
        if has_statusbar:
            self.sbar = QtGui.QStatusBar()
            layout.setContentsMargins(10, 10, 10, 0)
            layout = VBox([layout, self.sbar], spacing = 0, stretch = [1, 0])

        layout = ensureLayout(layout)
        if menu:
            layout.setMenuBar(menu)                 
        self.setLayout(layout)
        self.loadSettings()        
                 
    def setDialogLayout(self, layout, ok_handler, has_statusbar = True, 
                        close_btn = False, *, 
                        extra_buttons = None, 
                        autodefault = True,
                        menu = None):
        """
        extra_buttons should be an iterable of tuples (caption, handler)
        """
        buttons = []
        if extra_buttons:
            buttons.extend([Button(capt, handler, autodefault=autodefault) 
                            for capt, handler in extra_buttons])

        if close_btn:
            buttons.extend([Button('Close', self.reject, autodefault=autodefault)])
        else:
            buttons.extend([Button('&OK', ok_handler, autodefault=autodefault),
                            Button('Cancel', self.reject, autodefault=autodefault)])
            self.addAction(Action(self, 'OK', '', ok_handler, 'F5'))
        
        buttons = HBox(buttons, align = kRightAlign)
        box = VBox([layout, buttons], 10)
        
        self.setCustomLayout(box, has_statusbar, menu)        

    def loadSettings(self):
        s = QtCore.QSettings('PlatBox', self.appname)
        t = s.value("%s/geometry" % self.wndname)
        if t:
            self.restoreGeometry(t)
        self.state_saver.load()
    
    def closeEvent(self, event):
        s = QtCore.QSettings('PlatBox', self.appname)        
        s.setValue("%s/geometry" % self.wndname, self.saveGeometry())
        self.state_saver.save()
        
    def registerStateObj(self, name, obj):
        self.state_saver.register(name, obj)

class SaveStateWrapper:
    """
    This class wraps an object having saveState / restoreState methods
    so it can be registered with StateSaver
    """    
    def __init__(self, base):
        self.base = base
    
    def load(self, state):
        self.base.restoreState(state)
        
    def save(self):
        return self.base.saveState()
        

class StateSaver:
    def __init__(self, wndname, appname = 'PlatBox'):
        self.wndname = wndname
        self.appname = appname
        self.objs = []
        
    def load(self):
        if not self.objs:
            return
        s = QtCore.QSettings('PlatBox', self.appname)
        for name, obj in self.objs:
            t = s.value('%s/%s' % (self.wndname, name))
            if t != None:
                obj.load(pickle.loads(t))
                
    def save(self):
        if not self.objs:
            return
        s = QtCore.QSettings('PlatBox', self.appname)
        for name, obj in self.objs:
            s.setValue('%s/%s' % (self.wndname, name), pickle.dumps(obj.save()))
            
    def register(self, name, obj):
        self.objs.append((name, obj))
        

# returns (HBox, QLineEdit)
def createSearchBox(handler, owner, shortcut, completer_model = None,
                    invisible = False):
    """
    returns (layout, QLineEdit)
    """
    edit = QtGui.QLineEdit()
    edit.setFont(QtGui.QFont('Consolas'))    
    if shortcut:
        def sf_handler():
            edit.setVisible(True)
            btn.setVisible(True)
            owner.raise_()
            edit.setFocus()
            edit.selectAll()
        
        edit.setPlaceholderText('Press %s to focus...' % shortcut) 
        owner.addAction(Action(owner, 'Activate', '', sf_handler, shortcut))
    edit.returnPressed.connect(handler) 
    btn = ToolBtn(Action(owner, 'Search', 'data/magnifier.png', handler))
    
    if invisible:
        edit.setVisible(False)
        btn.setVisible(False)
    hbox = HBox([edit, btn], 0, 0)    
    
    if completer_model:
        compl = QtGui.QCompleter()
        compl.setModel(completer_model)
        compl.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        edit.setCompleter(compl)
        edit.textEdited.connect(completer_model.setPrefix)
        
    return (hbox, edit)

def ensureDir(fname):
    """
    creates all needed directories for file fname
    """
    d = os.path.dirname(fname)
    if not os.path.exists(d):
        os.makedirs(d)
        
def arrToRanges(a) -> [(int, int)]:
    """
    a must be an array of sorted unique integers
    """
    res = []
    st = None
    last = None
    for x in a:
        if st == None:
            st = x
            last = x
        elif last + 1 == x:
            last = x
        else:
            res.append((st, last))
            st = x
            last = x
    if st != None:
        res.append((st, last))
    return res

def eventToNum(event):
    """
    return a number (0-9) for keys 1..9, 0
    otherwise, returns None
    event should be QKeyEvent
    """
    if event.key() >= QtCore.Qt.Key_1 and event.key() <= QtCore.Qt.Key_9:
        return event.key() - QtCore.Qt.Key_1
    if event.key() == QtCore.Qt.Key_0:
        return 9
    return None

def showReport(title, text, only_close_button = True, modal=True):
    class ReportDialog(Dialog):
        def __init__(self, title, text):
            Dialog.__init__(self, 'PlatBox', 'report_wnd', title)
            e = QtGui.QTextEdit()
            e.setFont(QtGui.QFont('Consolas', 10))
            e.setReadOnly(True)
            e.setPlainText(text)
            self.setDialogLayout(e, 
                                 lambda: self.accept(), 
                                 has_statusbar = False, 
                                 close_btn = only_close_button)        
    
    d = ReportDialog(title, text)
    if modal:
        return d.exec_()
    else:
        d.show()
        return d # keep this reference to prevent garbage collection!

class Text:
    def __init__(self, dbid, name, authorid, categoryid, year, comment):
        """
        year is string
        """
        self.dbid = dbid
        self.name = name
        self.authorid = authorid
        self.categoryid = categoryid
        self.year = str(year) if year != None else ''
        self.comment = comment
        
class RtfEditor(QtGui.QPlainTextEdit):
    
    def __init__(self):
        super(RtfEditor, self).__init__()
        self.addAction(Action(self, 'Italic', '', self.rtfItalic, 'Ctrl+I'))
        self.addAction(Action(self, 'Bold', '', self.rtfBold, 'Ctrl+B'))
        self.addAction(Action(self, 'Hyperlink', '', self.rtfHRef, 'Ctrl+H'))
        self.addAction(Action(self, 'Underline', '', self.rtfUnderline, 'Ctrl+U'))
        self.addAction(Action(self, 'LineBreak', '', self.rtfLineBreak, 'Ctrl+N'))
        self.setTabChangesFocus(True)
    
    def rtfExtend(self, f, k):
        cur = self.textCursor()
        a, b = cur.selectionStart(), cur.selectionEnd()
        s = f(cur.selectedText())
        cur.insertText(s)
        cur.setPosition(a + k)
        cur.setPosition(b + k, QtGui.QTextCursor.KeepAnchor)        
        self.setTextCursor(cur)
    
    def rtfItalic(self):
        self.rtfExtend(lambda s: '<i>%s</i>' % s, 3)
        
    def rtfBold(self):
        self.rtfExtend(lambda s: '<b>%s</b>' % s, 3)
        
    def rtfUnderline(self):
        self.rtfExtend(lambda s: '<u>%s</u>' % s, 3)
    
    def rtfLineBreak(self):
        self.rtfExtend(lambda s: '<br>', 4)
        
    def rtfHRef(self):
        self.rtfExtend(lambda s: '<a href="">%s</a>' % s, 11)


def splitAtSymbols(s, seps):
    res = []
    cur = []
    for c in s:
        if c in seps:
            if cur: res.append(''.join(cur))
            res.append(c)
            cur = []
        else:
            cur.append(c)
    if cur: res.append(''.join(cur))
    return res    

def printcon(s):
    s2 = (s.__str__() + '\n').encode('utf-8')
    sys.stdout.buffer.write(s2)
    
def checkYear(s):
    if s == '':
        return True
    try:
        i = int(s)
    except:
        return False
    return 1000 <= i <= 2100

    
def getOpenFileName(owner, ident, title, filters, save=False):
    ident = 'openfile_' + ident
    s = QtCore.QSettings('PlatBox', 'PlatBox')
    path = s.value(ident, defaultValue='')
    if save:
        opts = QtGui.QFileDialog.DontConfirmOverwrite if save == 1 else 0
        fname = QtGui.QFileDialog.getSaveFileName(None, title, path, filters, opts)
    else:
        fname = QtGui.QFileDialog.getOpenFileName(None, title, path, filters)
    if fname:
        path = os.path.dirname(fname)
        s.setValue(ident, path)        
    return fname

class EncodingDialog(Dialog):
    def __init__(self):
        Dialog.__init__(self, 'PlatBox', 'enc_select', 'Select Encoding')
        self.res = None
        f = io.open('data/encodings.txt', encoding = 'utf-8')
        self.data = [x.split('\t') for x in f.read().split('\n')]
        f.close()
        self.cbox = QtGui.QComboBox()
        self.cbox.addItems(['%s (%s)' % (x[0], x[2]) for x in self.data])
        self.setDialogLayout(VBox([self.cbox], align=kTopAlign),
                             self.doOk, False)
        
    def doOk(self):
        self.res = self.data[self.cbox.currentIndex()][0]
        self.accept()
 
def selectEncoding():
    w = EncodingDialog()
    w.exec_()
    return w.res

class ParametersInput(Table):
    
    FLOAT = 1
    BOOL  = 2
    LIST  = 3
    STR   = 4
    I32   = 5
    
    def __init__(self, params):
        '''
        params: [(name, type [, extra])]
        '''
        def make(data):
            ty = data[1]
            if ty in [self.FLOAT, self.STR, self.I32]:
                return QtGui.QLineEdit()
            if ty == self.BOOL:
                res = QtGui.QComboBox()
                res.addItems(['False', 'True'])
                return res
            if ty == self.LIST:
                res = QtGui.QComboBox()
                res.addItems(data[2])
                return res
            assert(False)
        
        self.pnames = [x[0] for x in params]
        self.ptypes = [x[1] for x in params]
        self.controls = [make(x) for x in params]
        Table.__init__(self, zip(self.pnames, self.controls))
        
    def setValues(self, vals):
        assert(len(vals) == len(self.controls))
        for ty, c, v in zip(self.ptypes, self.controls, vals):
            if ty == self.FLOAT:
                c.setText("%.5f" % v)
            elif ty == self.I32:
                c.setText("%d" % v)
            elif ty == self.BOOL:
                c.setCurrentIndex(1 if v else 0)
            elif ty == self.STR:
                c.setText(v)
            elif ty == self.LIST:
                c.setCurrentIndex(v)
    
    def validate(self):
        for name, ty, c in zip(self.pnames, self.ptypes, self.controls):            
            try:
                if ty == self.FLOAT:
                    t = eval(c.text())
                    float(t)
                if ty == self.I32:
                    t = eval(c.text())
                    t = int(t)
                    if t < -(2 ** 31) or t >= 2 ** 31:
                        raise Exception('out of range')
            except:
                return 'Invalid value for %s' % name
        return ''
    
    def getValues(self):
        def get(ty, c):
            if ty == self.FLOAT:
                return float(eval(c.text()))
            if ty == self.I32:
                return int(eval(c.text()))
            if ty == self.BOOL:
                return c.currentIndex() == 1
            if ty == self.STR:
                return c.text()
            if ty == self.LIST:
                return c.currentIndex()
        
        return [get(ty, c) for ty, c in zip(self.ptypes, self.controls)] 
    

class ParametersDialog(Dialog):
    
    def __init__(self, name, title, data):
        Dialog.__init__(self, 'platboxplus', name, title)
        self.data = data
        self.keys = sorted([x for x in data.keys() if not x.startswith('#')])
        params = [(x, data['#' + x]) for x in self.keys]
        self.params = ParametersInput(params)
        self.params.setValues([data[x] for x in self.keys])
        self.setDialogLayout(self.params, self.doOk)
        
    def doOk(self):
        err = self.params.validate()
        if err:
            self.sbar.showMessage(err)
        else:
            for k, v in zip(self.keys, self.params.getValues()):
                self.data[k] = v            
            self.accept()

def Frame(widget, width = 2):
    """
    Adds a frame around a given widget/layout
    """
    fr = QtGui.QFrame()
    fr.setFrameStyle(QtGui.QFrame.Box | QtGui.QFrame.Plain)
    fr.setLineWidth(width)
    fr.setStyleSheet(".QFrame { color:gray }")    
    fr.setLayout(ensureLayout(widget))    
    widget.cmn_frame = fr
    return fr    

# this is a class decorator to use with classes of widgets
# which are put inside of Frame 
def FrameController(c):
    
    def focusInEvent(self, event):        
        self.cmn_frame.setStyleSheet(".QFrame { color:blue }")
        super(c, self).focusInEvent(event)        
    
    def focusOutEvent(self, event):
        self.cmn_frame.setStyleSheet(".QFrame { color:gray }")        
        super(c, self).focusOutEvent(event)
        
    c.focusInEvent = focusInEvent
    c.focusOutEvent = focusOutEvent
    return c

def QuickFilterBox(handler):
    filter = QtGui.QLineEdit()
    filter.setPlaceholderText('Quick filter')
    filter.textEdited.connect(handler)
    def clf():
        filter.clear()
        handler()
    act_clear_flt = Action(filter, 'Clear', 'icons/cross-small.png', clf)
    res = HBox([filter, ToolBtn(act_clear_flt)], spacing=0)
    def checkStr(self, s):
        p = filter.text()
        if not p:
            return True
        p = re.escape(p)
        return bool(re.search(p, s, re.IGNORECASE))
    res.checkStr = types.MethodType(checkStr, res)
    return res        
    
def unp_cell(cell):
    return cell['x'], cell['y']

def make_cell(x, y):
    return { 'x' : x, 'y' : y }
    
# debug code
def main():
    _ = QtGui.QApplication(sys.argv) 
    w = ParametersDialog('tmp', 'Test Dialog', {'p1' : 100, '#p1' : ParametersInput.FLOAT,
                                                'p2' : False, '#p2' : ParametersInput.BOOL})
    if w.exec_():
        print(w.data)
    #showReport('Test', 'Everything is\nforking awesome!')
    sys.exit(0)

if __name__ == '__main__':
    main()