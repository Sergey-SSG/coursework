from src.reports import spending_by_category


def test_spending_by_category_no_date(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты")
    assert result == -756  # Ожидаемая сумма за последние три месяца


def test_get_spending_by_category_with_date(sample_transactions):
    result = spending_by_category(sample_transactions, "Супермаркеты", "28.12.2021")
    assert result == -595  # Ожидаемая сумма за период до 2023-03-01


def test_get_spending_by_category_empty_category(sample_transactions):
    result = spending_by_category(sample_transactions, "nonexistent")
    assert result == 0  # Ожидаемая сумма для несуществующей категории
