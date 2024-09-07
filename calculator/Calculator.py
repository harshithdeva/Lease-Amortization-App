from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar
import csv
import os
from local_config import PATH


def split_rent_calculator(month_rent_list, rent_list):
    previous_month_rent = month_rent_list[-2]
    split_rent = rent_list[-1] - previous_month_rent
    return split_rent


def get_last_day(month, year):
    last_day = calendar.monthrange(year, month)
    last_day = list(last_day)
    return last_day[1]


def total_rent_for_month(rent, last_day, start_date):
    last_day = int(last_day)
    due_day = start_date.strftime("%d")
    due_day = int(due_day)
    month_rent = (rent / last_day) * (last_day - due_day)
    return round(month_rent)


def rent_hike_date(start_date, end_dates):
    hike_dates = list()
    while start_date < end_dates:
        hike_dates.append(start_date + relativedelta(years=1))
        start_date = start_date + relativedelta(years=1)
    return hike_dates


def calculate_first_month_rent(start_date, rent):
    last_day = get_last_day(start_date.month, start_date.year)
    month_rent = total_rent_for_month(rent, last_day, start_date)
    return month_rent, last_day


def calculate_rent(start_date, end_dates, rent, rate):
    current_date = start_date
    month_rent_list = []
    rent_list = []
    data_list = []
    rent_list.append(rent)
    first_month_rent, f_last_day = calculate_first_month_rent(start_date, rent)
    month_rent_list.append(first_month_rent)
    data_list.append([start_date, "", f_last_day, first_month_rent, "", ""])
    hike_dates = rent_hike_date(start_date, end_dates)

    while current_date < end_dates:
        row_list = []
        current_date = current_date + relativedelta(months=1)
        if current_date in hike_dates:
            rent = rent + (rent * (rate / 100))
            rent = round(rent)
        rent_list.append(rent)
        last_day = get_last_day(current_date.month, current_date.year)
        month_rent = total_rent_for_month(rent, last_day, start_date)
        month_rent_list.append(month_rent)
        split_rent = split_rent_calculator(month_rent_list, rent_list)
        total_rent = split_rent + month_rent
        row_list.append(current_date)
        row_list.append(rent)
        row_list.append(last_day)
        row_list.append(month_rent)
        row_list.append(split_rent)
        row_list.append(total_rent)
        data_list.append(row_list)

    header_list = [
        "Due Date",
        "Rent",
        "Last Day of Month",
        "Month End Rent",
        "Due Day Rent",
        "Total Rent",
    ]
    return header_list, data_list
