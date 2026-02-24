# SQLite interface comes preinstalled with python.
import sqlite3 
from employee import Employee

# Connection object for the database file creating a 
# database file called employee.db
# conn = sqlite3.connect("employee.db")

# Creates a database in RAM
conn = sqlite3.connect(":memory:") 

# Cursor used to interface with the database object
c = conn.cursor()

# Execute method runs sql commands on the database file
"""
Five Data Types in sqlite: 
Null: Null value
Integer: Signed integer -- byte size depends on magnitude
Real: 8 byte IEEE floating point
Text: String stored using database encoding
Blob: Raw binary input 
"""
c.execute("""CREATE TABLE employees (
          first text, 
          last text, 
          pay integer)
    """)

def insert_emp(emp): 
    # Context manager: will commit if it can 
    with conn: 
        c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
          {'first': emp.first, 'last': emp.last, 'pay': emp.pay} )


def get_emps_by_name(lastname):
    c.execute("SELECT * FROM employees WHERE last=:last", {'last': lastname})
    return c.fetchall()

def update_pay(emp, pay):
    with conn: 
        c.execute("""UPDATE employees SET pay = :pay
                  WHERE first = :first AND last = :last""", 
                  {'first': emp.first, 'last': emp.last, 'pay': pay})

def remove_emp(emp):
    with conn: 
        c.execute("""DELETE from employees WHERE first = :first AND last = :last""",
                  {'first': emp.first, 'last': emp.last})



emp_1 = Employee('John', "Doe", 9000)
emp_2 = Employee('Jane', 'Doe', 10000)

insert_emp(emp_1)
insert_emp(emp_2)

emps = get_emps_by_name('Doe')
print(emps)

update_pay(emp_2, 100000)
remove_emp(emp_1)

emps = get_emps_by_name("Doe")
print(emps)

conn.close()


# Manual Examples of each statement 

# # Insert method one: pass in a tuple with values to corresponding ?
# c.execute("INSERT INTO employees VALUES (?, ?, ?)", (emp_1.first, emp_1.last, emp_1.pay))

# conn.commit()

# # Insert method two: pass in a dictionary correpsoning to the keys defined 
# c.execute("INSERT INTO employees VALUES (:first, :last, :pay)", 
#           {'first': emp_2.first, 'last': emp_2.last, 'pay': emp_2.pay} )

# Select employee method 1: ? with tuple -- , is needed
# c.execute("SELECT * FROM employees WHERE last=?", ('Burgerton',))

# Above gives us one or mutiple database result
# c.fetchone() gives one return row
# c.fetchmany(5) gives 5 return rows 
# c.fetchall() gives all return rows
# Each is returned as a tuple

# print(c.fetchall())

# Select employee method 2: 
# c.execute("SELECT * FROM employees WHERE last=:last", {'last': 'Doe'})
# print(c.fetchall())

# # Commit changes made to the data base file
# conn.commit()

# # Close connection to the database file
# conn.close()
