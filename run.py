import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

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
    Get scoops sold data sold each day from user
    """
    while True:
        print("Please enter how many scoops sold today.")
        print("Data should be seven numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60,70\n")

        data_str = input("Enter your data here: ")  

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
                f"Ooops, please enter data for all 7 items, you provided {len(values)}"
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


def main():
    """
    run all program functions
    
    """

    data = get_scoops_data()
    scoops_data = [int(num) for num in data]
    update_scoops_worksheet(scoops_data)
    new_surplus_scoops = calculate_surplus_scoops(scoops_data)
    update_surplus_worksheet(new_surplus_scoops)


print("Welcome to Ice Cream Parlor Data Automation")
main()    