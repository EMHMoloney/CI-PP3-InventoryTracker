import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]
CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('ci_pp3_inventorytracker')


def get_product_titles(shop_sales):
    """
    Retrieves product titles from first row
    of worksheet
    """
    return shop_sales.row_values(1)


weekly_shop_sales = {}


def get_sales_input(product_titles):
    """
    Requests sale figures to be inputted from user,
    validates the data entered
    """
    while True:
        sales_input = input("Please enter this weeks SHOP sales for all items, separated by commas - ")
        try:
            sales_values = [int(sale) for sale in sales_input.split(',')]
        except ValueError:
            print("Please input numbers only.")
            continue

        if len(sales_values) != len(product_titles):
            print("Please enter a sale value for each item - 'no sales' for an item is to be entered as 0.")
            continue

        return sales_values


def update_shop_sales(shop_sales, product_titles, sales_values):
    """
    Updates thes sheet being worked on with
    validated sales figures from user
    """
    weekly_shop_sales = {}

    shop_sales.append_row(sales_values, value_input_option='USER_ENTERED')
    weekly_shop_sales = dict(zip(product_titles, sales_values))

    return weekly_shop_sales


def main():
    """
    Calls functions, passes data to them
    to execute program
    """
    shop_sales = SHEET.worksheet('shop-sales')
    product_titles = get_product_titles(shop_sales)

    sales_values = get_sales_input(product_titles)
    if sales_values is not None:
        weekly_shop_sales = update_shop_sales(shop_sales, product_titles, sales_values)
        print(f"Weekly SHOP sales:  \n")
        print(weekly_shop_sales)

main()
