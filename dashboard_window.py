from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget
from PyQt5.QtCore import QTimer
from widgets.gauge_widget import gauge_widget
import random
import sys

# Background color      : #1E1E1E
# Panel Background color: #424242
# Positive color (green): #579549
# Negative color (red)  : #9E4E42
# Main text color       : #FFFFFF
# Secondary text color  : #A0A0A0
# Accent 1 (Critical)   : #BA7432
# Accent 2 (General)    : #64C7FF
 
# inheriting from QMainWindow
class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()

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
        self.Engine_RPM_gauge = gauge_widget(self,"Engine RPM", 0, 12000, 9000, 11000)
        self.oil_pressure_gauge = gauge_widget(self,"Oil pressure", 0, 100, 70, 70, "psi")
        self.coolant_flow_gauge = gauge_widget(self,"Coolant Temperature", 0, 250, 185, 212, "°F")
        self.fuel_pressure_gauge = gauge_widget(self, "Fuel Pressure", 0, 100, 40, 55, "psi")

        # variables to move widgets
        x = 10
        y = (self.height()) - 10 - 200
        self.Engine_RPM_gauge.move(x,y)

        y -= 210
        self.oil_pressure_gauge.move(x,y)

        x += 260
        self.coolant_flow_gauge.move(x,y)

        y += 210
        self.fuel_pressure_gauge.move(x,y)
        self.simulate()

    def simulate(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.change)
        self.timer.start(1)

    def change(self):
        self.Engine_RPM_gauge.value = self.Engine_RPM_gauge.value + 1
        self.oil_pressure_gauge.value = random.randint(0,100)
        self.coolant_flow_gauge.value = random.randint(0,250)
        self.fuel_pressure_gauge.value = random.randint(0,100)