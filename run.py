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
    function logic: get_sales_data runs a while loop 
    until the correct amount of values are fed in.
    it changes data input to a list of data and
    checks for errors.
    checks for anything but integers and will throw 
    an error and repeat the while loop until all
    aspects run valid. 
    """

    while True:
        print("please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10, 20, 30, 40, 50, 60\n")

        data_str = input("Enter your data here: ")
    
        sales_data = data_str.split(",")
        

        if validate_data(sales_data):
            print("DATA IS VALID!")
            break
    return sales_data


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
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False

    return True

# def update_sales_worksheet(data):
   # """
   # update sales worksheet, add new row with the list data provided.
   # the sales word links to the page of the spreadsheet you wish to access
   # """
   # print("UPDATING SALES WORKSHEET . . . \n")
   # sales_worksheet = SHEET.worksheet("sales")
   # sales_worksheet.append_row(data)
   # print("SALES WORKSHEET UPDATED SUCCESSFULLY.\n")

# def update_surplus_worksheet(data):
    # """
    # update surplus worksheet, add new row with the list data provided.
    # the surplus word links to the page of the spreadsheet you wish to access
    # """
    # print("UPDATING SURPLUS WORKSHEET . . . \n")
    # surplus_worksheet = SHEET.worksheet("surplus")
    # surplus_worksheet.append_row(data)
    # print("SURPLUS WORKSHEET UPDATED SUCCESSFULLY.\n")

def update_worksheet(data, worksheet):
    """
    refactoring two functions into one function
    """
    print(f"UPDATING {worksheet} WORKSHEET . . . \n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")

def calculate_surplus_data(sales_row):
    """
    compare sales with stock and calculate the surplus for each item type.

    the surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative indicates extras made when stock sold out. 

    easiest way to retrieve the latest data is using the slice method with
    an index of minus 1
    """
    print("Calculating surplus data . . . \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data

def get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting the 
    last 5 entries for each sandwich and returns the data as a 
    list of lists
    note: numbers we give gspread methods for rows and columns 
    start at one NOT zero like indexes do!
    """

    sales = SHEET.worksheet("sales")
 
columns = []
for ind in range(1, 7):
    column = sales.col_values(ind)
    columns.append(column[-5:])

return columns


def main():
    """
    Runs all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")

print("WELCOME TO LOVE SANDWICHES DATA AUTOMATION")
# main()
sales_columns = get_last_5_entries_sales()