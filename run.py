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
    Get scoops sold data sold each day from user
    """
    print("Please enter how many scoops sold today.")
    print("Data should be seven numbers, separated by commas.")
    print("Example: 10,20,30,40,50,60,70\n")

    data_str = input("Enter your data here: ")  
    scoops_data = data_str.split(",")
    validate_data(scoops_data)

def validate_data(values):  
    """
    inside The try, converts all string values into integers
    raises ValueError if strings cannot be converted into integers,
    or if there arnt exactly 7 values.
    """ 

    try:
        if len(values) != 7:
            raise ValueError(
                f"Ooops, please enter data for all 7 items, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")

get_scoops_data()