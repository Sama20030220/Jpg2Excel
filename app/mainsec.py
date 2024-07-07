import os
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from openpyxl.utils.dataframe import dataframe_to_rows
from app.secondui import Ui_Dialog
import pandas as pd


class MainDialog1(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel(self)
        self.setCentralWidget(self.label)
        print("a")
        # 加载并转换图片为 QPixmap
        self.pixmap = QPixmap("data/bj.jpg")
        if self.pixmap.isNull():
            print("背景图片加载失败")
        self.label.resize(self.width(), self.height())  # 设置QLabel的尺寸
        self.label.setScaledContents(True)
        # 将背景图片设置为QLabel的内容
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))
        # 监听窗口大小变化事件
        self.resizeEvent = self.on_resize
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        script_directory = os.path.dirname(os.path.abspath(__file__))
        parent_directory = os.path.dirname(script_directory)
        output_file_path1 = os.path.join(parent_directory, "output.txt")
        self.ui.label_2.setText(output_file_path1)
        output_file_path2 = os.path.join(parent_directory, "output.xlsx")
        self.ui.label_3.setText(output_file_path2)
        self.show_excel(output_file_path2)
        self.show_txt(output_file_path1)

    def on_resize(self, event):
        self.label.resize(self.width(), self.height())
        self.label.setPixmap(self.pixmap.scaled(self.label.size(), aspectRatioMode=QtCore.Qt.KeepAspectRatio,
                                                transformMode=QtCore.Qt.SmoothTransformation))

    def show_excel(self, excel_path):
        """
        读取Excel文件并将其内容展示在QTableView中。
        """
        df = pd.read_excel(excel_path)  # 使用pandas读取Excel文件
        model = QStandardItemModel()
        for row in dataframe_to_rows(df, index=False, header=True):
            items = [QStandardItem(str(value)) for value in row]
            model.appendRow(items)
        self.ui.tableView.setModel(model)
        self.ui.tableView.resizeColumnsToContents()  # 调整列宽
        self.ui.tableView.resizeRowsToContents()  # 调整行高

    def show_txt(self, text_path):
        """
        读取文本文件并显示在QTextEdit中。
        """
        with open(text_path, 'r', encoding='ANSI') as file:
            content = file.read()
            self.ui.textEdit.setPlainText(content)
