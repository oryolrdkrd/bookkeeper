from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QComboBox, QLineEdit, QPushButton, QPlainTextEdit
from PySide6 import QtCore, QtWidgets
from PySide6.QtCore import QSize
from PySide6.QtGui import *
from bookkeeper.view.categories_view import CategoryDialog
from bookkeeper.models.budget import Budget


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.header_names = list(data[0].__dataclass_fields__.keys())

    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self.header_names[section]
        return super().headerData(section, orientation, role)

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            fields = list(self._data[index.row()].__dataclass_fields__.keys())
            return self._data[index.row()].__getattribute__(fields[index.column()])

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0].__dataclass_fields__)

    def addData(self, adddata):
        self._data.append(adddata)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #Основные параметры окна
        self.item_model = None
        self.setWindowTitle("Программа для ведения бюджета")

        #Делаем вертикальный Layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(QLabel('Последние расходы'))

        self.expenses_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.expenses_grid)

        #Создадим контекстное меню для таблицы расходов
        self.expenses_grid.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        #self.expenses_grid.customContextMenuRequested.connect(lambda pos, table=self.expenses_grid: self.context(pos, table))

        #Делаю слой для элементов бюджета
        self.budget_controls = QGridLayout()
        #Создаю таблицу вывода бюджета
        self.layout.addWidget(QLabel('Бюджет'))
        self.layout.addWidget(QLabel('Дата бюджета:'))
        self.datebug_line_edit = QtWidgets.QDateEdit()
        self.datebug_line_edit.setCalendarPopup(True)
        self.datebug_line_edit.setDisplayFormat("yyyy-MM-dd")
        self.datebug_line_edit.setDate(QtCore.QDate.currentDate())
        self.layout.addWidget(self.datebug_line_edit)

        self.budget_grid = QtWidgets.QTableView()
        self.layout.addWidget(self.budget_grid)

        self.bottom_controls = QGridLayout()

        # Добавляю поле ввода даты, на которую отнесен расход
        self.bottom_controls.addWidget(QLabel('Дата расхода'), 0, 0)
        self.dateexp_line_edit = QtWidgets.QDateEdit()
        self.dateexp_line_edit.setCalendarPopup(True)
        self.dateexp_line_edit.setDisplayFormat("yyyy-MM-dd")
        self.dateexp_line_edit.setDate(QtCore.QDate.currentDate())
        self.bottom_controls.addWidget(self.dateexp_line_edit, 0, 1)

        self.bottom_controls.addWidget(QLabel('Сумма'), 1, 0)
        self.amount_line_edit = QLineEdit()
        self.bottom_controls.addWidget(self.amount_line_edit, 1, 1)  # TODO: добавить валидатор

        self.bottom_controls.addWidget(QLabel('Категория'), 2, 0)
        self.category_dropdown = QComboBox()

        self.bottom_controls.addWidget(self.category_dropdown, 2, 1)

        self.category_edit_button = QPushButton('Редактировать')
        self.bottom_controls.addWidget(self.category_edit_button, 2, 2)
        self.category_edit_button.clicked.connect(self.show_cats_dialog)

        #Добавляем комментарий
        self.comment_edit = QPlainTextEdit()
        self.comment_edit.setGeometry(30, 30, 30, 30)
        self.bottom_controls.addWidget(QLabel('Комментарий'), 3, 0)
        self.bottom_controls.addWidget(self.comment_edit, 3, 1)

        self.expense_add_button = QPushButton('Добавить')
        self.bottom_controls.addWidget(self.expense_add_button, 4, 1)

        self.bottom_widget = QWidget()
        self.bottom_widget.setLayout(self.bottom_controls)

        self.layout.addWidget(self.bottom_widget)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)

        self.setCentralWidget(self.widget)

    def set_expense_table(self, data):
        if data:
            self.item_model = TableModel(data)
            self.expenses_grid.setModel(self.item_model)
            self.expenses_grid.resizeColumnsToContents()
            grid_width = sum([self.expenses_grid.columnWidth(x) for x in range(0, self.item_model.columnCount(0) + 1)])
            self.setFixedSize(grid_width + 80, 600)

    def set_budget_table(self, data):
        if data:
            self.item_model = TableModel(data)
            self.budget_grid.setModel(self.item_model)
            self.budget_grid.resizeColumnsToContents()
            grid_width = sum([self.budget_grid.columnWidth(x) for x in range(0, self.item_model.columnCount(0) + 1)])
            self.setFixedSize(grid_width + 80, 600)
            print('!')
        else:
            self.item_model = TableModel([Budget(amount_day_limit=None, amount_week_limit=None, amount_month_limit=None, month=None,
                    year=None, pk=None)])
            self.budget_grid.setModel(self.item_model)
            self.budget_grid.resizeColumnsToContents()
            grid_width = sum([self.budget_grid.columnWidth(x) for x in range(0, self.item_model.columnCount(0) + 1)])
            self.setFixedSize(grid_width + 80, 600)
            print('+')


    def set_category_dropdown(self, data):
        for c in data:
            self.category_dropdown.addItem(c.name, c.pk)

    def on_expense_add_button_clicked(self, slot):
        self.expense_add_button.clicked.connect(slot)

    def on_date_datebug_changed(self, slot):
        self.datebug_line_edit.dateChanged.connect(slot)

    def get_amount(self) -> float:
        return float(self.amount_line_edit.text())

    def get_date_exp(self) -> str:
        return self.dateexp_line_edit.text()

    def get_date_bug(self) -> str:
        return self.datebug_line_edit.text()

    def get_comment(self) -> str:
        return self.comment_edit.toPlainText()

    def get_selected_cat(self) -> int:
        return self.category_dropdown.itemData(self.category_dropdown.currentIndex())

    def on_category_edit_button_clicked(self, slot):
        self.category_edit_button.clicked.connect(slot)

    def show_cats_dialog(self, data):
        if data:
            cat_dlg = CategoryDialog(data)
            cat_dlg.setWindowTitle('Редактирование категорий')
            cat_dlg.setGeometry(300, 100, 600, 300)
            cat_dlg.exec_()

    def context(self, point, table, slot):
    #Контекстное меню на таблицу расходов
        menu = QtWidgets.QMenu()
        deleteAction = QAction('Удалить расход', menu)
        deleteAction.triggered.connect(slot)
        menu.addAction(deleteAction)
        menu.exec(table.mapToGlobal(point))