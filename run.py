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
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

sales = SHEET.worksheet('sales')

data = sales.get_all_values()

# print(data) commented out as working

def get_sales_data():
    """
    Get sales figures input from the user
    split turns string to a list by splitting 
    the values at the comma
    the backslash n gives an extra line of space below.
    """
    print("please enter sales data from the last market.")
    print("Data should be six numbers, separated by commas.")
    print("Example: 10, 20, 30, 40, 50, 60\n")

    data_str = input("Enter your data here: ")
   
    sales_data = data_str.split(",")
    validate_data(sales_data)


def validate_data(values):
    """
    Inside the try, converts all string values into intergers. 
    Raise ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    
    e shorthand for error in python!
    
    it's now doing two things, checking if the values provided 
    can be changed to a number, intigers. it's checking to see
    6 values have been provided and gives an error message 
    should 6 values not be found.
    """
    print(values)
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")



get_sales_data()