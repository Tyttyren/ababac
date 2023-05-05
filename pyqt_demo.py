import sys
import os
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt, QTimer

class FileSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('选择文件')
        self.setGeometry(100, 100, 1000, 800)

        # 创建UI组件
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.selectButton = QPushButton('选择文件', self)
        self.selectButton.clicked.connect(self.openFile)

        # 添加布局
        self.mainLayout = QVBoxLayout(self)
        self.topLayout = QHBoxLayout()
        self.topLayout.addStretch()
        self.topLayout.addWidget(self.selectButton)
        self.topLayout.addStretch()
        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addWidget(self.label)

        # 添加返回按钮
        self.backButton = QPushButton('返回', self)
        self.backButton.setGeometry(10, 10, 80, 30)
        self.backButton.clicked.connect(self.goBack)

        # 初始化视频播放相关变量
        self.video = None
        self.timer = QTimer()
        self.frameIndex = 0

    def openFile(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self, '选择文件', '', '图片文件 (*.jpg *.png);;视频文件 (*.mp4)', options=options)

        # 判断选择的是图片还是视频文件
        if file.endswith('.jpg') or file.endswith('.png'):
            # 加载并显示图片
            pixmap = QPixmap(file)
            if pixmap.width() > 800 or pixmap.height() > 600:
                pixmap = pixmap.scaled(800, 600, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)
        elif file.endswith('.mp4'):
            # 打开视频并获取帧数
            self.video = cv2.VideoCapture(file)
            self.frameCount = int(self.video.get(cv2.CAP_PROP_FRAME_COUNT))

            # 设置定时器
            self.timer.timeout.connect(self.showNextFrame)
            self.timer.start(1000 // int(self.video.get(cv2.CAP_PROP_FPS)))

    def showNextFrame(self):
        # 读取下一帧
        ret, frame = self.video.read()
        if ret:
            # 将帧转换为QImage，并显示在标签上
            height, width, channel = frame.shape
            if width > 800 or height > 600:
                frame = cv2.resize(frame, (800, 600), interpolation=cv2.INTER_AREA)
            qImg = QImage(frame.data, width, height, width * channel, QImage.Format_RGB888).rgbSwapped()
            self.label.setPixmap(QPixmap.fromImage(qImg))
            self.frameIndex += 1
        else:
            # 播放完毕，停止定时器
            self.timer.stop()
            self.video.release()

    def goBack(self):
        # 返回上一页
        self.close()
        # 创建目标窗口实例
# target_window = TargetWindow()
# # 显示目标窗口
# target_window.show()
# # 隐藏主窗口
# self.hide()
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileSelector()
    ex.show()
    sys.exit(app.exec_())