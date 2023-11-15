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


def get_product_titles(worksheet):
    """
    Retrieves product titles from first row
    of worksheet
    """
    return worksheet.row_values(1)


def get_sales_input(product_titles, sheet_name):
    """
    Requests sale figures to be inputted from user,
    validates the data entered
    """
    while True:
        sales_input = input(f"Please enter this weeks {sheet_name} sales for all items, separated by commas - ")
        try:
            sales_values = [int(sale) for sale in sales_input.split(',')]
        except ValueError:
            print("Please input numbers only.")
            continue

        if len(sales_values) != len(product_titles):
            print("Please enter a sale value for each item - 'no sales' for an item is to be entered as 0.")
            continue

        return sales_values


def update_sales(worksheet, product_titles, sales_values):
    """
    Updates the sheet being worked on with
    validated sales figures from user
    """
    worksheet.append_row(sales_values, value_input_option='USER_ENTERED')
    weekly_sales = dict(zip(product_titles, sales_values))

    return weekly_sales


def main():
    """
    Calls functions, passes data to them
    to execute program
    """
    shop_sales_worksheet = SHEET.worksheet('shop-sales')
    shop_product_titles = get_product_titles(shop_sales_worksheet)
    shop_sales_values = get_sales_input(shop_product_titles, "SHOP")

    if shop_sales_values is not None:
        weekly_shop_sales = update_sales(shop_sales_worksheet, shop_product_titles, shop_sales_values)
        print(f"Weekly SHOP sales: {weekly_shop_sales}")

    etsy_sales_worksheet = SHEET.worksheet('etsy-sales')
    etsy_product_titles = get_product_titles(etsy_sales_worksheet)
    etsy_sales_values = get_sales_input(etsy_product_titles, "ETSY")

    if etsy_sales_values is not None:
        weekly_etsy_sales = update_sales(etsy_sales_worksheet, etsy_product_titles, etsy_sales_values)
        print(f"Weekly ETSY sales: {weekly_etsy_sales}")


main()
