import random
import math
import numpy as np
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QBrush, QColor, QPen, QFont

color_pool = ["#EBD9CB", "#DBE2EC", "#DECECE", "#E7ADAC", "#A6BAAF", "#B4A29E", "#C6DEE0", "#B98A82"]

class Ball(QGraphicsEllipseItem):
    def __init__(self, p_id, name, memory_usage, x, y):
        super().__init__() 

        # related process info
        self.p_id = p_id
        self.name = name
        self.setMemoryUsg(memory_usage)
        self.setAcceptHoverEvents(True)

        # init size and position
        self.setRect(0, 0, self.size, self.size)
        self.setPos(x, y)

        # text
        self.text_item = QGraphicsTextItem(f"{self.memory_usage:.2%}", self)
        self.text_item.setFont(QFont("Arial", 8))
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos((self.size/2 - text_rect.width()/2 ), (self.size/2 - text_rect.height()/2 ))

        self.tag = QGraphicsTextItem(self.name, self)
        self.tag.setVisible(False)  # 預設不顯示

        # color
        brush = QBrush(QColor(random.choice(color_pool)))
        self.setBrush(brush)

        pen = QPen(QColor(90, 90, 90))
        pen.setWidth(2)
        self.setPen(pen)

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def getP_Id(self):
        return self.p_id
    
    # size = 20 + 60 * memory usage percentage
    # speed scalar = 5 - 3 * memory usage percentage
    def setMemoryUsg(self, memory_usage, reset_dir=True):
        self.memory_usage = memory_usage
        self.size = 30 + 400 * self.memory_usage

        if memory_usage < 0.25:
            speed_scalar = 4 - 12 * self.memory_usage
        elif memory_usage < 0.5:
            memory_usage -= 0.25
            speed_scalar = 1 - 2 * self.memory_usage
        else:
            speed_scalar = 0.5 - 0.8 * (memory_usage-0.25)
        if reset_dir:
            self.x_dir = random.random() * speed_scalar
            self.y_dir = math.sqrt(pow(speed_scalar, 2) - pow(self.x_dir, 2))
            if random.random() > 0.5 :
                self.x_dir *= -1
            if random.random() > 0.5:
                self.y_dir *= -1
        else:
            old_sc = math.sqrt(self.x_dir**2 + self.y_dir **2)
            self.x_dir = math.sqrt(self.x_dir**2 * (speed_scalar**2 / old_sc**2)) * (self.x_dir/abs(self.x_dir))
            self.y_dir = math.sqrt(self.y_dir**2 * (speed_scalar**2 / old_sc**2)) * (self.y_dir/abs(self.y_dir))
            self.text_item.setPlainText(f"{memory_usage:.2%}")

    def update(self):
        # check if out of scene
        sceneRect = self.scene().sceneRect()
        new_x, new_y = self.updatePos(sceneRect)
        self.setRect(0, 0, self.size, self.size)
        self.setPos(new_x, new_y)
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos((self.size/2 - text_rect.width()/2 ), (+ self.size/2 - text_rect.height()/2 ))
    
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
        self.scene().removeItem(self)
        del self
    
    def hoverEnterEvent(self, event):
        # 設定文字框的位置在圓形右上角
        text_x = self.rect().topRight().x()
        text_y = self.rect().topRight().y()
        self.tag.setPos(text_x-10, text_y - 20)  # 顯示在右上角稍上方
        self.tag.setVisible(True)  # 顯示文字框
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.tag.setVisible(False)  # 當滑鼠離開時隱藏文字框
        super().hoverLeaveEvent(event)