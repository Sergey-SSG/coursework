import json
from typing import Any, Dict

from src.utils import (PATH_TO_FILE, convert_to_rub, get_price_stocks, get_time_date, get_time_for_greeting,
                       slice_period)


def main_info(date: str) -> Dict[str, Any]:
    """Функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающую JSON-ответ."""
    greeting = get_time_for_greeting()
    time_start, time_end = get_time_date(date)
    print(time_start, time_end)
    sorted_df = slice_period(PATH_TO_FILE, [time_start, time_end])
    print(sorted_df)

    data = {
        "greeting": greeting,
    }

    json_data = json.dumps(data, ensure_ascii=False, indent=4)
    return json_data

    print(f"currency_rates: {convert_to_rub()}")

    print(f"stock_prices: {get_price_stocks()}")
