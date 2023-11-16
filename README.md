# Inventory Tracker
 
 ## A programme in Python to automate sales and inventory tracking for a small business

 A python application to automate the tracking of sales and inventory of individual
 stock lines for a small retailer.
 The user is requested to enter sales figures for each line from
 different sources - a standalone shop of some kind, and an Etsy storefront.
 The app then updates the sheets for those outlets, then it
 creates a report of total sales from the different sources for each item.
 The inventory sheet is updated to create running stockholding total figures
 for each item , based on the previous figures with the news sales subtracted.
 These new inventory numbers are the final report sent to the user.

 ## Setup

 ### Credentials and Dependencies

 The credentials req to access the Google Sheets API for the app are
 located in a .json file called 'credentials'.
  Dependencies are in the 'requirements.txt' file, to be installed using 
  'pip install' method.

  ### Google Sheets

  The app requires a Google Sheets workbook - name 'ci-pp3-inventorytracker'
  with sheets 'shop-sales', 'etsy-sales' and 'inventory'.

  NB- The 'inventory' sheet must be prepopulated with the inventory figures
  of the individual items, the app can only update existing inventory figures ,
  otherwise a "replenishment required" message will be reported to the user. 

## Development and Testing

The application code follows PEP8 guidelines and was
 passed through the pep8 linter. 
 Testing involved checking for user entry errors - icluding non-numeric entries, 
 insufficient/excess entries, and  for non population of the inventory sheet.

### Credits

The source code for the scope is from [Love Sandwiches project](https://codeinstitute.net).
The app uses the ValueInOption 'USER_ENTERED' from
 [Developers Google](https://developers.google.com/sheets/api/rest/v4/spreadsheets.values)
 after encountering value access errors when accessing the sheets to append.

 ### Future Updates

 In commercial use the figures from an ecomm platform or retail EPOS
 system could be automatically transferred. Further reports could
  be generated i.e. a percentage breakdown of sales by source, or by styles/SKUs etc.



