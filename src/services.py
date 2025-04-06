import json
import logging

# Пример массива транзакций
transactions = [
    {"id": 1, "description": "Покупка кофе", "category": "Еда"},
    {"id": 2, "description": "Оплата за интернет", "category": "Услуги"},
    {"id": 3, "description": "Покупка книги", "category": "Книги"},
    {"id": 4, "description": "Посещение ресторана", "category": "Еда"},
]

def search_transactions(query):
    # Приводим запрос к нижнему регистру для нечувствительного поиска
    query = query.lower()

    # Ищем транзакции, содержащие запрос в описании или категории
    results = [
        transaction for transaction in transactions
        if query in transaction["Описание"].lower() or query in transaction["Категория"].lower()
    ]

    # Возвращаем результаты в формате JSON
    return json.dumps(results)


# Пример использования функции
search_query = "еда"
response = search_transactions(search_query)
print(response)