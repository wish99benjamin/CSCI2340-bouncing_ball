import os
import psutil
import sys
import random
import time

from PyQt5.QtWidgets import QApplication, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import QTimer, QThread, pyqtSignal

from ball import Ball

class WorkerThread(QThread):
    # 定義一個信號來傳遞處理過的數據
    data_ready = pyqtSignal(dict)

    def __init__(self, memory_threshold, memory_total):
        super().__init__()
        self.memory_threshold = memory_threshold
        self.memory_total = memory_total
        self.my_dict = {}

    def run(self):
        self.updateDict()
        self.data_ready.emit(self.my_dict)  # 線程完成時發送信號並傳遞數據

    def updateDict(self):
        # 查找使用超過0.5%記憶體的進程
        self.my_dict = {}
        count = 0
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            count += 1
            if count == 10:
                time.sleep(0.001)
                count = 0
            try:
                process_info = proc.info
                if process_info['memory_info'].rss > self.memory_threshold:
                    self.my_dict[process_info['pid']] = [process_info['name'], process_info['memory_info'].rss / self.memory_total]
            # 處理無法訪問的進程
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
            # pass

class MainWindow(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bouncing Ball")

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        self.unit_width = screen_size.width() // 6
        self.unit_height = screen_size.height() // 4

        self.setGeometry(int(1.5*self.unit_width), int(0.5*self.unit_height), 3*self.unit_width, 3*self.unit_height)
        self.setFixedSize(3*self.unit_width, 3*self.unit_height)

        self.memory_total = psutil.virtual_memory().total
        self.memory_threshold = self.memory_total* 0.005

        self.setBackgroundBrush(QColor(230, 230, 230))
        self.createScene()

        # init timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateScene)
        self.timer.start(5000)

    def createScene(self):
        my_dict = {}
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            try:
                process_info = proc.info
                if process_info['memory_info'].rss > self.memory_threshold:
                    my_dict[process_info['pid']] = [process_info['name'], process_info['memory_info'].rss / self.memory_total]
            # precess that can't be visited
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  

        self.scene = QGraphicsScene()
        for key, value in my_dict.items():
            self.addBall(key, value[0], value[1])
        self.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 3*self.unit_width-2, 3*self.unit_height-62)

    def updateScene(self):
        self.worker = WorkerThread(self.memory_threshold, self.memory_total)
        self.worker.data_ready.connect(self.updateBall)  # 當線程數據準備好時更新界面
        self.worker.start()

    def updateBall(self, data):
        for item in self.scene.items():
            if isinstance(item, Ball):
                if item.getP_Id() in data:
                    item.setMemoryUsg(data[item.getP_Id()][1], reset_dir=False)
                    del data[item.getP_Id()]
                else:
                    item.removeSelf()
        for key, value in data.items():
            self.addBall(key, value[0], value[1])


    def addBall(self, p_id, name, memory_usage):
        x = random.randint(int(0.25*self.unit_width), int(2.75*self.unit_width))
        y = random.randint(int(0.25*self.unit_height), int(2.75*self.unit_height))
        ball = Ball(p_id, name, memory_usage, x, y)
        self.scene.addItem(ball)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



























# 獲取所有運行中的進程
# for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
#     try:
#         process_info = proc.info
#         print(f"Process ID: {process_info['pid']}, "
#               f"Process Name: {process_info['name']}, "
#               f"Memory Usage: {process_info['memory_info'].rss / (1024 * 1024)} MB")
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass  # 處理無法訪問的進程

# 獲取當前所有進程
# for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
#     try:
#         # 顯示進程ID、名稱及內存使用
#         print(f"Process ID: {proc.info['pid']}, Process Name: {proc.info['name']}, Memory Usage: {proc.info['memory_info'].rss / (1024 * 1024):.2f} MB")

#         # 尋找子進程
#         parent = psutil.Process(proc.info['pid'])
#         children = parent.children(recursive=True)

#         # 列出每個子進程
#         if children:
#             for child in children:
#                 child_info = child.as_dict(attrs=['pid', 'name', 'memory_info'])
#                 print(f"  Child Process ID: {child_info['pid']}, Name: {child_info['name']}, Memory Usage: {child_info['memory_info'].rss / (1024 * 1024):.2f} MB")

#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass

# 使用 psutil.Process() 獲取進程的記憶體使用情況
# 獲取當前程式的 PID
# current_pid = os.getpid()
# current_pid = 50256
# process_info = psutil.Process(current_pid)
# print(f"Process ID: {process_info.pid}, "
#               f"Process Name: {process_info.name()}, "
#               f"Memory Usage: {process_info.memory_info().rss / (1024 * 1024)} MB")
# print(process_info)

# 獲取系統的內存信息
# memory_info = psutil.virtual_memory()
# print(memory_info)