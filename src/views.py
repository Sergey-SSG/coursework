from src.utils import get_time_for_grating, get_time_date, slice_period, PATH_TO_FILE, convert_to_rub, get_price_stocks
from typing import Union


def main_infor(date: str):
    grating = get_time_for_grating()
    print(grating)

    time_start, time_end = get_time_date(date)
    print(time_start, time_end)

    sorted_df = slice_period(PATH_TO_FILE, [time_start, time_end])
    print(sorted_df)

    # print("\nconvert_eur_rub:", convert_to_rub("100", "EUR"), "rub.")
    # print("\nconvert_usd_rub:", convert_to_rub("100", "USD"), "rub.")
    print(get_price_stocks())