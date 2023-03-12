"""
Описан класс, представляющий собой бюджет
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class Budget:
    """
    Бюджет>.
    amount_day_limit - сумма дневного ограничения
    amount_week_limit - сумма недельного ограничения
    amount_month_limit - сумма недельного ограничения
    month - месяц, к которому применяются ограничения, устанавливается по первому дню месяца
    pk - id записи в базе данных
    """
    amount_day_limit: float = 0.0
    amount_week_limit: float = 0.0
    amount_month_limit: float = 0.0
    month: str = ''
    year: str = ''
    pk: int = 0