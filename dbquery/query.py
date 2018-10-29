# Import library
import sqlite3

# Connect to database file and retreive cursor object
conn = sqlite3.connect('course_database.db')
cur = conn.cursor()
query = ""

while query != "exit":
    # Get query text from user
    query = input("Enter SQL Command (type exit to exit): ")
    
    try:
        # Query Database
        cur.execute(query)
    except sqlite3.OperationalError as err:
        print(type(err), err)

    # Print results of query
    print(cur.fetchall())
