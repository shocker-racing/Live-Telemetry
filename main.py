from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QDesktopWidget
from widgets.gauge_widget import gauge_widget
import sys

# Background color      : #1E1E1E
# Panel Background color: #424242
# Positive color (green): #32CD32
# Negative color (red)  : #FF0000
# Main text color       : #FFFFFF
# Secondary text color  : #A0A0A0
# Accent 1 (Critical)   : #FFD700
# Accent 2 (General)    : #64C7FF
 
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

        # background
        self.setStyleSheet("background-color: #000000")

        self.initUI()

    def initUI(self):
        # Making widgets on window
        self.gauge = gauge_widget(self)

        # variables to move widgets
        x = (self.width() // 2) - self.gauge.width() // 2
        y = (self.height() // 2) - self.gauge.height() // 2
        self.gauge.move(x,y)


def window():
    app = QApplication(sys.argv)
    win = mainWindow()

    # showing window
    win.show()

    ## for clean exit when X is clicked
    sys.exit(app.exec_())

def main():
    window()

if __name__ == "__main__":
    main()