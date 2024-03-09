from datetime import datetime
from dateutil.relativedelta import relativedelta
import calendar

def split_rent_calculator(month_rent_list,rent_list):
    previous_month_rent = month_rent_list[-2]
    split_rent = rent_list[-1]-previous_month_rent
    return split_rent

def get_last_day(month,year):
    last_day = calendar.monthrange(year,month)
    last_day = list(last_day)
    return last_day[1]


def total_rent_for_month(rent,last_day,start_date):
    last_day = int(last_day)
    due_day = start_date.strftime("%d")
    due_day = int(due_day)
    month_rent = (rent/last_day)*(last_day-due_day)
    return int(round(month_rent))

    
def rent_hike_date(start_date,end_dates):
    hike_dates = list()
    while start_date < end_dates:
        hike_dates.append(start_date+relativedelta(years=1))
        start_date = start_date+relativedelta(years=1)
    return hike_dates

def calculate_first_month_rent(start_date,rent):
    last_day = get_last_day(start_date.month,start_date.year)
    month_rent = total_rent_for_month(rent,last_day,start_date)
    return month_rent,last_day

def calculate_rent(start_date,end_dates,rent,rate):
    current_date = start_date
    month_rent_list = []
    rent_list = []
    rent_list.append(rent)
    first_month_rent,f_last_day = calculate_first_month_rent(start_date,rent)
    month_rent_list.append(first_month_rent)
    print(f"Due Date: {start_date}")
    print(f"Rent: {rent}")
    print(f"Last Day of Month: {f_last_day}")
    print(f"Month End Rent: {first_month_rent}")
    hike_dates = rent_hike_date(start_date, end_dates)

    while current_date < end_dates:
        current_date = current_date+ relativedelta(months=1)
        if current_date in hike_dates:
            rent = rent+(rent*(rate/100))
            rent = int(round(rent))
        rent_list.append(rent)
        last_day = get_last_day(current_date.month,current_date.year)
        month_rent = total_rent_for_month(rent,last_day,start_date)
        month_rent_list.append(month_rent)
        split_rent = split_rent_calculator(month_rent_list,rent_list)
        total_rent = split_rent + month_rent
        print(f"Due Date: {current_date}")
        print(f"Rent: {rent}")
        print(f"Last Day of Month: {last_day}")
        print(f"Month End Rent: {month_rent}")
        print(f"Due Day Rent : {split_rent}")
        print(f"Total Rent: {total_rent}")
              


def main ():
    start_date = input('What is the start date?\n')
    end_date = input('What is the end date?\n')
    rent_pm = input('What is the rent amount\n')
    rent_pm = int(rent_pm)
    rate_increase = input('What is the Rate hike %\n')
    rate_increase = int(rate_increase)
    try:
        start_date = datetime.strptime(start_date,"%d-%m-%Y")
        end_date = datetime.strptime(end_date,"%d-%m-%Y")
    except:
        print("Date Entered in the Incorrect Format")
    
    calculate_rent(start_date,end_date,rent_pm,rate_increase)


main()
