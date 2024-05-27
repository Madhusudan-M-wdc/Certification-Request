import sqlite3

# Define the dictionary
sku_options = {
    "Vulcan_GOEM": ["SDDPTQD-256G", "SDDPTQD-512G", "SDDPTQD-1T00", "SDDPTQE-512G", "SDDPTQE-1T00", "SDDPTQE-2T00", "SDDPMQD-256G", "SDDPMQD-512G", "SDDPMQD-1T00", "SDDPMQE-512G", "SDDPMQE-1T00", "SDDPMQE-2T00", "SDDPNQD-256G", "SDDPNQD-512G", "SDDPNQD-1T00", "SDDPNQE-512G", "SDDPNQE-1T00", "SDDPNQE-2T00", "SDDQTQD-256G", "SDDQTQD-512G", "SDDQTQD-1T00", "SDDQTQE-2T00", "SDDQNQD-256G", "SDDQNQD-512G", "SDDQNQD-1T00", "SDDQNQE-2T00", "SDDPTQE-2T00-1050", "SDDPMQE-2T00-1050"],
    "Vulcan_HP": ["SDDPNQD-256G-2006", "SDDPNQD-512G-2006", "SDDPNQD-1T00-2006", "SDDPTQD-256G-2006", "SDDPTQD-512G-2006", "SDDPNQE-512G-2006", "SDDQNQD-512G-2006", "SDDPNQE-1T00-2006", "SDDQNQD-256G-2006", "SDDQNQD-256G-2506", "SDDQNQD-512G-2506", "SDDPNQD-256G-2406", "SDDPNQD-512G-2406", "SDDQNQD-256G-1006", "SDDQNQD-512G-1006", "SDDQNQD-256G-1506", "SDDQNQD-512G-1506", "SDDPNQD-256G-1406", "SDDPNQD-512G-1406", "SDDPNQD-256G-1006", "SDDPNQD-512G-1006", "SDDPNQD-1T00-1006", "SDDPTQD-256G-1006", "SDDPTQD-512G-1006", "SDDPNQE-512G-1006", "SDDPNQE-1T00-1006"],
    "Vulcan_Dell": ["SDDQTQE-2T00-1012", "SDDPNQD-256G-1002", "SDDPNQD-512G-1002", "SDDPNQD-1T00-1002", "SDDPNQE-2T00-1002", "SDDPTQD-256G-1012", "SDDPTQD-512G-1012", "SDDPTQD-1T00-1012", "SDDQTQD-256G-1012", "SDDQTQD-512G-1012", "SDDQTQD-1T00-1012", "SDDPTQE-2T00-1012", "SDDPTQE-512G-1012", "SDDPTQE-1T00-1012"],
    "Vulcan_Asus": ["SDDPTQE-2T00-1102", "SDDQNQD-256G-1002", "SDDQNQD-512G-1002", "SDDQNQD-1T00-1002", "SDDQNQE-2T00-1002", "SDDPNQE-1T00-1102", "SDDPNQE-512G-1002", "SDDPNQE-1T00-1002", "SDDPNQD-256G-1102", "SDDPNQD-512G-1102", "SDDPNQD-1T00-1102", "SDDPNQE-2T00-1102", "SDDPTQD-256G-1002", "SDDPTQD-512G-1002", "SDDPTQD-1T00-1002", "SDDPTQD-256G-1102", "SDDPTQD-512G-1102", "SDDPTQD-1T00-1102"],
    "Vulcan_Lenovo_LBG": ["SDDPMQD-256G-1301", "SDDPMQD-512G-1301", "SDDPMQD-1T00-1301", "SDDPMQE-2T00-1301", "SDDPMQD-256G-1201", "SDDPMQD-512G-1201", "SDDPMQD-1T00-1201", "SDDPMQE-2T00-1201", "SDDPTQD-256G-1002", "SDDPTQD-512G-1002", "SDDPTQD-1T00-1002", "SDDPTQD-256G-1102", "SDDPTQD-512G-1102", "SDDPTQD-1T00-1102"],
    "Vulcan_Lenovo_TBG": ["SDDQNQD-256G-1201", "SDDQNQD-512G-1201", "SDDQNQD-1T00-1201", "SDDQMQD-256G-1201", "SDDQMQD-512G-1201", "SDDQMQD-1T00-1201", "SDDQMQE-2T00-1201", "SDDQMQD-256G-1001", "SDDQMQD-512G-1001", "SDDQMQD-1T00-1001", "SDDQNQD-256G-1001", "SDDQNQD-512G-1001", "SDDQNQD-1T00-1001", "SDDPNQE-512G-1001", "SDDPNQE-1T00-1001", "SDDQNQE-512G-1001", "SDDQNQE-1T00-1001", "SDDQMQE-2T00-1001"],
    "Vulcan_Acer": ["SDDPNQE-512G-1014", "SDDPNQE-1T00-1014", "SDDQNQD-256G-1014", "SDDQNQD-512G-1014", "SDDQNQD-1T00-1014", "SDDQNQD-256G-1114", "SDDQNQD-512G-1114", "SDDQNQD-1T00-1114", "SDDQNQE-2T00-1014"],
    "Vulcan_Fujitsu": ["SDDQTQD-256G-1016", "SDDQTQD-512G-1016", "SDDQTQD-1T00-1016", "SDDQNQD-256G-1016", "SDDQNQD-512G-1016", "SDDQNQD-1T00-1016", "SDDPTQD-256G-1016", "SDDPTQD-512G-1016", "SDDPTQD-1T00-1016", "SDDPNQD-256G-1016", "SDDPNQD-512G-1016", "SDDPNQD-1T00-1016", "SDDPTQE-2T00-1016", "SDDPNQE-2T00-1016", "SDDQTQE-2T00-1016", "SDDQNQE-2T00-1016"],
    "Vulcan_Huawei": ["SDDPNQE-512G-1027", "SDDPNQE-1T00-1027", "SDDPNQE-2T00-1027", "SDDPNQE-2T00-1127", "SDDPNQD-256G-1027", "SDDPNQD-512G-1027", "SDDPNQD-1T00-1027", "SDDPNQD-256G-1127", "SDDPNQD-512G-1127", "SDDPNQD-1T00-1127"],
    "Vulcan_Honor": ["SDDPNQD-256G-1136", "SDDPNQD-512G-1136", "SDDPNQD-1T00-1136", "SDDPNQE-1T00-1136", "SDDPNQE-1T00-1036", "SDDPNQD-256G-1036", "SDDPNQD-512G-1036", "SDDPNQD-1T00-1036"],
    "Vulcan_MSI": ["SDDPNQE-512G-1032", "SDDPNQE-1T00-1032", "SDDPNQD-256G-1032", "SDDPNQD-512G-1032", "SDDPNQD-1T00-1032", "SDDPNQE-2T00-1032"],
    "Vulcan_MSFT": ["SDDPTQD-256G-1024", "SDDPTQD-512G-1024", "SDDPTQD-1T00-1024", "SDDPTQE-2T00-1024"],
    "Vulcan_LG": ["SDDPNQD-256G-1009", "SDDPNQD-512G-1009", "SDDPNQD-1T00-1009"],
    "Vulcan_Samsung": ["SDDPNQD-256G-1004", "SDDPNQD-512G-1004", "SDDPNQD-1T00-1004"],
    "Vulcan_Toshiba": ["SDDPNQD-256G-1010", "SDDPNQD-512G-1010", "SDDPNQD-1T00-1010"],
    "Vivaldi_Acer":["SDEQNSJ-512G-1014", "SDEQNSJ-1T00-1014", "SDEQNSJ-2T00-1014"],
    "Vivaldi_Asus":["SDEQTSJ-512G-1002", "SDEQTSJ-1T00-1002", "SDEQTSJ-2T00-1002", "SDEQNSJ-512G-1002", "SDEQNSJ-1T00-1002", "SDEQNSJ-2T00-1002"],
    "Vivaldi_Dell":["SDEPTSJ-512G-1012", "SDEPTSJ-1T00-1012", "SDEPTSJ-2T00-1012"],
    "Vivaldi_GOEM":["SDEPTSJ-512G", "SDEPTSJ-1T00", "SDEPTSJ-2T00", "SDEQTSJ-512G", "SDEQTSJ-1T00", "SDEQTSJ-2T00", "SDEPNSJ-512G", "SDEPNSJ-1T00", "SDEPNSJ-2T00", "SDEQNSJ-512G", "SDEQNSJ-1T00", "SDEQNSJ-2T00"],
    "Vivaldi_Honor":["SDEPNSJ-512G-1036", "SDEPNSJ-1T00-1036", "SDEPNSJ-2T00-1036", "SDEQNSJ-512G-1036", "SDEQNSJ-1T00-1036", "SDEQNSJ-2T00-1036"],
    "Vivaldi_HP": ["SDEPTSJ-512G-1006", "SDEPTSJ-1T00-1006", "SDEPTSJ-2T00-1006", "SDEQTSJ-512G-1006", "SDEQTSJ-1T00-1006", "SDEQTSJ-2T00-1006", "SDEPNSJ-512G-1006", "SDEPNSJ-1T00-1006", "SDEPNSJ-2T00-1006", "SDEQNSJ-512G-1006", "SDEQNSJ-1T00-1006", "SDEQNSJ-2T00-1006", "SDEQNSJ-1T00-1016", "SDEQNSJ-512G-1016"],
    "Vivaldi_Huawei":["SDEQNSJ-512G-1027", "SDEQNSJ-1T00-1027", "SDEQNSJ-2T00-1027"],
    "Vivaldi_Lenovo_LBG": ["SDEPMSJ-512G-1101", "SDEPMSJ-1T00-1101", "SDEPMSJ-2T00-1101"],
    "Vivaldi_Lenovo_TBG": ["SDEPNSJ-512G-1001", "SDEPNSJ-1T00-1001", "SDEPNSJ-2T00-1001"],
    "Vivaldi_MSI": ["SDEPNSJ-512G-1032", "SDEPNSJ-1T00-1032", "SDEPNSJ-2T00-1032"],  
      

}
# Connect to the database (create it if not exists)
conn = sqlite3.connect('sku.db')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store product, OEM, and SKU
cursor.execute('''CREATE TABLE IF NOT EXISTS Products
                (Product TEXT, OEM TEXT, SKU TEXT)''')

# Iterate through the dictionary and insert data into the table
for product_oem, skus in sku_options.items():
    product, oem = product_oem.split('_')[0],product_oem.split('_')[1]
    for sku in skus:
        cursor.execute("INSERT INTO Products (Product, OEM, SKU) VALUES (?, ?, ?)", (product, oem, sku))

# Commit changes and close the connection
conn.commit()
conn.close()

print("Data inserted successfully into the database.")
"""import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('sku.db')
c = conn.cursor()

# Execute a SELECT query to fetch all rows from the ProductSKU table
c.execute("SELECT * FROM Products")

# Fetch all rows
rows = c.fetchall()

# Print the rows
for row in rows:
    print(row)

# Close connection
conn.close()
"""