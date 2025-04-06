from pprint import pprint
from src.views import main_infor

# from src.reports import spending_by_category
# from src.services import search_transactions

if __name__ == '__main__':
    date_request = "2018-05-20 15:30:00"
    result_views = main_infor(date_request)
    pprint(result_views)

    result_reports = ''
    pprint(result_reports)
