import random
from PySide6 import QtWidgets
from PySide6.QtCore import Qt

"""
#Схема расположения виджетов на окне
#       MainWindow
#       -- vertical_layout
#           -- ExpensesTable
#           -- Button
"""

class MainWindow(QtWidgets.QWidget):
    greetings = 'Привет! Здравствуйте! Здорово! '\
                'Приветствую! Hi! Hello! Bonjour!'.split()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label = QtWidgets.QLabel()
        self.button = QtWidgets.QPushButton('Нажми меня! ')
        self.button.clicked.connect(self.click)
        #Создадим элемент таблицы
        self.expenses_table = QtWidgets.QTableWidget(4, 20)
        self.expenses_table.setColumnCount(4)
        self.expenses_table.setRowCount(20)
        self.expenses_table.setHorizontalHeaderLabels(
            "Дата Сумма Категория Комментарий".split())
        self.header = self.expenses_table.horizontalHeader()
        self.header.setSectionResizeMode(
            0, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            1, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            2, QtWidgets.QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(
            3, QtWidgets.QHeaderView.Stretch)
        self.expenses_table.setEditTriggers(
            QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expenses_table.verticalHeader().hide()

        #Добавляем элементы на слой
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.addWidget(self.label)
        self.vbox.addWidget(self.button)
        self.vbox.addWidget(self.expenses_table)
        self.setLayout(self.vbox)

    def click(self):
        self.label.setText(random.choice(self.greetings))
        self.set_data([[1,2,3,4]])

    def set_data(self, data: list[list[str]]):
        for i, row in enumerate(data):
            for j, x in enumerate(row):
                self.expenses_table.setItem(
                    i, j,
                    QtWidgets.QTableWidgetItem(x)
                )