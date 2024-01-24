import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

import pyautogui

class GameOverlay(QWidget):
    def __init__(self):
        super().__init__()

        self.setMouseTracking(True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowType.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen = QApplication.primaryScreen()
        screen_geometry = screen.geometry()

        self.screen_width = screen_geometry.width()
        self.screen_height = screen_geometry.height()

        self.setGeometry(0, 0, self.screen_width, self.screen_height)  # Set the overlay size to match the screen        

        self.mouseArray = []
        self.px = "-"
        self.py = "-"

        self.hue = 0

        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)

        # # Draw a transparent background
        # painter.setBrush(QBrush(QColor(0, 0, 0, 0)))
        # painter.drawRect(self.rect())

        # # Draw the circle outline
        # painter.setPen(QColor(Qt.white))
        # painter.setBrush(QBrush(QColor(0, 0, 0, 0)))


        mousePos = pyautogui.position()
        self.mouseArray.append(mousePos)
        if len(self.mouseArray) > 16:
            self.mouseArray.pop(0)

        self.hue -= (len(self.mouseArray) - 1)

        self.penSize = 1

        for e in self.mouseArray:
            pen = QPen(QColor.fromHsl(self.hue % 360, 255, 128))
            pen.setWidth(int(self.penSize))
            pen.setCapStyle(Qt.RoundCap)
            self.penSize += 30 / len(self.mouseArray)
            painter.setPen(pen)
            # painter.setPen(QColor.fromHsl(self.hue % 255 + 1, 255, 128))
            self.hue += 1
            if self.px == "-":
                self.px = e[0]
                self.py = e[1]
            else:
                painter.drawLine(self.px, self.py, e[0], e[1])
                self.px = e[0]
                self.py = e[1]

        self.px = "-"
        self.py = "-"
        
    
    # def mouseMoveEvent(self, event):
    #     print(event.y())
    #     self.mouseArray.insert(0, [event.x(), event.y()])
    #     if len(self.mouseArray) > 16:
    #         self.mouseArray.pop()

def main():
    app = QApplication(sys.argv)
    overlay = GameOverlay()

    timer = QTimer()
    timer.timeout.connect(overlay.update)
    timer.start(16)  # Update the overlay approximately every 16 milliseconds (about 60 FPS)

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

wow = 0
while (True): 
    wow += 1