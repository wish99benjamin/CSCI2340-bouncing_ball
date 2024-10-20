import sys
import random
import time
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QTimer
from ball import Ball

class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bouncing Ball")

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.unit_width = screen_size.width() // 6
        self.unit_height = screen_size.height() // 4

        self.setGeometry(2*self.unit_width, self.unit_height, 2*self.unit_width, 2*self.unit_height)
        self.setFixedSize(2*self.unit_width, 2*self.unit_height)

        self.setBackgroundBrush(QColor(230, 230, 230))
        self.createScene()

        # init timer
        self.timeTooEmpty = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(50)

    def createScene(self):
        self.scene = QGraphicsScene()
        for num in range(5):
            ball = Ball(random.randint(2.5*self.unit_width, 3.5*self.unit_width), 
                        random.randint(1.5*self.unit_height, 2.5*self.unit_height))
            self.scene.addItem(ball) # coordinate of ball is the same as coordinate of scene
        self.setScene(self.scene)
        view_rect = self.viewport().rect()
        scene_rect = self.mapToScene(view_rect).boundingRect()
        self.scene.setSceneRect(scene_rect)

    def updateScene(self):
        counter = 0
        for item in self.scene.items():
            if isinstance(item, Ball): counter += 1
            if counter >= 5: 
                self.timeTooEmpty = 0
                break

        if counter < 5:
            self.timeTooEmpty += 1
            if self.timeTooEmpty >= 60:
                self.addBall()
                self.timeTooEmpty = 0

    def addBall(self, x = None, y = None):
        if x is None:
            x = random.randint(int(2.5*self.unit_width), int(3.5*self.unit_width))
        if y is None:
            y = random.randint(int(1.5*self.unit_height), int(2.5*self.unit_height))
        ball = Ball(x, y)
        self.scene.addItem(ball)

    def mousePressEvent(self, event):
        if event.button() == 1:
            item = self.itemAt(event.pos()) # look at coordinate of view
            if isinstance(item, Ball) and item.contains(self.mapToScene(event.pos())): # map to scene look at coordinate of scene
                super().mousePressEvent(event)
            else:
                self.addBall(self.mapToScene(event.pos()).x() - Ball.size/2, self.mapToScene(event.pos()).y() - Ball.size/2)
        else:
            super().mousePressEvent(event)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
