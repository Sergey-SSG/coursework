import logging
from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd

from src.utils import PATH_TO_FILE

# Настройка логирования
logging.basicConfig(
    filename="../logs/reports.log",
    encoding="utf-8",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("reports")


def report_decorator(filename=None):
    """Декоратор для функций-отчетов, который записывает в файл результат,
    который возвращает функция, формирующая отчет."""

    def decorator(func):
        @wraps(func)
        def wrapper(filename=None, *args, **kwargs):
            # Вызов функции для получения отчета
            result = func(*args, **kwargs)

            # Определяем имя файла
            if filename is None:
                filename = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                # filename = f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

            # Запись результата в файл
            with open(filename, "w", encoding="utf-8") as file:
                file.write(str(result))

            logging.INFO(f"Отчет сохранен в {filename}")
            return result

        return wrapper

    return decorator
    # return decorator if filename is not None else decorator(None)


# Пример использования декоратора
@report_decorator(filename="mylog.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    # Если дата не передана, используем текущую дату
    if date is None:
        date = datetime.now()
        logging.INFO("Дата не указана, используется текущая дата: %s", date)
    else:
        # Преобразуем дату в формат datetime
        date = pd.to_datetime(date)
        logging.INFO("Использование предоставленной даты: %s", date)

    # Определяем дату три месяца назад
    three_months_ago = date - pd.DateOffset(months=3)

    # Фильтруем дата фрейм по дате и категории
    filtered_df = transactions[
        (transactions["Дата платежа"] >= three_months_ago)
        & (transactions["Дата платежа"] <= date)
        & (transactions["Категория"] == category)
    ]

    # Суммируем траты по заданной категории
    total_expenses = filtered_df["Сумма платежа"].sum()
    logging.INFO(f"Сформированный отчет для категории: {category}, общий расход: {total_expenses}")

    return total_expenses


# transactions = pd.read_excel(PATH_TO_FILE)
# transactions_df = pd.DataFrame(transactions)
# print(spending_by_category(transactions_df, "Супермаркеты", "31.12.2021"))
