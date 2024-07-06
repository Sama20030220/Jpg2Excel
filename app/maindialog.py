from PyQt5.QtGui import QImage, QPixmap, QImageReader
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from ai.ToExcel import excel
from app.mdui import Ui_Dialog
import cv2 as cv
from PyQt5 import QtWidgets, QtGui, QtCore
from app.mainsec import MainDialog1
from ai.ToWords import Words

import data.resource_rc
class MainDialog(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)

        # 加载并转换图片为 QPixmap
        self.pixmap = QPixmap("data/bg.jpg")  # 假设图片路径正确
        if self.pixmap.isNull():
            print("背景图片加载失败")
            # 设置QLabel的尺寸
        self.label.resize(self.width(), self.height())
        self.label.setScaledContents(True)
        # 将背景图片设置为QLabel的内容
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))
        # 监听窗口大小变化事件
        self.resizeEvent = self.on_resize
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.img = cv.imread('data/excel1.jpg')
        self.showimg()

    def on_resize(self, event):
        self.label.resize(self.width(), self.height())
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))
    def showimg(self):
        h, w, c = self.img.shape
        img_bytes = self.img.tobytes()
        image = QImage(img_bytes, w, h, w * c, QImage.Format_BGR888)
        pix = QPixmap.fromImage(image)
        width = self.ui.label_2.width()
        height = self.ui.label_2.height()
        scale_pix = pix.scaled(width, height, Qt.KeepAspectRatio)
        self.ui.label_2.setPixmap(scale_pix)

    def Excel(self):
        boundaries = excel(self.img)
        Words(boundaries)
        self.md = MainDialog1()
        self.md.show()
        self.close()
