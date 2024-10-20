import random
import math
import numpy as np
from PyQt5.QtWidgets import QGraphicsEllipseItem
from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QBrush, QColor, QPen


class Ball(QGraphicsEllipseItem):
    size = 20
    unitSpeed = 3

    def __init__(self, x, y):
        super().__init__() 

        # init speed and direction
        self.x_dir, self.y_dir = self.initDirection()

        # init size and position
        self.setRect(0, 0, self.size, self.size)
        self.setPos(x, y)

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
        x_dir = random.random() * self.unitSpeed
        y_dir = math.sqrt(pow(self.unitSpeed, 2) - pow(x_dir, 2))
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
            self.removeSelf()
        else:
            r, g, b= self.color()
            brush = QBrush(QColor(r, g, b))  # RGB 顏色
            self.setBrush(brush)

        self.checkColliding()
    
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
    
    def removeSelf(self):
        # ball = Ball(820, 640)
        # self.scene().addItem(ball)
        self.scene().removeItem(self)
        del self
    
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
    
    def mousePressEvent(self, event):
        if event.button() == 1:
            times = pow(self.unitSpeed, 2) / (pow(self.x_dir, 2) + pow(self.y_dir, 2))
            self.x_dir += times * self.x_dir
            self.y_dir += times * self.y_dir
            super().mousePressEvent(event)
        elif event.button() == 2:
            self.removeSelf()
        else:
            super().mousePressEvent(event)

    def contains(self, point):
        # distance to center of circle
        distance = math.sqrt((point.x() - self.x() - self.size/2)**2 + (point.y() - self.y() - self.size/2)**2)

        # return if in circle
        return distance <= self.size
    
    def overlaps(self, x, y, size):
        distance = math.sqrt((x + size - self.x() - self.size/2)**2 + (y + size - self.y() - self.size/2)**2)

        return distance <= self.size + size

    def checkColliding(self):
        # if colliding => fusion
        itemList = self.collidingItems()

        # check if self is the largest one colliding (only deal with largest one)
        for idx in range(len(itemList)-1, -1, -1):
            if itemList[idx] and isinstance(itemList[idx], Ball) and self.size < itemList[idx].size:
                return
            
        for idx in range(len(itemList)-1, -1, -1):
            if itemList[idx] and isinstance(itemList[idx], Ball) and \
                self.overlaps(itemList[idx].x(), itemList[idx].y(), itemList[idx].size):
                    itemList[idx].setVisible(False)

                    # adjust speed
                    self.x_dir = ((self.size / itemList[idx].size) * self.x_dir + itemList[idx].x_dir) / (self.size / itemList[idx].size)
                    self.y_dir = ((self.size / itemList[idx].size) * self.y_dir + itemList[idx].y_dir) / (self.size / itemList[idx].size)
                    if (self.x_dir)**2 + (self.y_dir)**2 == 0:
                        self.x_dir = random.random() * self.unitSpeed
                        self.y_dir = math.sqrt(pow(self.unitSpeed, 2) - pow(x_dir, 2))
                    elif ((self.x_dir)**2 + (self.y_dir)**2) < (self.unitSpeed)**2:
                        times = (self.unitSpeed)**2 / ((self.x_dir)**2 + (self.y_dir)**2)
                        self.x_dir = times * self.x_dir
                        self.y_dir = times * self.y_dir

                    self.size += itemList[idx].size
                    self.life = (self.life + itemList[idx].life)/2
                    x, y = self.x(), self.y()
                    self.setRect(0, 0, self.size, self.size)
                    self.setPos(x - itemList[idx].size/2, y - itemList[idx].size/2)
                    itemList[idx].removeSelf()
