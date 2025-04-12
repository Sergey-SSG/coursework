import json

from src.utils import (PATH_TO_FILE, convert_to_rub, get_price_stocks, get_time_date, get_time_for_greeting,
                       slice_period)


def main_info(date: str) -> str:
    """Функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ."""
    greeting = get_time_for_greeting()
    time_start, time_end = get_time_date(date)
    sorted_df, sorted_sales, top_transactions = slice_period(PATH_TO_FILE, [time_start, time_end])

    cards_data = []
    for card, data in sorted_sales.iterrows():
        last_digits = str(card)[-4:]  # Извлечь последние 4 цифры номера карты
        total_spent = round(data["Сумма операции с округлением"], 2)  # Округление до сотых
        cashback = round(data["Кэшбэк"], 2)  # Округление до сотых
        cards_data.append({
            "last_digits": last_digits,
            "total_spent": total_spent,
            "cashback": cashback
        })

    top_transactions_data = []
    for _, row in top_transactions.iterrows():  # Итерация по строкам таблицы
        date = row["Дата операции"].strftime("%d.%m.%Y")
        amount = round(row["Сумма операции с округлением"], 2)
        category = row["Категория"]
        description = row["Описание"]
        top_transactions_data.append({
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        })

    currency_rates = convert_to_rub()

    stock_prices = get_price_stocks()

    response_data = {
        "greeting": greeting,
        "cards": cards_data,
        "top_transactions": top_transactions_data,
        "currency_rates": currency_rates,
        "stock_prices": stock_prices
    }

    return json.dumps(response_data, indent=4, ensure_ascii=False)
