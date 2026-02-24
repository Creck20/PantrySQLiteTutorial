# SQLite comes preinstalled in python
import sqlite3
from datetime import date, timedelta

"""
Desired system requirements (various sources): 
1. Create a SQL database with at least one table 
(your software can create the table or you can use already existing table).

2. Software should query data from the database.

3. Software should add new data to the database.

4. Software should update data from the database.

5. Software should delete data from the database.

Strectch Ideas: 
Add additional tables to your database and perform a
join in your software between two of the tables.

Use at least two of the aggregate functions to summarize 
numerical data in your database.

Demonstrate the use of a column containing a date or time 
along with a query that demonstrates filtering within a date or time range.

Functionality: 
A system that lets you add items to your pantry and search for items by name. 

CREATE TABLE pantry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    category TEXT,
    expiration_date DATE,
    date_added DATE DEFAULT CURRENT_DATE
);

Five Data Types in sqlite: 
Null: Null value
Integer: Signed integer -- byte size depends on magnitude
Real: 8 byte IEEE floating point
Text: String stored using database encoding
Blob: Raw binary input 
"""

# Using a virtual memory database 
# (created at runtime for demonstration purposes)
conn = sqlite3.connect(":memory:")

# Cursor used to interface with database object:
c = conn.cursor()

# Run at start of program to create tables
c.execute("""CREATE TABLE pantry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    category TEXT,
    expiration_date DATE,
    date_added DATE DEFAULT CURRENT_DATE
)""")

def add_item(prod_name, quantity=1, category="general", expiration_date=None):
    """
    Purpose:
        Insert item into database. If item already exists, update by quantity.
    Parameters: 
        prod_name: Product name string 
        opt quantity: Quantity of products, default 1
        opt category: Category of product(s), default general
        opt expiration_date: Date product expires, default todays date + 7 days
    Return: 
        Void
    """
    if expiration_date is None:
        expiration_date = (date.today() + timedelta(days=7)).isoformat()
    
    c.execute("SELECT quantity FROM pantry WHERE product_name = ?", (prod_name,))
    row = c.fetchone()
    
    # If item already exists, update quantity. Otherwise, insert new item.
    if row:
        with conn:
            c.execute("""
                UPDATE pantry 
                SET quantity = quantity + ? 
                WHERE product_name = ?
            """, (quantity, prod_name))
    else:
        with conn:
            c.execute("""
                INSERT INTO pantry 
                (product_name, quantity, category, expiration_date, date_added)
                VALUES (?, ?, ?, ?, ?)
            """, (prod_name, quantity, category, expiration_date, date.today().isoformat()))

def search_item(search_term):
    """
    Purpose:
        Search for item by name or partial name, return all matching items:
    Parameters: 
        search_term: String to search for in product names
    Return: 
        List of tuples containing matching items
    """
    # Use wildcard %% search to find items that contain the search term
    c.execute("SELECT * FROM pantry WHERE product_name LIKE ?", (f"%{search_term}%",))
    return c.fetchall()


def delete_item(product_name):
    """
    Purpose:
        Delete an item from the pantry table.
    Parameters: 
        product_name: Name of the product to delete
    Return: 
        Void
    """
    with conn:
        c.execute("DELETE FROM pantry WHERE product_name = ?", (product_name,))

def query_all(): 
    """
    Purpose:
        Query all items in the pantry table.
    Parameters: 
        None
    Return: 
        List of tuples containing all pantry items
    """
    c.execute("SELECT * FROM pantry")
    return c.fetchall()

def summary_report():
    """
    Purpose:
        Generate a summary report of the pantry, including total items, categories, 
        and quantities in each category.
    Parameters:
        None
    Return:
        None (prints summary report to console)
    """
    # Count function returns a single value, so we fetch the first element of the result tuple
    c.execute("SELECT COUNT(*) FROM pantry")
    total_items = c.fetchone()[0]

    # Group by category and sum quantities to get total quantity per category
    c.execute("SELECT category, SUM(quantity) FROM pantry GROUP BY category")
    category_summary = c.fetchall()

    print(f"Total Items: {total_items}")
    for category, total_quantity in category_summary:
        print(f"Category: {category}, Total Quantity: {total_quantity}")

def expiring_items(): 
    """
    Purpose:
        Query items that are expiring within the next 7 days.
    Parameters:
        None
    Return:
        List of tuples containing expiring items
    """
    today = date.today().isoformat()
    next_week = (date.today() + timedelta(days=7)).isoformat()
    
    c.execute("""
        SELECT * FROM pantry 
        WHERE expiration_date BETWEEN ? AND ?
    """, (today, next_week))
    
    return c.fetchall()

def main():
    while (True):
        print("\nPantry Management System")
        print("1. Add Item")
        print("2. Search Item")
        print("3. Delete Item")
        print("4. View All Items")
        print("5. Summary Report")
        print("6. Expiring Items")
        print("7. Load Preset")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            prod_name = input("Product Name: ")
            quantity = int(input("Quantity: "))
            category = input("Category: ")
            expiration_date = input("Expiration Date (YYYY-MM-DD, optional): ")
            add_item(prod_name, quantity, category, expiration_date if expiration_date else None)
            print(f"Added {quantity} of {prod_name} to pantry.")
        
        elif choice == '2':
            search_term = input("Enter product name or partial name to search: ")
            results = search_item(search_term)
            if results:
                for item in results:
                    print(item)
            else:
                print("No items found.")
        
        elif choice == '3':
            product_name = input("Enter the name of the product to delete: ")
            delete_item(product_name)
            print(f"Deleted {product_name} from pantry.")
        
        elif choice == '4':
            items = query_all()
            for item in items:
                print(item)
        
        elif choice == '5':
            summary_report()
        
        elif choice == '6':
            expiring = expiring_items()
            if expiring:
                for item in expiring:
                    print(item)
            else:
                print("No items expiring within the next 7 days.")
        
        elif choice == '7': 
            add_item('milk', category='dairy')
            add_item('beef', category='meat')
            add_item('lettuce', category='vegetable')
        
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    conn.close()
