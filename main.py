import qt_onion
import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    main = Main()
    main.show() 
    sys.exit(app.exec_())
     
if __name__ == "__main__":
    main()
