from PySide6.QtWidgets import QApplication
from bookkeeper.view.expense_view import MainWindow
from bookkeeper.presenter.expense_presenter import ExpensePresenter
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget
from bookkeeper.repository.sqlite_repository import SQLiteRepository
import sys

DB_NAME = './db/test_01.db'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    view = MainWindow()
    model = None  # TODO: здесь должна быть модель

    cat_repo = SQLiteRepository[Category](DB_NAME, Category)
    exp_repo = SQLiteRepository[Expense](DB_NAME, Expense)
    budget_repo = SQLiteRepository[Budget](DB_NAME, Budget)

    window = ExpensePresenter(model, view, cat_repo, exp_repo, budget_repo)  # TODO: передать три репозиториq
    window.show()
    app.exec_()