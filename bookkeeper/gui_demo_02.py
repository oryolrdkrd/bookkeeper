"""
Демонстрация TreeView на основе http://pharma-sas.com/common-manipulation-of-qtreeview-using-pyqt5/
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

import sys
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

import sys
from collections import deque
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtCore import *


class view(QWidget):
    def __init__(self, data):
        super(view, self).__init__()
        self.tree = QTreeView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.tree)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Name', 'Height', 'Weight'])
        self.tree.header().setDefaultSectionSize(180)
        self.tree.setModel(self.model)
        self.importData(data)
        self.tree.expandAll()


    def importData(self, data, root=None):
        self.model.setRowCount(0)
        if root is None:
            root = self.model.invisibleRootItem()
        seen = {}   # List of  QStandardItem
        values = deque(data)
        while values:
            value = values.popleft()
            if value['unique_id'] == 1:
                parent = root
            else:
                pid = value['parent_id']
                if pid not in seen:
                    values.append(value)
                    continue
                parent = seen[pid]
            unique_id = value['unique_id']
            parent.appendRow([
                QStandardItem(value['short_name']),
                #QStandardItem(value['height']),  # TODO: убрать лишние поля
                #QStandardItem(value['weight'])
            ])
            seen[unique_id] = parent.child(parent.rowCount() - 1)


if __name__ == '__main__':
    cat_repo = SQLiteRepository[Category]('./db/test.db', Category)  # TODO: репозиторий sqlite пока не реализован

    data = [{'unique_id': pk, 'short_name': name, 'parent_id': pid} for pk, name, pid in cat_repo.get_all()]
    data = data[:4]  # TODO: выяснить причину зависания на полном списке категорий
    print(data)
 #   data = [
 #       {'unique_id': 1, 'parent_id': 0, 'short_name':  'test test'},
 #       {'unique_id': 2, 'parent_id': 1, 'short_name':  'test test'},
 #       {'unique_id': 3, 'parent_id': 2, 'short_name':  'test test'},
 #       {'unique_id': 4, 'parent_id': 2, 'short_name':  'test test'},
 #       {'unique_id': 5, 'parent_id': 1, 'short_name':  'test test'},
 #       {'unique_id': 6, 'parent_id': 5, 'short_name':  'test test'},
 #       {'unique_id': 7, 'parent_id': 5, 'short_name':  'test test'},
 #       {'unique_id': 8, 'parent_id': 1, 'short_name':  'test test'},
 #       {'unique_id': 9, 'parent_id': 8, 'short_name':  'test test'},
 #       {'unique_id': 10, 'parent_id': 8, 'short_name': 'test test'},
 #   ]
    app = QApplication(sys.argv)
    view = view(data)
    view.setGeometry(300, 100, 600, 300)
    view.setWindowTitle('QTreeview Example')
    view.show()
    sys.exit(app.exec_())