import pandas as pd
import pytest


@pytest.fixture
def transactions_df():
    # Подготовка данных для тестов
    data = {
        "Дата платежа": ["27.06.2021", "28.12.2021"],
        "Категория": ["Супермаркеты", "Дом и ремонт"],
        "Описание": ["Дикси", "Галамарт"],
        "Бонусы (включая кэшбэк)": [5, 2],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_transactions():
    data = {
        "Дата операции": [
            "01.05.2024 10:00:00",
            "15.04.2024 14:30:00",
            "20.03.2024 18:00:00",
            "10.02.2024 09:00:00",
        ],
        "Категория": ["Супермаркеты", "Супермаркеты", "Рестораны", "Супермаркеты"],
        "Сумма операции": [150.0, 200.0, 300.0, 100.0],
    }
    return pd.DataFrame(data)


@pytest.fixture
def mock_exchange_rates_response():
    return {
        "success": True,
        "terms": "https://apilayer.com/terms",
        "privacy": "https://apilayer.com/privacy",
        "query": {"from": "USD", "to": "RUB", "amount": 1},
        "info": {"timestamp": 1685000000, "rate": 80.0},
        "result": 80.0,
    }


# Mock response for stock prices API
@pytest.fixture
def mock_stock_prices_response():
    return {
        "symbol": "AAPL",
        "name": "Apple Inc",
        "exchange": "NASDAQ",
        "country": "US",
        "currency": "USD",
        "price": 150.00,
        "timestamp": 1685000000,
    }


# Mock data for the Excel file
@pytest.fixture
def mock_excel_data():
    data = {
        "Дата операции": [
            "2024-05-01 10:00:00",
            "2024-05-15 14:30:00",
            "2024-05-20 18:00:00",
        ],
        "Номер карты": ["1234567890123456", "1234567890123456", "9876543210987654"],
        "Сумма операции с округлением": [150, 200, 300],
        "Категория": ["Супермаркеты", "Рестораны", "Транспорт"],
        "Описание": ["Пятерочка", "Макдональдс", "Яндекс.Такси"],
    }
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"])
    return df
