import datetime

from bookkeeper.models.expense import Expense

class ExpensePresenter:

    def __init__(self, model, view, cat_repo, exp_repo):
        self.model = model
        self.view = view
        self.exp_repo = exp_repo
        self.exp_data = None
        self.cat_data = cat_repo.get_all()  # TODO: implement update_cat_data() similar to update_expense_data()
        self.view.on_expense_add_button_clicked(self.handle_expense_add_button_clicked)
        self.view.on_category_edit_button_clicked(self.handle_category_edit_button_clicked)


    def update_expense_data(self):
        self.exp_data = self.exp_repo.get_all()
        for e in self.exp_data: #TODO: "TypeError: 'NoneType' object is not iterable" on empty DB
            for c in self.cat_data:
                if c.pk == e.category:
                    e.category = c.name
                    break
        self.view.set_expense_table(self.exp_data)

    def show(self):
        self.view.show()
        self.update_expense_data()
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

    def handle_category_edit_button_clicked(self):
        self.view.show_cats_dialog(self.cat_data)