import gspread
from google.oauth2.service_account import Credentials

# Scope and credentials code from Love Sandwiches walkthrough
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
        sales_input = input(f"Please enter this weeks {sheet_name} sales
                            for all 12 items, separated by commas - \n")
        try:
            sales_values = [int(sale) for sale in sales_input.split(',')]
        except ValueError:
            print("Please input numbers only.")
            continue

        if len(sales_values) != len(product_titles):
            print("Please enter a sale value for each item -
                  'no sales' for an item is to be entered as 0.")
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


def calculate_total_sales(sales_dicts):
    """
    Totals sales from each input/sheet
    """
    total_sales = {}
    for sales_dict in sales_dicts:
        for product_title, sales_value in sales_dict.items():
            total_sales[product_title] = total_sales.get(product_title, 0) +
            sales_value
    return total_sales


def update_inventory(worksheet, product_titles, total_sales):
    """
    Updates inventory shett by subtracting
    total sales from stock to create
    running total
    """
    inventory_updated = {}

    for title in product_titles:
        index = product_titles.index(title)

        if index < 0:
            print(f"{index} is not in items.")
            continue

        last_row = len(worksheet.col_values(index + 1))
        while last_row > 0 and worksheet.cell(last_row, index + 1).value == "":
            last_row -= 1

        previous_num_cell = worksheet.cell(last_row, index + 1)
        previous_num = previous_num_cell.value

        if previous_num is None:
            print(f"{title} previous cell is empty")
            continue

        new_num = int(previous_num) - total_sales.get(title, 0)

        worksheet.update_cell(last_row, index + 1, new_num)

        inventory_updated[title] = new_num

    return inventory_updated


def main():
    """
    Calls functions, passes data to them
    to execute program
    """
    shop_sales_worksheet = SHEET.worksheet('shop-sales')
    shop_product_titles = get_product_titles(shop_sales_worksheet)
    shop_sales_values = get_sales_input(shop_product_titles, "SHOP")

    if shop_sales_values is not None:
        weekly_shop_sales = update_sales(shop_sales_worksheet,
                                         shop_product_titles,
                                         shop_sales_values)
        print(f"Weekly SHOP sales: \n {weekly_shop_sales}\n")

    etsy_sales_worksheet = SHEET.worksheet('etsy-sales')
    etsy_product_titles = get_product_titles(etsy_sales_worksheet)
    etsy_sales_values = get_sales_input(etsy_product_titles, "ETSY")

    if etsy_sales_values is not None:
        weekly_etsy_sales = update_sales(etsy_sales_worksheet,
                                         etsy_product_titles,
                                         etsy_sales_values)
        print(f"Weekly ETSY sales: \n {weekly_etsy_sales}\n")

    total_sales_dicts = [weekly_shop_sales, weekly_etsy_sales]
    total_sales = calculate_total_sales(total_sales_dicts)
    print(f"Total Sales This Week:  \n {total_sales}\n")

    inventory_worksheet = SHEET.worksheet('inventory')
    inventory_product_titles = get_product_titles(inventory_worksheet)

    inventory_updated = update_inventory(inventory_worksheet,
                                         inventory_product_titles, total_sales)
    print(f"Inventory Updated: \n {inventory_updated}\n")


main()
