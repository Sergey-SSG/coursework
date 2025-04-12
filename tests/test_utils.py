from datetime import datetime
from unittest.mock import patch

import pandas as pd
import pytest

from dotenv import load_dotenv

from src.utils import (
    get_time_for_greeting,
    get_time_date,
    slice_period,
    convert_to_rub,
    get_price_stocks,
    PATH_TO_FILE,
)

# Load environment variables for testing
load_dotenv("../.env")

# ---- Mock Data and Constants for Testing ----
TEST_API_URL = "https://test.apilayer.com/exchangerates_data"
TEST_API_KEY_EXCHANGE = "test_exchange_api_key"
TEST_API_URL_STOCKS = "https://test.twelvedata.com"
TEST_API_KEY_STOCKS = "test_stocks_api_key"


# ---- Tests for Individual Functions ----
def test_get_time_for_greeting():
    now = datetime.now()
    hour = now.hour
    if 5 <= hour < 12:
        assert get_time_for_greeting() == "Доброе утро"
    elif 12 <= hour < 18:
        assert get_time_for_greeting() == "Добрый день"
    elif 18 <= hour < 22:
        assert get_time_for_greeting() == "Добрый вечер"
    else:
        assert get_time_for_greeting() == "Доброй ночи"


def test_get_time_date():
    date_time = "2023-10-26 12:34:56"
    start_date, end_date = get_time_date(date_time)
    assert start_date == "01.10.2023 00:00:00"
    assert end_date == "26.10.2023 12:34:56"


@patch("pandas.read_excel")
def test_slice_period(mock_read_excel, mock_excel_data):
    mock_read_excel.return_value = mock_excel_data
    period_date = ["01.05.2024 00:00:00", "31.05.2024 23:59:59"]
    sorted_df, sorted_sales, top_transactions = slice_period(
        PATH_TO_FILE, period_date
    )
    assert isinstance(sorted_df, pd.DataFrame)
    assert isinstance(sorted_sales, pd.DataFrame)
    assert isinstance(top_transactions, pd.DataFrame)
    assert len(top_transactions) == 3  # Number of transactions in mock data


@patch("requests.get")
def test_convert_to_rub(mock_get, mock_exchange_rates_response):
    mock_get.return_value.json.return_value = mock_exchange_rates_response
    mock_get.return_value.raise_for_status.return_value = None  # Mock raise_for_status
    rates = convert_to_rub()
    assert isinstance(rates, list)
    assert len(rates) == 2
    assert rates[0]["currency"] == "USD"
    assert rates[0]["rate"] == 80.0


@patch("requests.get")
def test_get_price_stocks(mock_get, mock_stock_prices_response):
    mock_get.return_value.json.return_value = {
        "status": "ok",
        **mock_stock_prices_response,
    }  # Mock successful response
    mock_get.return_value.raise_for_status.return_value = None  # Mock raise_for_status
    prices = get_price_stocks()
    assert isinstance(prices, list)
    assert len(prices) == 5
    assert prices[0]["stock"] == "AAPL"
    assert prices[0]["price"] == 150.00


if __name__ == "__main__":
    pytest.main()
