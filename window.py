from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QDesktopWidget
import sys

# inheriting from QMainWindow
class mainWindow(QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()

        # getting screen size
        screen = QDesktopWidget().screenGeometry()
        width = int(screen.width() * 0.7)
        height = int(screen.height() * 0.7)
        left = (screen.width() - width) // 2
        top = (screen.height() - height) // 2

        # positioning and size of window: win.setGeometry(xpos, ypos, width, height)
        self.setGeometry(left, top, width, height)
        self.setWindowTitle("Real-time Telemetry")

        self.initUI()

    def initUI(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setText("Button not clicked")
        self.label.move(50,50)
        self.label.adjustSize()

        self.b1 = QtWidgets.QPushButton(self)
        self.b1.setText("Button")
        self.b1.clicked.connect(self.clicked)

    def clicked(self):
        self.label.setText("Clicked Button")
        self.update()

    def update(self):
        self.label.adjustSize()

def window():
    app = QApplication(sys.argv)
    win = mainWindow()

    # showing window
    win.show()

    ## for clean exit when X is clicked
    sys.exit(app.exec_())


window()