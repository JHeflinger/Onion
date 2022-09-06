from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import onion

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.files = []
        self.setWindowTitle("LIHKT")
        self.resize(QSize(900, 500))
        self._createActions()
        self._connectActions()
        self._createMenuBar()
        self._createShortCuts()
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)
        self.show()
    
    def _createActions(self):
        self.newFileAction = QAction("&New File", self)
        self.openAction = QAction("&Open (ctrl+o)", self)
        self.saveAction = QAction("&Save (ctrl+s)", self)
        self.saveAsAction = QAction("&Save As", self)
        self.shellAction = QAction("&Shell (alt+s)", self)
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.shellAction)

    def _connectActions(self):
        self.openAction.triggered.connect(self.openFile)
        #self.importThemesAction.triggered.connect(self.close)
        #self.importElementsAction.triggered.connect(self.copyContent)
        self.saveAction.triggered.connect(self.save)
        #self.saveAsAction.triggered.connect(self.cutContent)
        self.shellAction.triggered.connect(self.openShell)
      
    def _createShortCuts(self):
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_save.activated.connect(self.save)
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.openFile)
        self.shortcut_shell = QShortcut(QKeySequence('Alt+S'), self)
        self.shortcut_shell.activated.connect(self.openShell)
      
    def save(self):
        self.tabs.currentWidget().save()
        
    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\',"Onion Supported Files (*.txt *.py)")
        if fname[0] != "":
            self.files.append(fname)
            file_content = onion.GetFileContent(fname[0])
            self.tabs.addTab(EditorWindow(file_content, fname[0]), fname[0].split("/")[len(fname[0].split("/")) - 1])
            
    def openShell(self):
        dlg = ShellDialog()
        if dlg.exec():
            try:
                exec(dlg.shellBox.toPlainText())
            except:
                dlg2 = notifyDialog("ERROR IN EXECUTING SCRIPT")
                dlg2.exec()

class notifyDialog(QDialog):
    def __init__(self, msg):
        super().__init__()
        self.setWindowTitle("Notification")
        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.layout = QVBoxLayout()
        message = QLabel(msg)
        self.layout.addWidget(message)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class ShellDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Shell")
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        title = QLabel("Enter Script:")
        self.shellBox = QTextEdit("")
        self.layout.addWidget(title)
        self.layout.addWidget(self.shellBox)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class EditorWindow(QPlainTextEdit):
    def __init__(self, txt, filename):
        super().__init__(txt)
        self.filename = filename
        self.saved = False
        
        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.setFont(fixedfont)
        
    def save(self):
        self.saved = onion.SaveFile(self.saved, self.toPlainText(), self.filename) 