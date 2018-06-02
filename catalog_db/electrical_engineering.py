import sqlite3

# We will test with Computer Science DB first
# It's okay to have more than one instance courses per major for now 
# but optimizing memory usage is a first after alpha passes testing

# Create a database in RAM
cs_db = sqlite3.connect(':memory:')
# Creates or opens a file called mydb with a SQLite3 DB
cs_db = sqlite3.connect('data/mydb')

# Get a cursor object for your database
cursor = major_db.cursor()
cursor.execute('''
    CREATE TABLE COURSEWORK_CORE(
        COURSE_ID TEXT PRIMARY KEY, COURSE_NAME TEXT
    )
    CREATE TABLE CONCENTRATION_ELECTRODYNAMICS(
        COURSE_ID TEXT PRIMARY KEY, COURSE_NAME TEXT
    )
    CREATE TABLE CONCENTRATION_EMBEDDED_SYSTEM_DESIGN(
        COURSE_ID TEXT PRIMARY KEY, COURSE_NAME TEXT
    )
    CREATE TABLE CONCENTRATION_DIGITAL_HYBRID_SYSTEMS(
        COURSE_ID TEXT PRIMARY KEY, COURSE_NAME TEXT
    )
''')
db.commit()

# Where does this happen?
# If separate databases with overlapping data per major, only open
# appropriate db when these are implemented
# e.g. COP4250 may exist in both cs and ce, but both databases need
# not be open at the same time
# db.close()