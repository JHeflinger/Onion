import onion
import sys
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QDialog,
    QFileDialog,
    QDialogButtonBox,
    QLineEdit,
    QTextEdit,
    QCheckBox,
    QFrame,
    QComboBox,
    QScrollArea,
    QMenu,
    QAction,
    QTabWidget,
    QShortcut)
     
class Main(QMainWindow):
     
    def __init__(self, parent = None):
        QMainWindow.__init__(self,parent)
     
        self.initUI()
     
    def initUI(self):
     
        # x and y coordinates on the screen, width, height
        self.setGeometry(100,100,1030,800)
     
        self.setWindowTitle("Onion")
