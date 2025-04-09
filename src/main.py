import pandas as pd
from src.views import main_info
from src.utils import PATH_TO_FILE
from src.reports import spending_by_category
from src.services import search_transactions

if __name__ == '__main__':
    date_request = "2018-05-20 15:30:00"
    result_views = main_info(date_request)
    print(result_views)

    transactions_data = pd.read_excel(PATH_TO_FILE)
    transactions_df = pd.DataFrame(transactions_data)
    print(search_transactions(transactions_df, 'Дом и ремонт'))

    transactions = pd.read_excel(PATH_TO_FILE)
    print(spending_by_category(transactions, "Каршеринг", "31.12.2021"))
