import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtProperty

class gauge_widget(QWidget):
    def __init__(self, parent = None, title = "", min_gauge_value = 0, max_gauge_value = 100, orange_start = 33, orange_end = 66):
        super().__init__(parent)
        self.setMinimumSize(250,200)

        self._value = 5000;

        #setting params
        self.title = title
        self.min_gauge = min_gauge_value
        self.max_gauge = max_gauge_value
        self.orange_start = orange_start
        self.orange_end = orange_end

        # colors for this widget
        self.background_color = QColor("#1E1E1E")
        self.panel_color = QColor("#424242")
        self.gauge_arc_color = QColor("#A0A0A0")
        self.needle_color = QColor("#FFD700")
        self.label_color = QColor("#FFFFFF")
        self.center_circle_color = QColor("#A0A0A0")
        self.green_zone = QColor("#579549")
        self.orange_zone = QColor("#BA7432")
        self.red_zone = QColor("#9E4E42")

    def paintEvent(self, event):
        """
        Function for redrawing widget
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

        side = min(self.width(), self.height())

        painter.save()
        painter.translate(self.width() / 2, (self.height() / 2) + 30)
        painter.scale(side / 200.0, side / 200.0)

        self.draw_title(painter)
        self.draw_value(painter)
        self.draw_gauge_arc(painter)
        self.draw_main_gauge(painter)
        self.draw_main_gauge_color(painter)
        # self.draw_ticks_and_labels(painter)
        # self.draw_needle(painter)

        painter.restore

    def draw_title(self, painter):
        painter.save()

        painter.setFont(QFont("Arial", 14))
        painter.setPen(QPen(self.label_color))

        painter.drawText(QRectF(-105, -120, 210, 20), Qt.AlignCenter, self.title)

        painter.restore()

    def draw_value(self, painter):
        painter.save()

        painter.setFont(QFont("Arial", 16))
        painter.setPen(QPen(self.label_color))
        text = f"{self._value}"

        painter.drawText(QRectF(-40, -10, 80, 20), Qt.AlignCenter, text)

        painter.restore()
        
    def draw_gauge_arc(self, painter):
        
        pen = QPen(self.green_zone)
        pen.setWidth(3)
        pen.setCapStyle(Qt.FlatCap)
        painter.setPen(pen)

        angle_orange_start = int(240*(self.orange_start / self.max_gauge))
        angle_orange_end = int(240*(self.orange_end / self.max_gauge))

        painter.rotate(150)

        # negative number = clockwise
        # positive number = counterclockwise
        painter.drawArc(QRectF(-80, -80, 160, 160), 0 * 16, -angle_orange_start * 16)

        pen.setColor(self.red_zone)
        painter.setPen(pen)
        painter.drawArc(QRectF(-80, -80, 160, 160), -angle_orange_end * 16, -(240-angle_orange_end) * 16)
        pen.setColor(self.orange_zone)
        painter.setPen(pen)
        painter.drawArc(QRectF(-80, -80, 160, 160), -angle_orange_start * 16, -(angle_orange_end - angle_orange_start) * 16)
        

    def draw_main_gauge(self, painter):
        painter.save()
        pen = QPen(self.gauge_arc_color)
        pen.setWidth(30)
        pen.setCapStyle(Qt.FlatCap)

        painter.setPen(pen)
        painter.drawArc(QRectF(-60, -60, 120, 120), 0 * 16, -240 * 16)
        painter.restore()

    def draw_main_gauge_color(self, painter):
        painter.save()
        pen = QPen(self.green_zone)
        pen.setCapStyle(Qt.FlatCap)
        pen.setWidth(30)
        if(self._value < self.orange_start):
            pen.setColor(self.green_zone)
        elif(self._value > self.orange_end):
            pen.setColor(self.red_zone)
        else: 
            pen.setColor(self.orange_zone)

        painter.setPen(pen)
        angle = 0

        if(self._value >= self.max_gauge):
            angle = 240
        else:
            angle = int((self._value / self.max_gauge) * 240)

        painter.drawArc(QRectF(-60, -60, 120, 120), 0 * 16, -angle * 16)
        painter.restore()


    def draw_ticks_and_labels(self, painter):
        painter.save

        pen = QPen(self.gauge_arc_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 10))

        for i in range(11):
            angle = 240 + (i * 24)
            painter.save()
            painter.rotate(angle)
            painter.drawLine(0, -70, 0, -80)
            
            # Position and draw the label text
            text = str(i * 10)
            text_rect = QRectF(-20, -100, 40, 20)
            painter.drawText(text_rect, Qt.AlignCenter, text)
            
            painter.restore()
            
        painter.restore()

    def draw_needle(self, painter): 
        painter.translate(self.width() / 2, self.height() / 2)
        painter.save()
        
        # Pen setup
        pen = QPen(self.needle_color)
        pen.setWidth(4)
        painter.setPen(pen)

        angle = 60 + (self._value * 2.4)
        painter.rotate(angle)
        painter.drawLine(0, 0, 0, 70)

        painter.restore()

        # Drawing center circle
        painter.setBrush(QBrush(self.center_circle_color))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(QRectF(-10, -10, 20, 20))

        # Draw number
        painter.setFont(QFont("Arial", 12))
        painter.setPen(QPen(self.label_color))
        text = f"{int(self._value)}" + " MPH"
        text_rect = QRectF(-50, 20, 100, 20)
        painter.drawText(text_rect, Qt.AlignCenter, text)

    @pyqtProperty(int)
    def value(self):
        return self._value
    
    @value.setter
    def value(self, val):
        if(0 <= val <= 100):
            self._value = val
            self.update()