""" ‍*********************************************************************** """
""" ‍                                                                        """
""" ‍                                                        |\              """
""" ‍    query.py                                      ------| \----         """
""" ‍                                                  |    \`  \  |  p      """
""" ‍    By: mihirlad55                                |  \`-\   \ |  o      """
""" ‍                                                  |---\  \   `|  l      """
""" ‍    Created: 2018/10/29 13:11:01 by mihirlad55    | ` .\  \   |  y      """
""" ‍    Updated: 2018/10/29 20:06:27 by mihirlad55    -------------         """
""" ‍                                                                        """
""" ‍*********************************************************************** """
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
