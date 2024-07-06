import os
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QDialog
from openpyxl.utils.dataframe import dataframe_to_rows
from app.secondui import Ui_Dialog
import pandas as pd


class MainDialog1(QDialog):
    def __init__(self):
        super().__init__()
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
