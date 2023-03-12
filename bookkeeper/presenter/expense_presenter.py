import datetime

from bookkeeper.models.expense import Expense
from bookkeeper.models.budget import Budget

class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo, budget_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.budget_repo = budget_repo
        self.exp_data = None
        self.budget_data = None
        self.header_nums = {}   #Словарь Заголовок таблицы расходов - его индекс
        self.cat_data = cat_repo.get_all()  # TODO: implement update_cat_data() similar to update_expense_data()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_date_datebug_changed(self.handle_budget_add_button_clicked)
        self.view.on_category_edit_button_clicked(self.handle_category_edit_button_clicked)
        self.view.expenses_grid.customContextMenuRequested.connect(
            lambda pos, table=self.view.expenses_grid: self.view.context(pos, table,
                lambda: self.delete_row_exp()))

    def delete_row_exp(self) -> None:
        row = self.view.expenses_grid.currentIndex().row()
        self.exp_repo.delete( self.view.expenses_grid.model().index(row, 5).data()) #TODO Забирать индекс столбца с pk автоматом
        self.update_expense_data()

    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        for e in self.exp_data: #TODO: "TypeError: 'NoneType' object is not iterable" on empty DB
            for c in self.cat_data:
                if c.pk == e.category:
                    e.category = c.name
                    break
        print(self.exp_data)
        self.view.set_expense_table(self.exp_data)

    def update_budget_data(self):
        #self.budget_data = self.budget_repo.get_all()
        budget_data = self.budget_repo.get_all({'find_obj':'*','month':str(int(self.view.get_date_bug()[5:7])), 'AND':'', 'year':self.view.get_date_bug()[0:4]})
        #budget_data = self.budget_repo.get_all({'find_obj': '*', 'year': self.view.get_date_bug()[0:4]})
        a = self.exp_repo.get_all({'find_obj':'sum(amount)','expense_date':self.view.get_date_bug()})[0].pk
        print(f'a = {a}')
        b = Budget(amount_day_limit=self.exp_repo.get_all({'find_obj':'sum(amount)','expense_date':self.view.get_date_bug()})[0].pk,
                   amount_week_limit='7000', amount_month_limit='28000', month=None, pk=1)
        #TODO Добавить данные недельного и месячного расходов
        """
        SELECT 
        sum(case when expense_date = '2023-03-12' then  amount end ) as SUM_DAY
        ,sum(case when expense_date between  date('2023-03-10', 'weekday 0','1 days') and date('2023-03-10', 'weekday 6','1 days') then  amount end ) as SUM_week
        ,sum(case when expense_date between  date('2023-03-12', 'start of month') and date('2023-04-12', 'start of month', '-1 days')  then  amount end ) as SUM_month

        FROM EXPENSE;
 
        SELECT date('2023-03-12', 'weekday 0','1 days'),date('2023-03-10', 'weekday 6','1 days');
        """

        budget_data.append(b)
        print(budget_data)
        self.view.set_budget_table(budget_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
        self.update_budget_data()
        self.view.set_category_dropdown(self.cat_data)

    def handle_expense_add_button_clicked(self) -> None:
        cat_pk = self.view.get_selected_cat()
        amount = self.view.get_amount()
        expense_date = self.view.get_date_exp()
        added_date = datetime.datetime.now()
        comment = self.view.get_comment()
        exp = Expense(int(amount), cat_pk, expense_date, added_date.strftime("%y-%m-%d"), comment)
        self.exp_repo.add(exp)
        self.update_expense_data()

    def handle_budget_add_button_clicked(self) -> None:
        self.update_budget_data()

    def handle_category_edit_button_clicked(self):
        self.view.show_cats_dialog(self.cat_data)

