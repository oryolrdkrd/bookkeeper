"""
Модуль описывает репозиторий, работающий в c БД
"""
from inspect import get_annotations
from bookkeeper.repository.abstract_repository import AbstractRepository, T
from itertools import count
from typing import Any
import sqlite3

class SQLiteRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий c БД SQLite
    """

    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str=True)
            # RO: получили список полей БД, их будем использовать в запросах
        self.fields.pop('pk')
        self._container: dict[int, T] = {}
            # RO: ??? Это значения из передаваемых объектов
        self._counter = count(1)

    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут pk.
        """
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        req = ""+"insert into "+self.table_name+" ("+names+") values ("+p+")"""
        values = [getattr(obj, x) for x in self.fields]
        data = (getattr(obj, 'name', None), getattr(obj, 'parent', None))
            #RO: Получил данные из объекта для вставки
        try:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                cur.execute(req, values)
                obj.pk = cur.lastrowid
            con.close()
        except (sqlite3.Error, sqlite3.Warning) as err:
                print("Ошибка:", err)
        return obj.pk

    def get(self, pk: int) -> T | None:
        pass

    def get_all(self, where: dict[str, Any] | None = None) -> list[T]:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """
        if where is None:
            try:
                with sqlite3.connect(self.db_file) as con:
                    cur = con.cursor()
                    cur.execute("""SELECT * FROM Category""")
                print(cur.fetchall())
                return list(cur.fetchall())
                con.close()
            except (sqlite3.Error, sqlite3.Warning) as err:
                print("Ошибка:", err)
        try:
            with sqlite3.connect(self.db_file) as con:
                cur = con.cursor()
                #req = "" + "SELECT * FROM " + self.table_name + "WHERE (" + where + "=" + where.+")"""
                cur.execute("""SELECT * FROM Category WHERE """)
            print(cur.fetchall())
            return list(cur.fetchall())
            con.close()
        except (sqlite3.Error, sqlite3.Warning) as err:
            print("Ошибка:", err)

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        pass

    def delete(self, pk: int) -> None:
        pass
