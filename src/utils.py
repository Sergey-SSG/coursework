import json
import os
from datetime import datetime

import pandas as pd
import requests
from dotenv import load_dotenv

PATH_TO_FILE = "../data/operations.xlsx"


def get_time_for_greeting() -> str:
    """функцию, принимающую на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращает приветствие"""
    user_date_time = datetime.now()
    user_hour = user_date_time.hour
    if 5 <= user_hour < 12:
        return "Доброе утро"
    elif 12 <= user_hour < 18:
        return "Добрый день"
    elif 18 <= user_hour < 22:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_time_date(date_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> tuple[str, str]:
    """Функция для страницы «Главная» принимает на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращает период в виде списка строк"""
    format_date = datetime.strptime(date_time, date_format)
    # Преобразование 01.05.2018 : 00:00:00, 20.05.2018 : 15:30:00
    start_day = format_date.replace(day=1, hour=0, minute=0, second=0)
    date_format_output = "%d.%m.%Y %H:%M:%S"
    return start_day.strftime(date_format_output), format_date.strftime(date_format_output)


def slice_period(path_to_file: str, period_date: list):
    """Функция для страницы «Главная» извлекает детали транзакций для каждой карты:
    - последние 4 цифры карты;
    - общие расходы;
    - Кэшбэк (1 рубль за каждые 100 рублей расхода);
    - 5 лучших транзакций по сумме платежа."""
    df = pd.read_excel(path_to_file, "Отчет по операциям")
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    start_date = datetime.strptime(period_date[0], "%d.%m.%Y %H:%M:%S")
    end_date = datetime.strptime(period_date[1], "%d.%m.%Y %H:%M:%S")
    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]
    sorted_df = filtered_df.sort_values(by="Дата операции")

    # последние 4 цифры карты, общие расходы, Кэшбэк (1 рубль за каждые 100 рублей расхода
    filtered_df.loc[:, "Кэшбэк"] = filtered_df["Сумма операции с округлением"] // 100
    sales_by_card = filtered_df.groupby("Номер карты")[["Сумма операции с округлением", "Кэшбэк"]].sum()
    sorted_sales = sales_by_card.sort_values(by="Сумма операции с округлением", ascending=False)

    # Сортировка и получение 5 лучших транзакций
    top_transactions = filtered_df.sort_values(by="Сумма операции с округлением", ascending=False).head(5)
    return sorted_df, sorted_sales, top_transactions


load_dotenv("../.env")

API_URL = "https://api.apilayer.com/exchangerates_data"
headers = {"apikey": os.getenv("API_KEY_exchange")}


def convert_to_rub() -> str:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных —
    float. Если транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и
    конвертации суммы операции в рубли."""
    currency_list = ["USD", "EUR"]
    convert_to = "RUB"
    new_currency_list = []

    for currency in currency_list:
        response = requests.get(f"{API_URL}/convert?from={currency}&to={convert_to}&amount=1", headers=headers)

        response.raise_for_status()
        conversion_data = response.json()
        currency_value = conversion_data.get("result")

        if currency_value is not None:
            new_currency_list.append(currency_value)
        else:
            print("Ошибка: ключ 'result' не найден в ответе для:", currency)
    result_json = json.dumps(new_currency_list, indent=4)
    return result_json


API_URL_ = "https://api.twelvedata.com"
API_KEY_stocks = os.getenv("Secret_key")


def get_price_stocks() -> str:
    """Функция, которая извлекает цены акций из списка S&P 500 путем вызова внешнего API."""
    stocks_list = ["AAPL", "AMZN", "GOOGL", "MSFT", "TSLA"]
    price_stocks = []

    for stock in stocks_list:
        response = requests.get(f"{API_URL_}/price?symbol={stock}&apikey={API_KEY_stocks}")
        dict_result = response.json()
        price_element = dict_result.get("price")
        price_stocks.append(price_element)
    result_json = json.dumps(price_stocks, indent=4)
    return result_json
