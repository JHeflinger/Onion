from PyQt5.QtWidgets import QApplication
import sys
from qt_onion import MainWindow

if __name__ == '__main__':
 
    # create application
    app = QApplication(sys.argv)
    app.setApplicationName("Onion")
    window = MainWindow()
 
    # execute app
    app.exec_()
