import sys
import random
from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
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
        self.createScene()

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

        
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
