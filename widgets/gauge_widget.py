import math
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QBrush, QColor, QPen, QFont, QPainterPath
from PyQt5.QtCore import Qt, QPointF, QRectF, pyqtProperty

class gauge_widget(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setMinimumSize(200,200)

        self._value = 0;

        # colors for this widget
        self.background_color = QColor("#1E1E1E")
        self.panel_color = QColor("#424242")
        self.gauge_arc_color = QColor("#A0A0A0")
        self.needle_color = QColor("#FFD700")
        self.label_color = QColor("#FFFFFF")
        self.center_circle_color = QColor("#A0A0A0")

    def paintEvent(self, event):
        """
        Function for redrawing widget
        """

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.NoPen)
        painter.drawRect(self.rect())

        side = min(self.width(), self.height())

        painter.save()
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.draw_gauge_arc(painter)
        self.draw_ticks_and_labels(painter)
        self.draw_needle(painter)

        painter.restore

        
    def draw_gauge_arc(self, painter):
        pen = QPen(self.gauge_arc_color)
        pen.setWidth(10)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)

        painter.drawArc(QRectF(-80, -80, 160, 160), -30 * 16, 240 * 16)

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
        text = f"{int(self._value)}"
        text_rect = QRectF(-50, 20, 100, 20)
        painter.drawText(text_rect, Qt.AlignCenter, text)