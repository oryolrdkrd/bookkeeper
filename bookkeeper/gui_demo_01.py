"""
Демонстрация TableView на основе https://www.pythonguis.com/tutorials/qtableview-modelviews-numpy-pandas/
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QPushButton, QVBoxLayout, QLabel, QLineEdit, QWidget
from PySide6.QtCore import Qt

cat_repo = SQLiteRepository[Category]('./db/test.db', Category)  # TODO: репозиторий sqlite пока не реализован


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("My App")

        self.label = QLabel()

        self.input = QLineEdit()
        self.input.textChanged.connect(self.label.setText)

        #Добавление тестовой кнопки
        self.test_button = QPushButton('Тест')
        self.test_button.clicked.connect(self.show_grid)

        #Формирование таблицы с данными
        self.table = QtWidgets.QTableView()
        data = cat_repo.get_all()
        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.input)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.test_button)


        self.container = QWidget()
        self.container.setLayout(self.layout)

        self.setCentralWidget(self.container)

    def show_grid(self):
        self.layout.addWidget(self.table)



app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()
