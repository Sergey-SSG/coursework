import pandas as pd

from src.reports import spending_by_category
from src.services import search_transactions
from src.utils import PATH_TO_FILE
from src.views import main_info

if __name__ == "__main__":
    date_request = "2018-05-20 15:30:00"
    result_views = main_info(date_request)
    print(result_views)

    transactions_df = pd.read_excel(PATH_TO_FILE)
    print(search_transactions(transactions_df, "Дом и ремонт"))
    print(spending_by_category(transactions_df, "Супермаркеты", "30.12.2021"))
