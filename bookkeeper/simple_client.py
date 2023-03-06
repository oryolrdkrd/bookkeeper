"""
Простой тестовый скрипт для терминала
"""

from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense
from bookkeeper.repository.memory_repository import MemoryRepository
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import read_tree

cat_repo = MemoryRepository[Category]()
exp_repo = MemoryRepository[Expense]()

cat_repo_sql = SQLiteRepository[Category]("./repository/test.db", Category)

cats = '''
продукты
    мясо
        сырое мясо
        мясные продукты
    сладости
книги
одежда
'''.splitlines()

Category.create_from_tree(read_tree(cats), cat_repo)

while True:
    try:
        cmd = input('$> ')
    except EOFError:
        break
    if not cmd:
        continue
    if cmd == 'категории':
        print(*cat_repo.get_all(), sep='\n')
    elif cmd == 'расходы':
        print(*exp_repo.get_all(), sep='\n')
    #RO: Мой блок тестовых команд методов класса Category
    #RO: Создаю категории из заданного списка в SQL репо
    elif cmd == 'SQL_load_cat_from_list':
        Category.create_from_tree(read_tree(cats), cat_repo_sql)
    #RO: очистка таблицы от записей
    elif cmd == 'SQL_clean_db':
        pass
    # RO: добавление категорий
    elif cmd == 'SQL_add_cat':
        try:
            cmd = input('Введите категорию: ')
        except EOFError:
            break
        if not cmd:
            continue
        Category.name = cmd
        try:
            cmd = input('Введите номер родителя: ')
        except EOFError:
            break
        if not cmd:
            continue
        Category.parent = int(cmd)
        cat_repo_sql.add(Category)
    # RO: получение всех категорий
    elif cmd == 'SQL_get_all':
        cat_repo_sql.get_all()
    #RO: очистка таблицы от записей
    elif cmd == 'SQL_clean_db':
        pass
    elif cmd[0].isdecimal():
        amount, name = cmd.split(maxsplit=1)
        try:
            cat = cat_repo.get_all({'name': name})[0]
        except IndexError:
            print(f'категория {name} не найдена')
            continue
        exp = Expense(int(amount), cat.pk)
        exp_repo.add(exp)
        print(exp)
