import pandas as pd

from datetime import datetime
from typing import Optional
from src.utils import PATH_TO_FILE
from functools import wraps


def report_decorator(filename=None):
    """ Декоратор для функций-отчетов, который записывает в файл результат,
    который возвращает функция, формирующая отчет."""

    def decorator(func):
        @wraps(func)
        def wrapper(filename=None, *args, **kwargs):
            # Вызов функции для получения отчета
            report_data = func(*args, **kwargs)

            # Определение имени файла
            if filename is None:
                filename = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            # Запись данных отчета в файл
            with open(filename, 'w', encoding='utf-8') as file:
                file.write(report_data)

            return report_data  # Возвращаем данные отчета

        return wrapper

    return decorator if filename is not None else decorator(None)


# Пример использования декоратора

@report_decorator(filename="mylog.txt")
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    # Если дата не передана, используем текущую дату
    if date is None:
        date = datetime.now()

    # Преобразуем дату в формат datetime
    date = pd.to_datetime(date)

    # Определяем дату три месяца назад
    three_months_ago = date - pd.DateOffset(months=3)

    # Фильтруем датафрейм по дате и категории
    filtered_df = transactions[
        (transactions['Дата платежа'] >= three_months_ago) &
        (transactions['Дата платежа'] <= date) &
        (transactions['Категория'] == category)
        ]

    # Суммируем траты по заданной категории
    total_expenses = filtered_df['Сумма платежа'].sum()

    return total_expenses


if __name__ == "__main__":
    transactions = pd.read_excel(PATH_TO_FILE)
    print(spending_by_category(transactions, "Каршеринг", "31.12.2021"))
