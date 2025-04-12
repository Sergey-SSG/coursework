import pandas as pd
import pytest
from src.reports import spending_by_category


def test_spending_by_category_valid_date(mock_transactions):
    total_spending = spending_by_category(
        mock_transactions, category="Супермаркеты", date="30.04.2024 00:00:00"
    )
    assert total_spending == 300.0


def test_spending_by_category_no_transactions(mock_transactions):
    total_spending = spending_by_category(
        mock_transactions, category="NonExistentCategory", date="30.04.2024 00:00:00"
    )
    assert total_spending == 0.0


def test_spending_by_category_empty_transactions():
    empty_transactions = pd.DataFrame(
        columns=["Дата операции", "Категория", "Сумма операции"]
    )

    total_spending = spending_by_category(
        empty_transactions, category="Супермаркеты", date="30.04.2024 00:00:00"
    )
    assert total_spending == 0.0


if __name__ == "__main__":
    pytest.main()
