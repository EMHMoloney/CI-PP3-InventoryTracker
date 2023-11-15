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
    return shop_sales.row_values(1)

weekly_shop_sales = {}

def get_sales_input(product_titles):
    sales_input = input("Please enter this weeks SHOP sales for all items, seperated by commas - ")
    sales_values = [int(sale) for sale in sales_input.split(',')]

    if len(sales_values) != len(product_titles):
        print("Please enter a sale value for each item - no sales must be entered as 0.")
        return None

    try:
        sales_values = [int(sale) for sale in sales_values]
    except ValueError:
        print("Sales must be entered as whole numbers, please try again ")
        return None

    return sales_values

def update_shop_sales(shop_sales, product_titles, sales_values):
    weekly_shop_sales = {} 

    shop_sales.append_row(sales_values, value_input_option = 'USER_ENTERED')
    weekly_shop_sales = dict(zip(product_titles, sales_values))

    return weekly_shop_sales


def main ():
    shop_sales = SHEET.worksheet('shop-sales')
    product_titles = get_product_titles(shop_sales)

    sales_values = get_sales_input(product_titles)
    if sales_values is not None:
        weekly_shop_sales = update_shop_sales(shop_sales, product_titles, sales_values)
#etsy_data = etsy_sales.get_all_values()
#print(etsy_data)

#shop_data = shop_sales.get_all_values()
#print(shop_data)

#print(f"Weekly SHOP sales:  \n")
#print(weekly_shop_sales)
main()