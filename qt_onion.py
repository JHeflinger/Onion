from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtPrintSupport import *
import os
import sys
import subprocess
import onion

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Onion v0.1.2")
        self.resize(QSize(900, 500))
        self.openfiles = []
        self._createActions()
        self._connectActions()
        self._createMenuBar()
        self._createShortCuts()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)
        self.tabs.currentChanged.connect(self.updateCurrentTab)
        self.setCentralWidget(self.tabs)
        self.console = ConsoleWindow()
        self.pExplorer = ProjectExplorer(self)
        self._setPalette()
        self._startup()
        self.show()
         
    def _setPalette(self):
        #tabs
        stylesheet = """ 
            QTabBar::tab:selected {background: #1E1E40; color: #D4D4D4;}
            QTabBar::tab {background: #3D3D3D; color: #BFBFBF;}
            QTabWidget>QWidget>QWidget{background: #1E1E40; color: #D4D4D4;}
            """
        self.tabs.setStyleSheet(stylesheet)
        #menubar
        stylesheet = """ 
            QMenuBar {background: #292929; color: #D4D4D4;}
            """
        self.menuBar().setStyleSheet(stylesheet)
        #main window
        stylesheet = """ 
            QMainWindow {background: #1F0505;}
            QMainWindow>QWidget {background: black;}
            """
        self.setStyleSheet(stylesheet)
   
    def _startup(self):
        print("startup sequence")
        opened_files = onion.SettingsGet_OPENED()
        selected_tab = onion.SettingsGet_SELECTED()
        for f in opened_files:
            if f != "":
                self.openFileByName(f)
        self.tabs.setCurrentIndex(selected_tab)

    def _createActions(self):
        #file menu actions
        self.newFileAction = QAction("&New File (ctrl+n)", self)
        self.openAction = QAction("&Open (ctrl+o)", self)
        self.openProjectAction = QAction("&Open Project (ctrl+shift+o)", self)
        self.saveAction = QAction("&Save (ctrl+s)", self)
        self.saveAsAction = QAction("&Save As (ctrl+a+s)", self)
        self.shellAction = QAction("&Shell (alt+s)", self)
        self.runAction = QAction("&Run Script(ctrl+r)", self)
        self.runProjectAction = QAction("&Run Project(ctrl+shift+r)", self)
        #settings menu actions
        self.shortcutsAction = QAction("&Shortcuts", self)
        self.projconfigAction = QAction("&Configure Project", self)
        #window menu actions
        self.showconsoleAction = QAction("&Show Console (ctrl+shft+c)", self)
        self.showprojectsAction = QAction("&Show File Explorer (ctrl+shift+p)", self)
    
    def _createMenuBar(self):
        menuBar = self.menuBar()
        #file menu
        fileMenu = menuBar.addMenu("&File")
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.openProjectAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.saveAsAction)
        fileMenu.addSeparator()
        fileMenu.addAction(self.shellAction)
        fileMenu.addAction(self.runAction)
        fileMenu.addAction(self.runProjectAction)
        #settings menu
        settingsMenu = menuBar.addMenu("&Settings")
        settingsMenu.addAction(self.shortcutsAction)	
        settingsMenu.addAction(self.projconfigAction)
        #window menu
        windowsMenu = menuBar.addMenu("&Windows")
        windowsMenu.addAction(self.showconsoleAction)
        windowsMenu.addAction(self.showprojectsAction)

    def _connectActions(self):
        self.openAction.triggered.connect(self.openFile)
        self.openProjectAction.triggered.connect(self.openProject)
        self.saveAction.triggered.connect(self.save)
        self.saveAsAction.triggered.connect(self.saveAs)
        self.shellAction.triggered.connect(self.openShell)
        self.runAction.triggered.connect(self.runScript)
        self.runProjectAction.triggered.connect(self.runProject)
        self.newFileAction.triggered.connect(self.newFile)
        self.showconsoleAction.triggered.connect(self.showConsole)
        self.showprojectsAction.triggered.connect(self.showProjects)
        self.projconfigAction.triggered.connect(self.configProject)
      
    def _createShortCuts(self):
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+S'), self)
        self.shortcut_save.activated.connect(self.save)
        self.shortcut_open = QShortcut(QKeySequence('Ctrl+O'), self)
        self.shortcut_open.activated.connect(self.openFile)
        self.shortcut_shell = QShortcut(QKeySequence('Alt+S'), self)
        self.shortcut_shell.activated.connect(self.openShell)
        self.shortcut_run = QShortcut(QKeySequence('Ctrl+R'), self)
        self.shortcut_run.activated.connect(self.runScript)
        self.shortcut_runproject = QShortcut(QKeySequence('Ctrl+Shift+R'), self)
        self.shortcut_runproject.activated.connect(self.runProject)
        self.shortcut_new = QShortcut(QKeySequence('Ctrl+N'), self)
        self.shortcut_new.activated.connect(self.newFile)
        self.shortcut_saveas = QShortcut(QKeySequence('Ctrl+Shift+S'), self)
        self.shortcut_saveas.activated.connect(self.saveAs)
        self.shortcut_showconsole = QShortcut(QKeySequence('Ctrl+Shift+C'), self)
        self.shortcut_showconsole.activated.connect(self.showConsole)
        self.shortcut_showprojects = QShortcut(QKeySequence('Ctrl+Shift+P'), self)
        self.shortcut_showprojects.activated.connect(self.showProjects)
        self.shortcut_openproject = QShortcut(QKeySequence('Ctrl+Shift+O'), self)
        self.shortcut_openproject.activated.connect(self.openProject)
   
    def closeEvent(self, event):
        unsavedwork = False
        for i in range(self.tabs.count()):
            if self.tabs.widget(i).saved == False:
                unsavedwork = True
        if unsavedwork:
            dlg = ConfirmDialog("You have unsaved work! Would you like to go back and save your work?")
            if dlg.exec():
                event.ignore()
    
    def configProject(self):
        self.console.consoleOutput("configuring Project")
        dlg = ProjectConfigDialog()
        if dlg.exec():
            self.console.consoleOutput("setting new project settings")
            onion.SettingsWrite_PROJLANG(dlg.lang.text())
            onion.SettingsWrite_PROJCONTENT(dlg.content.toPlainText())
            onion.SettingsWrite_PROJDEST(dlg.dest.text())

    def runProject(self):
        self.console.consoleOutput("running project")
        onion.RunProject(self.console)

    def openProject(self):
        print("open!")
        proj = QFileDialog.getExistingDirectory(self, "Open a folder", "/home", QFileDialog.ShowDirsOnly)
        #write and then update project explorer
        onion.SettingsWrite_PROJECT(proj)
        self.pExplorer.updateProj(proj)
      
    def showConsole(self):
        print("show console!")
        self.console.setVisible(True != self.console.isVisible())
        self.addDockWidget(Qt.BottomDockWidgetArea, self.console)

    def showProjects(self):
        self.pExplorer.setVisible(True != self.pExplorer.isVisible())
        self.addDockWidget(Qt.LeftDockWidgetArea, self.pExplorer)

    def updateCurrentTab(self, index):
        print(index)
        onion.SettingsWrite_SELECTED(index)

    def closeTab(self, index):
        print(index)
        readytoclose = True
        if self.tabs.widget(index).saved == False:
            dlg = ConfirmDialog("Warning: You have unsaved work! Are you sure you'd like to continue?")
            readytoclose = dlg.exec()
        if readytoclose:
            print("closing " + self.tabs.widget(index).filename)
            print("removing from ")
            print(self.openfiles)
            self.openfiles.remove(self.tabs.widget(index).filename)
            self.tabs.removeTab(index)
            onion.SettingsWrite_OPENED(self.openfiles)

    def save(self):
        if self.tabs.currentWidget().filename == "":
            self.saveAs()
        else:
            self.tabs.currentWidget().save()

    def saveAs(self):
        self.tabs.currentWidget().saveAs()
        self.openfiles[self.tabs.currentIndex()] = self.tabs.currentWidget().filename
        onion.SettingsWrite_OPENED(self.openfiles)

    def runScript(self):
        self.tabs.currentWidget().runScript(self.console)
        
    def newFile(self):
        print("new file")
        self.tabs.addTab(EditorWindow("", "", self.tabs), "Untitled File")
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.openfiles.append("")
        onion.SettingsWrite_OPENED(self.openfiles)

    def openFile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file')
        if fname[0] != "":
            if self.navigateToFile(fname[0]):
                return
            file_content = onion.GetFileContent(fname[0])
            self.tabs.addTab(EditorWindow(file_content, fname[0], self.tabs), fname[0].split("/")[len(fname[0].split("/")) - 1])
            self.tabs.setCurrentIndex(self.tabs.count() - 1)
            self.openfiles.append(fname[0])
            onion.SettingsWrite_OPENED(self.openfiles)

    def navigateToFile(self, filename):
        if filename in self.openfiles:
            self.tabs.setCurrentIndex(self.openfiles.index(filename))
            return True 
        return False

    def openFileByName(self, filename):
        if filename in self.openfiles:
            self.tabs.setCurrentIndex(self.openfiles.index(filename))
            return
        file_content = onion.GetFileContent(filename)
        self.tabs.addTab(EditorWindow(file_content, filename, self.tabs), filename.split("/")[len(filename.split("/")) - 1])
        self.tabs.setCurrentIndex(self.tabs.count() - 1)
        self.openfiles.append(filename)
        onion.SettingsWrite_OPENED(self.openfiles)
            
    def openShell(self):
        dlg = ShellDialog()
        if dlg.exec():
            try:
                exec(dlg.shellBox.toPlainText())
            except:
                dlg2 = notifyDialog("ERROR IN EXECUTING SCRIPT")
                dlg2.exec()

class ProjectExplorer(QDockWidget):
    def __init__(self, mainwindow):
        super().__init__()
        self.layout = QVBoxLayout()
        self.path = onion.SettingsGet_PROJECT()
        self.mainwindow = mainwindow

        # setting font to the window
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(11)
        self.setFont(fixedfont)

        #explorer
        self.explorer = QTreeView()
        self.explorer.setContextMenuPolicy(Qt.CustomContextMenu)
        self.explorer.customContextMenuRequested.connect(self.openMenu)
        self.model = QFileSystemModel()
        self.model.setRootPath("/")
        self.explorer.setModel(self.model)
        self.explorer.setRootIndex(self.model.index(self.path))
        self.explorer.hideColumn(1)
        self.explorer.hideColumn(2)
        self.explorer.hideColumn(3)
        self.explorer.doubleClicked.connect(self.openFile)
        self.explorer.clicked.connect(self.navigateToFile)

        #form layout and frame
        self.layout.addWidget(self.explorer)
        self.mainWidget = QFrame()
        self.mainWidget.setLayout(self.layout)
        self.setWidget(self.mainWidget)

    def updateProj(self, newpath):
        self.explorer.setRootIndex(self.model.index(newpath))

    def openFile(self, signal):
        path = self.explorer.model().filePath(signal)
        if os.path.isfile(path):
            self.mainwindow.openFileByName(path)

    def navigateToFile(self, signal):
        path = self.explorer.model().filePath(signal)
        if os.path.isfile(path):
            self.mainwindow.navigateToFile(path)

    def openMenu(self, position):
        print("yo")
        menu = QMenu()

        #delete
        delAct = QAction("Delete", self)
        delAct.triggered.connect(self.deleteFile)
        menu.addAction(delAct)

        #rename
        renAct = QAction("Rename", self)
        renAct.triggered.connect(self.renameFile)
        menu.addAction(renAct)

        #copy
        cpyAct = QAction("Copy", self)
        cpyAct.triggered.connect(self.copyFile)
        menu.addAction(cpyAct)

        #cut
        cutAct = QAction("Cut", self)
        cutAct.triggered.connect(self.cutFile)
        menu.addAction(cutAct)

        #copy path
        cpyPAct = QAction("Copy Path", self)
        cpyPAct.triggered.connect(self.copyPath)
        menu.addAction(cpyPAct)

        menu.exec_(self.explorer.viewport().mapToGlobal(position))

    def deleteFile(self):
        print("deleting!")

    def renameFile(self):
        print("renaming!")

    def copyFile(self):
        print("copying!")

    def cutFile(self):
        print("cutting!")

    def copyPath(self):
        print("copying path!")

class ConsoleWindow(QDockWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(11)
        self.setFont(fixedfont)

        #console
        self.console = QTextEdit("ONION CONSOLE V:0.1.2")
        self.console.setReadOnly(True)

        #terminal
        self.terminal = QTextEdit("ONION TERMINAL V:0.1.1")
        self.terminal.setReadOnly(True)

        #tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.console, "Console")
        self.tabs.addTab(self.terminal, "Terminal")

        #input
        self.input = QLineEdit("")
        self.input.returnPressed.connect(self.enterCommand)

        #form layout and frame
        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.input)
        self.mainWidget = QFrame()
        self.mainWidget.setLayout(self.layout)
        self.setWidget(self.mainWidget)

    def enterCommand(self):
        print("input command")
        command = self.input.text()
        self.input.clear()
        self.printInput(command)
        self.processCommand(command)

    def printInput(self, msg):
        if self.tabs.currentIndex() == 0:
            self.console.append(">> " + msg)
        else:
            self.terminal.append(">> " + msg)

    def consoleOutput(self, msg):
        self.console.append("<< " + msg)

    def terminalOutput(self, msg):
        self.terminal.append("<< " + msg)

    def processCommand(self, msg):
        if self.tabs.currentIndex() == 0:
            self.consoleCommand(msg)
        else:
            self.terminalCommand(msg)

    def consoleCommand(self, msg):
        if msg == "version":
            self.consoleOutput("ONION CONSOLE V:0.1.2")
        else:
            self.consoleOutput("ERROR: Command \"" + msg + "\" not supported")

    def terminalCommand(self, msg):
        #print(subprocess.run(["ls"], capture_output=True, text=True).stdout)
        if msg == "version":
            self.terminalOutput("ONION TERMINAL V:0.1.1")
        else:
            process = subprocess.run([msg], capture_output=True, text=True, shell=True)
            if process.stderr != "":
                self.terminalOutput(process.stderr)
            else:
                self.terminalOutput(process.stdout)

class ProjectConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Set Project Configuration")
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.layout = QVBoxLayout()
        self.langLabel = QLabel("Project Language")
        self.lang = QLineEdit(onion.SettingsGet_PROJLANG())
        self.contentLabel = QLabel("Project Files")
        self.content = QPlainTextEdit(onion.SettingsGet_PROJCONTENT().replace("?", "\n"))
        self.content.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.destLabel = QLabel("Project Destination")
        self.dest = QLineEdit(onion.SettingsGet_PROJDEST())
        self.layout.addWidget(self.langLabel)
        self.layout.addWidget(self.lang)
        self.layout.addWidget(self.contentLabel)
        self.layout.addWidget(self.content)
        self.layout.addWidget(self.destLabel)
        self.layout.addWidget(self.dest)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class NotifyDialog(QDialog):
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

class ConfirmDialog(QDialog):
    def __init__(self, msg):
        super().__init__()
        self.setWindowTitle("Confirm")
        QBtn = QDialogButtonBox.Cancel | QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
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

class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.codeEditor = editor

    def sizeHint(self):
        return QSize(self.codeEditor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.codeEditor.lineNumberAreaPaintEvent(event)

class EditorWindow(QPlainTextEdit):
    def __init__(self, txt, filename, tabWidget):
        super().__init__(txt)
        self.filename = filename
        self.tabWidget = tabWidget
        
        #set up save mirroring
        self.saved = True
        self.textChanged.connect(self.changedText)
        
        # setting font to the editor
        fixedfont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixedfont.setPointSize(12)
        self.setFont(fixedfont)

        #disable text wrapping
        self.setLineWrapMode(QPlainTextEdit.NoWrap)

        #set up line numbers
        self.lineNumberArea = LineNumberArea(self)
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.updateLineNumberAreaWidth(0)

        #set palette
        self.colorPalette()

    def colorPalette(self):
        print("setting tab palette")

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 15 + self.fontMetrics().width('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()
            lineColor = QColor(Qt.red).darker(160)
            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        painter_color = QColor()
        painter_color.setRgb(61, 61, 61)
        painter.fillRect(event.rect(), painter_color)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(blockNumber + 1)
                painter_color.setRgb(212, 212, 212)
                painter.setPen(painter_color)
                painter.drawText(0, int(top), self.lineNumberArea.width(), height, Qt.AlignRight, number + " ")

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def runScript(self, console):
        success = onion.RunScript(self.toPlainText(), self.filename, console)
        if not success:
            print("error. script failed to run.")
        
    def changedText(self):
        self.unsave()
        self.tabToSpaces()
        self.pySmartReturn()

    def tabToSpaces(self):
        if self.getCursorChar() == '\t':
            self.textCursor().deletePreviousChar()
            self.insertPlainText("    ")

    def pySmartReturn(self):
        if self.getCurrLine() == "":
            prevline = self.getLineByNum(self.textCursor().blockNumber() - 1)
            spaces = 0
            for c in prevline:
                if c != " ":
                    break
                spaces += 1
            spacestr = ""
            for i in range(spaces):
                spacestr += " "
            self.insertPlainText(spacestr)

    def getLineByNum(self, linenum):
        return self.document().findBlockByLineNumber(linenum).text()

    def getCurrLine(self):
        return self.textCursor().block().text()

    def getCursorChar(self):
        return self.document().characterAt(self.textCursor().position() - 1)

    def unsave(self):
        if self.saved:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), self.tabWidget.tabText(self.tabWidget.currentIndex()) + "*")
            self.saved = False
        
    def save(self):
        self.saved = onion.SaveFile(self.saved, self.toPlainText(), self.filename) 
        if self.saved:
            self.tabWidget.setTabText(self.tabWidget.currentIndex(), self.filename.split("/")[len(self.filename.split("/")) - 1])

    def saveAs(self):
        print("save as")
        self.filename = QFileDialog.getSaveFileName(self, 'Save File')[0]
        self.saved = onion.SaveFile(False, self.toPlainText(), self.filename) 
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), self.filename.split("/")[len(self.filename.split("/")) - 1])
