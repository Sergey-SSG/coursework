import json
import logging

import pandas as pd

from src.utils import PATH_TO_FILE

# Настройка логирования
logging.basicConfig(
    filename="../logs/services.log",
    encoding="utf-8",
    filemode="w",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)

logger = logging.getLogger("services")


def search_transactions(transactions_df, search_string):
    """Пользователь передает строку для поиска, возвращается JSON-ответ со всеми транзакциями,
    содержащими запрос в описании или категории."""

    logging.DEBUG(f"Начинаем поиск: {search_string}")

    # Фильтруем дата фрейм по описанию и категории
    filtered_df = transactions_df[
        (transactions_df["Описание"].str.contains(search_string, case=False, na=False))
        | (transactions_df["Категория"].str.contains(search_string, case=False, na=False))
    ]

    logging.DEBUG(f"Количество найденных транзакций: {len(filtered_df)}")

    # Преобразуем отфильтрованный дата фрейм в список словарей
    transactions_list = filtered_df.to_dict(orient="records")

    # Формируем JSON-ответ
    json_response = json.dumps(transactions_list, ensure_ascii=False, indent=4)

    return json_response


if __name__ == "__main__":
    transactions_data = pd.read_excel(PATH_TO_FILE)
    transactions_df = pd.DataFrame(transactions_data)
    print(search_transactions(transactions_df, "Дом и ремонт"))
