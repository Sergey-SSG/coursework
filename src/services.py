import json
import logging

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

    logger.debug(f"Начинаем поиск: {search_string}")

    # Фильтруем датафрейм по описанию и категории
    filtered_df = transactions_df[
        (transactions_df["Описание"].str.contains(search_string, case=False, na=False))
        | (transactions_df["Категория"].str.contains(search_string, case=False, na=False))
    ]

    logger.debug(f"Количество найденных транзакций: {len(filtered_df)}")

    # Преобразуем отфильтрованный датафрейм в список словарей
    transactions_list = filtered_df.to_dict(orient="records")

    # Формируем JSON-ответ
    json_response = json.dumps(transactions_list, ensure_ascii=False, indent=4)

    return json_response
