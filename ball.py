import random
import math
import numpy as np
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QBrush, QColor, QPen


class Ball(QGraphicsEllipseItem):
    def __init__(self, x, y):
        super().__init__() 

        # init speed and direction
        self.x_dir, self.y_dir = self.initDirection()

        # init size and position
        self.size = 20
        self.setRect(0, 0, self.size, self.size)
        self.setPos(x,y)

        # init life(color) and other style
        self.life = min(int(np.random.exponential(400)), 1000)
        r, g, b= self.color()
        brush = QBrush(QColor(r, g, b))
        self.setBrush(brush)
        pen = QPen(QColor(90, 90, 90))
        pen.setWidth(2)
        self.setPen(pen)

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def initDirection(self):
        x_dir = random.random() * 3
        y_dir = math.sqrt(9 - pow(x_dir, 2))
        if random.random() > 0.5 :
            x_dir *= -1
        if random.random() > 0.5:
            y_dir *= -1
        return x_dir, y_dir

    def update(self):
        # check if out of scene
        sceneRect = self.scene().sceneRect()
        new_x, new_y = self.updatePos(sceneRect)
        self.setPos(new_x, new_y)

        self.life += 1
        if self.life >= 1275:
            # ball = Ball(820, 640)
            # self.scene().addItem(ball)
            self.scene().removeItem(self)
            del self
        else:
            r, g, b= self.color()
            brush = QBrush(QColor(r, g, b))  # RGB 顏色
            self.setBrush(brush)
    
    def updatePos(self, sceneRect):
        new_x, new_y = self.x()+self.x_dir, self.y()+self.y_dir 

        # check and fix x
        if new_x >= sceneRect.x() and new_x+self.size <= sceneRect.right():
            pass
        else:
            if new_x < sceneRect.x():
                x_offset = new_x-sceneRect.x()
                new_x = sceneRect.x() + -1*x_offset
            elif new_x+self.size > sceneRect.right():
                x_offset = new_x+self.size-sceneRect.right()
                new_x = sceneRect.right() + -1*x_offset - self.size
            self.x_dir *= -1
        # check and fix y
        if new_y >= sceneRect.y() and new_y+self.size <= sceneRect.bottom():
            pass
        else:
            if new_y < sceneRect.y():
                y_offset = new_y-sceneRect.y()
                new_y = sceneRect.y() + -1*y_offset
            elif new_y+self.size > sceneRect.bottom():
                y_offset = new_y+self.size-sceneRect.bottom()
                new_y = sceneRect.bottom() + -1*y_offset - self.size
            self.y_dir *= -1

        return new_x, new_y
    
    def color(self):
        # 255, 255, 255 white  0
        # 255, 0,   0   red    1
        # 255, 255, 0   yellow 2
        # 0,   255, 0   green  3
        # 0,   0,   255 blue   4
        # 127, 0,   128 purple 
        # 0,   0,   0   black  5

        stage, value = self.life//255, self.life%255
        if stage == 0:
            r, g, b = 255, 255-value, 255-value
        elif stage == 1:
            r, g, b = 255, value, 0
        elif stage == 2:
            r, g, b = 255-value, 255, 0
        elif stage == 3:
            r, g, b = 0, 255-value, value
        elif stage == 4:
            if value <= 127:
                r, g, b = value, 0, 255-value
            else:
                r, g, b = 255-value, 0, 255-value
        return r, g, b