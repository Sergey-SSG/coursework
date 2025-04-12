import logging
from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd

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
        def wrapper(*args, **kwargs):
            # Вызов функции для получения отчета
            result = func(*args, **kwargs)
            # Определяем имя файла
            report_filename = filename or f"report_{func.__name__}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            # Запись результата в файл
            try:
                with open(report_filename, "w", encoding="utf-8") as file:
                    file.write(str(result))
                logger.info(f"Отчет сохранен в {report_filename}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении отчета: {e}")
            return result

        return wrapper

    return decorator


# Пример использования декоратора
@report_decorator(filename="mylog.txt")
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> float:
    # Если дата не передана, используем текущую дату
    if date is None:
        date = datetime.now()
        logger.info("Дата не указана, используется текущая дата: %s", date)
    else:
        # Преобразуем дату в формат datetime
        date = pd.to_datetime(date, dayfirst=True)
        logger.info("Использование предоставленной даты: %s", date)

    # Определяем дату три месяца назад
    three_months_ago = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], format="%d.%m.%Y %H:%M:%S")

    # Фильтруем дата фрейм по дате и категории
    filtered_df = transactions[
        (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]

    # Суммируем траты по заданной категории
    total_expenses = filtered_df["Сумма операции"].sum()
    logger.info(f"Сформированный отчет для категории: {category}, общий расход: {total_expenses}")

    return total_expenses
