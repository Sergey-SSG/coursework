import json
import pytest
from src.services import search_transactions


def test_search_by_category(transactions_df):
    result = search_transactions(transactions_df, 'Супермаркеты')
    expected_result = [
        {'Дата платежа': '27.06.2021', 'Категория': 'Супермаркеты',
         'Описание': 'Дикси', 'Бонусы (включая кэшбэк)': 5}
    ]
    assert json.loads(result) == expected_result


def test_search_by_description(transactions_df):
    result = search_transactions(transactions_df, 'Дом и ремонт')
    expected_result = [
        {'Дата платежа': '28.12.2021', 'Категория': 'Дом и ремонт',
         'Описание': 'Галамарт', 'Бонусы (включая кэшбэк)': 2}
    ]
    assert json.loads(result) == expected_result


def test_no_results(transactions_df):
    result = search_transactions(transactions_df, 'nonexistent')
    expected_result = []
    assert json.loads(result) == expected_result


if __name__ == "__main__":
    pytest.main()
