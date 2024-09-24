import sys
import random
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
            self.scene.addItem(ball)
        # self.scene.setSceneRect(2*self.unit_width, self.unit_height, 2*self.unit_width, 2*self.unit_height)
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

    def addBall(self):
        ball = Ball(random.randint(2.5*self.unit_width, 3.5*self.unit_width), 
                        random.randint(1.5*self.unit_height, 2.5*self.unit_height))
        self.scene.addItem(ball)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
