import gspread
from hashlib import new
from colorama import Fore, Back, Style

from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('project-3')


def get_scoops_data():
    """
    Get scoops sold data each day from user:
    """
    while True:
        print(Fore.GREEN+"Please enter how many scoops sold today.")
        print(Fore.GREEN+"Data should be seven numbers, separated by commas.")
        print(Fore.GREEN+"Example: 10,20,30,40,50,60,70\n")

        data_str = input(Fore.GREEN+"Enter How many scoops sold today here:\n")

        scoops_data = data_str.split(",")

        if validate_data(scoops_data):
            print(Fore.GREEN+"Data is valid!")
            break

    return scoops_data


def validate_data(values):
    """
    inside The try, converts all string values into integers
    raises ValueError if strings cannot be converted into integers,
    or if there arnt exactly 7 values.
    """

    try:
        [int(value) for value in values]
        if len(values) != 7:
            raise ValueError(
                "Ooops, please enter data for all 7 items,"
            )
    except ValueError as e:
        print(Fore.GREEN+f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_scoops_worksheet(data):
    """
    Update scoops worksheet, add new row with the list data provided.
    """
    print(Fore.GREEN+"Updating Scoop count....\n")
    scoops_worksheet = SHEET.worksheet("scoops")
    scoops_worksheet.append_row(data)
    print(Fore.GREEN+"Scoops worksheet updated successfully...\n")


def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print(Fore.GREEN+"Updating Scoop count....\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print(Fore.GREEN+"Surplus worksheet updated successfully...\n")


def update_worksheet(data, worksheet):
    """
    Updates the worksheet with the data provided,
    after recieving  a list of integers
    that have been entered into a worksheet\
    """
    print(Fore.GREEN+f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(Fore.GREEN+f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_scoops(scoops_row):
    """
    Deduct the sold scoops from the amount of scoops available in a 10kg tub
    The surplus is defined as the scoops figure is deducted from the stock
    """

    print(Fore.GREEN+"Calculating how many scoops left in stock...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_scoops = []
    for stock, scoops in zip(stock_row, scoops_row):
        surplus = int(stock) - scoops
        surplus_scoops.append(surplus)

    return surplus_scoops


def get_current_stock():
    """
    Collects data from scoops worksheet, for the last 5 days
    and returns the data as a list of lists
    """
    scoops = SHEET.worksheet("stock")


    columns = []
    for ind in range(1, 8):
        column = scoops.col_values(ind)
        columns.append(column[-1:])

    return columns


def calculate_stock_data(data,scoops_data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print(Fore.GREEN+"Calculating stock data...\n")
    print(Fore.GREEN+"Thank you for your input, have a great day")
    new_stock_data = []
    for j in range(len(data)+0):
        new_stock_data.append(int(data[j][0])-int(scoops_data[j]))
    return new_stock_data

def weekly_scoops():
    w_scoops = SHEET.worksheet("scoops")
    column = []
    print(Fore.GREEN+"~~~~~~~~~~~Weekly Scoop~~~~~~~~~\n")
    for ind in range(1, 8):
        col = w_scoops.col_values(ind)
        column.append(col)
    for i in range(len(column)+0):
        total=0
        # print(type(column[i]))
        for k in range(len(column[i])+0):
            if k==0 :
                continue
            elif k>len(column[i])-8:
                # print(f"{column[i][2]} ={total} i={i}k={k}\n")
             
                total=total+int(column[i][k])
                # print(f"total ={total} \n")
            
        print(f"{total} {column[i][0]}\n")
    print(Fore.GREEN+"########### Weekly Scoop ###########\n")

def data_in_stock():
     w_scoops = SHEET.worksheet("stock")
     column = []
     print(Fore.GREEN+"~~~~~~~~~~~ Stock ~~~~~~~~~\n")
     for ind in range(1, 8):
        col = w_scoops.col_values(ind)
        column.append(col)
        # product=w_scoops.a
     for i in range(len(column)+0):
        total=0
        # print(type(column[i]))
        for k in range(len(column[i])+0):
            if k==0 :
                total=total+int(column[i][len(column[i])-1])
                continue            
        print(f"{total} {column[i][0]}\n")
        if total<36:
            print(Fore.GREEN+f' Your stock is running low please oder more {column[i][0]}\n')
     print(Fore.GREEN+"########### Stock ###########\n")
def main():
    """
    run all program functions
    """
    print(Fore.GREEN+"     _                                                ")
    print(Fore.GREEN+"    ' `                                               ")
    print(Fore.GREEN+"   '   '.   _                                         ")   
    print(Fore.GREEN+"   >_.(__) (_)                                        ")
    print(Fore.GREEN+" (_,-'   |  _  ___ ___  ___ _ __ ___  __ _ _ __ ___   ")
    print(Fore.GREEN+"   `.    | | |/ __/ _ \/ __| '__/ _ \/ _` | '_ ` _ \  ")
    print(Fore.GREEN+"      .  | | | (_|  __/ (__| | |  __/ (_| | | | | | | ")
    print(Fore.GREEN+"        .| |_|\___\___|\___|_|  \___|\__,_|_| |_| |_| ")
    print(Fore.GREEN+"         `                                            ")

    welcome_input = input(Fore.GREEN+"Enter Ice Cream Parlour y/n?:\n")
    if welcome_input == "y":
        print(Fore.GREEN+"Welcome to the menu")
        print(Fore.GREEN+"Please enter 1 to enter Ice Cream data")
        print(Fore.GREEN+"Please enter 2 to see Ice Cream data")
        menu=int(input(Fore.GREEN+"Enter 1 or 2 \n"))
        if menu==1:
            data = get_scoops_data()
            scoops_data = [int(num) for num in data]
            update_worksheet(scoops_data, "scoops")
            new_surplus_scoops = calculate_surplus_scoops(scoops_data)
            update_worksheet(new_surplus_scoops, "surplus")
            scoops_columns = get_current_stock()
            stock_data = calculate_stock_data(scoops_columns,scoops_data)
            update_worksheet(stock_data, "stock")
        elif menu==2:
            print(Fore.GREEN+"Please enter 1 to see weekly scoops total")
            print(Fore.GREEN+"Please enter 2 to remaining Stock")
            view=int(input(Fore.GREEN+"Enter 1 or 2 \n"))
            if view == 1:
                weekly_scoops()
            elif view == 2:
                data_in_stock()
            else:
                print(Fore.GREEN+"Incorrect input") 
        else:
           print(Fore.GREEN+"Incorrect input") 
    elif welcome_input == "n":
        print(Fore.GREEN+"no IceCream data for you today")
    else :
        print(Fore.GREEN+"Incorrect input") 

print(Fore.GREEN+"Welcome to Ice Cream Parlor Data Automation")
main()
