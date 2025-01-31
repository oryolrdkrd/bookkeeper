"""
Вспомогательные функции
"""

from typing import Iterable, Iterator
import datetime


def _get_indent(line: str) -> int:
    return len(line) - len(line.lstrip())


def _lines_with_indent(lines: Iterable[str]) -> Iterator[tuple[int, str]]:
    for line in lines:
        if not line or line.isspace():
            continue
        yield _get_indent(line), line.strip()


def read_tree(lines: Iterable[str]) -> list[tuple[str, str | None]]:
    """
    Прочитать структуру дерева из текста на основе отступов. Вернуть список
    пар "потомок-родитель" в порядке топологической сортировки. Родитель
    элемента верхнего уровня - None.

    Пример. Следующий текст:
    parent
        child1
            child2
        child3

    даст такое дерево:
    [('parent', None), ('child1', 'parent'),
     ('child2', 'child1'), ('child3', 'parent')]

    Пустые строки игнорируются.

    Parameters
    ----------
    lines - Итерируемый объект, содержащий строки текста (файл или список строк)

    Returns
    -------
    Список пар "потомок-родитель"
    """
    parents: list[tuple[str | None, int]] = []
    last_indent = -1
    last_name = None
    result: list[tuple[str, str | None]] = []
    for i, (indent, name) in enumerate(_lines_with_indent(lines)):
        if indent > last_indent:
            parents.append((last_name, last_indent))
        elif indent < last_indent:
            while indent < last_indent:
                _, last_indent = parents.pop()
            if indent != last_indent:
                raise IndentationError(
                    f'unindent does not match any outer indentation '
                    f'level in line {i}:\n'
                )
        result.append((name, parents[-1][0]))
        last_name = name
        last_indent = indent
    return result

def get_start_end_week(date:str) -> list[str]:
    """Функция получения начальной и конечной даты недели
    по передаваемой дате"""
    d = date.split('-')
    date_date = datetime.datetime.strptime(date,'%Y-%m-%d')
    sdt = datetime.datetime.fromisocalendar(int(d[0]), date_date.isocalendar()[1], 1)
    edt = datetime.datetime.fromisocalendar(int(d[0]), date_date.isocalendar()[1], 7)
    if int(edt.strftime("%m"))+1 == 13:
        nmonth = '01'
    else:
        if len(str(int(edt.strftime("%m"))+1)) == 1:
            nmonth = '0' + str(int(edt.strftime("%m")) + 1)
        else:
            nmonth = str(int(edt.strftime("%m"))+1)
    d[1] = nmonth
    print(f"месяц {d[0]+'-'+d[1]+'-'+d[2]}")
    return [datetime.datetime.strftime(sdt,'%Y-%m-%d'), datetime.datetime.strftime(edt,'%Y-%m-%d'),d[0]+'-'+d[1]+'-'+d[2]]
