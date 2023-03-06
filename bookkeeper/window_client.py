import sys
from PySide6 import QtWidgets
from bookkeeper.view.window_main import MainWindow
from bookkeeper.view.we_expenses import ExpensesWindow

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
expenses = ExpensesWindow()

#Параметры главного окна
window.setWindowTitle('Учет личных финансов')
window.resize(500, 500)
window.show()

sys.exit(app.exec())