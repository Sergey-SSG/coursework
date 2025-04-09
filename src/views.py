import json

from src.utils import get_time_for_greeting, get_time_date, slice_period, PATH_TO_FILE, convert_to_rub, get_price_stocks
from typing import Dict, Any


def main_info(date: str) -> Dict[str, Any]:
    """ Функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ."""
    greeting = get_time_for_greeting()
    time_start, time_end = get_time_date(date)
    print(time_start, time_end)
    sorted_df = slice_period(PATH_TO_FILE, [time_start, time_end])
    print(sorted_df)

    data = {
        "greeting": greeting,
        "cards": [],

    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data

    # print(f"currency_rates: {convert_to_rub()}")

    # "currency_rates": [
    #     {
    #         "currency": "USD",
    #         "rate": 73.21
    #     },
    #     {
    #         "currency": "EUR",
    #         "rate": 87.08
    #     }
    # ]

    # print(f"stock_prices: {get_price_stocks()}")

    # "stock_prices": [
    #     {
    #         "stock": "AAPL",
    #         "price": 150.12
    #     },
    #     {
    #         "stock": "AMZN",
    #         "price": 3173.18
    #     },
    #     {
    #         "stock": "GOOGL",
    #         "price": 2742.39
    #     },
    #     {
    #         "stock": "MSFT",
    #         "price": 296.71
    #     },
    #     {
    #         "stock": "TSLA",
    #         "price": 1007.08
    #     }
    # ]
    # }
