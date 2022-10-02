import gspread
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
        print("Please enter how many scoops sold today.")
        print("Data should be seven numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60,70\n")

        data_str = input("Enter How many scoops sold today here:\n")

        scoops_data = data_str.split(",")

        if validate_data(scoops_data):
            print("Data is valid!")
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
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True


def update_scoops_worksheet(data):
    """
    Update scoops worksheet, add new row with the list data provided.
    """
    print("Updating Scoop count....\n")
    scoops_worksheet = SHEET.worksheet("scoops")
    scoops_worksheet.append_row(data)
    print("“Scoops worksheet updated successfully...\n")


def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list data provided.
    """
    print("Updating Scoop count....\n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("“Surplus worksheet updated successfully...\n")


def update_worksheet(data, worksheet):
    """
    Updates the worksheet with the data provided,
    after recieving  a list of integers
    that have been entered into a worksheet\
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def calculate_surplus_scoops(scoops_row):
    """
    Deduct the sold scoops from the amount of scoops available in a 10kg tub
    The surplus is defined as the scoops figure is deducted from the stock
    """

    print("Calculating how many scoops left in stock...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]

    surplus_scoops = []
    for stock, scoops in zip(stock_row, scoops_row):
        surplus = int(stock) - scoops
        surplus_scoops.append(surplus)

    return surplus_scoops


def get_popular_flavours():
    """
    Collects data from scoops worksheet, for the last 5 days
    and returns the data as a list of lists
    """
    scoops = SHEET.worksheet("scoops")


    columns = []
    for ind in range(1, 8):
        column = scoops.col_values(ind)
        columns.append(column[-5:])

    return columns


def calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    print("Thank you for your input, have a great day")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


def main():
    """
    run all program functions
    """
    print("     _                                                                             ")
    print("    ' `                                                                           ")
    print("   '   '.   _                                                                       ")   
    print("   >_.(__) (_)                                                                      ")
    print(" (_,-'   |  _  ___ ___  ___ _ __ ___  __ _ _ __ ___                               ")
    print("   `.    | | |/ __/ _ \/ __| '__/ _ \/ _` | '_ ` _ \                              ")
    print("      .  | | | (_|  __/ (__| | |  __/ (_| | | | | | |                                   ")
    print("        .| |_|\___\___|\___|_|  \___|\__,_|_| |_| |_|             ")
    print("         `  ")

    welcome_input = input("Enter y/n?:\n")
    if(welcome_input == "y"):
        print("Welcome to the menu")
        print("Please enter 1 to enter data")
        print("Please enter 2 to see data")
        menu=int(input("Enter 1 or 2:\n"))

        if(menu==1):
            data = get_scoops_data()
            scoops_data = [int(num) for num in data]
            update_worksheet(scoops_data, "scoops")
            new_surplus_scoops = calculate_surplus_scoops(scoops_data)
            update_worksheet(new_surplus_scoops, "surplus")
            scoops_columns = get_popular_flavours()
            stock_data = calculate_stock_data(scoops_columns)
            update_worksheet(stock_data, "stock")
        if(menu==2):
            print("view data functionality is going to be implemented")
    if(welcome_input=="n"):
        print("no IceCream data for you today")

print("Welcome to Ice Cream Parlor Data Automation")
main()



                                                                  
    

     _                                        
(_)                                       
 _  ___ ___  ___ _ __ ___  __ _ _ __ ___  
| |/ __/ _ \/ __| '__/ _ \/ _` | '_ ` _ \ 
| | (_|  __/ (__| | |  __/ (_| | | | | | |
|_|\___\___|\___|_|  \___|\__,_|_| |_| |_|
                                          