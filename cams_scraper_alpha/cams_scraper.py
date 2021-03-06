""" ‍***************************************************************************** """
""" ‍                                                                              """
""" ‍                                                        |\                    """
""" ‍    cams_scraper.py                               ------| \----               """
""" ‍                                                  |    \`  \  |  p            """
""" ‍    By: mattgiallourakis                          |  \`-\   \ |  o            """
""" ‍                                                  |---\  \   `|  l            """
""" ‍    Created: 2018/09/25 19:53:53 by mattgiallourakis    | ` .\  \   |  y      """
""" ‍    Updated: 2018/10/29 22:58:54 by mihirlad55    -------------               """
""" ‍                                                                              """
""" ‍***************************************************************************** """


from selenium.webdriver.support.ui  import WebDriverWait
from selenium.webdriver.support.ui  import Select
from selenium.webdriver.support     import expected_conditions
from selenium.common.exceptions     import TimeoutException
from selenium.webdriver.common.by   import By
from selenium                       import webdriver

from pprint                         import pprint, pformat

from time                           import sleep


import sqlite3
import json
import re
import sys, getopt

# DEFINE GLOBALS
WEBPAGE_GET_WAIT_TIME               = 10
LOGIN_WAIT_TIME                     = 60

CAMS_TRANSCRIPT_TABLE_XPATH         = "//*[@id='mainBody']/div[2]"
CAMS_LOGIN_BOX_XPATH                = "//*[@id='LeftSide']"
CAMS_COURSES_TABLE_XPATH            = "//*[@id='mainBody']/div[2]/table"
CAMS_COURSES_NUM_OF_PAGES_XPATH     = "//*[@id='mainBody']/div[2]/div[1]"

CAMS_URL                            = "https://cams.floridapoly.org/student/login.asp"
CAMS_TRANSCRIPT_URL                 = "https://cams.floridapoly.org/student/cePortalTranscript.asp"
CAMS_COURSES_URL                    = "https://cams.floridapoly.org/student/cePortalOffering.asp"
CHROME_LAUNCH_ARGS                  = "--incognito"

# Globals
chrome_instance = None
username = ""
password = ""

def initializeChromeDriver():
    print("Launching ChromeDriver instance")

    # Modify global version of chrome_instance
    global chrome_instance
    # Create chrome instance with pre-defined options and naviage to CAMS
    option = webdriver.ChromeOptions()
    option.add_argument(CHROME_LAUNCH_ARGS)
    chrome_instance = webdriver.Chrome(chrome_options=option)
    chrome_instance.get(CAMS_URL)


def loginCAMS():
    # Modify global version of chrome_instance
    global chrome_instance, username, password


    # Switch to alert and dismiss it
    chrome_instance.switch_to.alert.accept()

    # Get term drop down menu and select first item
    dropDownTermMenu = Select(chrome_instance.find_element_by_id("idterm"))
    dropDownTermMenu.select_by_index(0)

    # If username argument is given, input username in CAMS
    if username != "":
        chrome_instance.find_element_by_id("txtUsername").send_keys(username)

    # If password argument is given, input password in CAMS
    if password != "":
        chrome_instance.find_element_by_id("txtPassword").send_keys(password)

    # If both username and password were given, login automatically
    if username != "" and password != "":
        chrome_instance.find_element_by_id("btnLogin").click()
    else:
        sleep(WEBPAGE_GET_WAIT_TIME)

        print("Waiting for the user to sign in (1 min timeout)")
        try:
            # Wait until the login box is no longer visible
            login_box = (By.XPATH, CAMS_LOGIN_BOX_XPATH)
            is_visible = expected_conditions.visibility_of_element_located(login_box)
            WebDriverWait(chrome_instance, LOGIN_WAIT_TIME).until(is_visible)
        except TimeoutException:
            print("Timed Out")
            chrome_instance.quit()



def scrapeTranscript():
    # Modify global version of chrome_instance
    global chrome_instance
    
    print("navigating to transcript")

    # Navigate to Unofficial Transcript Page
    chrome_instance.get(CAMS_TRANSCRIPT_URL)
    
    # Get inner text of transcript table
    transcript_table = chrome_instance.find_element_by_xpath(CAMS_TRANSCRIPT_TABLE_XPATH).text

    return transcript_table


def scrapeCourseOfferings():
    # Modify global version of chrome_instance
    global chrome_instance

    # Navigate to Course Offerings webpage
    chrome_instance.get(CAMS_COURSES_URL)

    coursesTable = ""

    # Get number of pages of courses
    numOfPagesDiv = chrome_instance.find_element_by_xpath(CAMS_COURSES_NUM_OF_PAGES_XPATH).text
    numOfPages = numOfPagesDiv.split('\n')[-1].split(' ')[-1][:-1]
    
    for i in range(1, int(numOfPages) + 1):
        # Load next page by calling javascript function
        chrome_instance.execute_script("displayNewPage(" + str(i) + ")")

        # Get inner text of courses table and add it to coursesTable
        coursesTable += chrome_instance.find_element_by_xpath(CAMS_COURSES_TABLE_XPATH).text + "\n"
    
    # Remove unnecessary text
    coursesTable = re.sub(r"(Book List)|(Instructor Room Days Date Start Time End Time Max Enr Total Enr)|" +
        r"(Course Offering List)|(Course Course Name Credits Start Date End Date Max Enr Total Enr)", "", coursesTable)

    print(coursesTable)
    return(coursesTable)





#################################################################   
#                   Assuming This Table Format                  #
#################################################################
# EML4951CENGR02                                                #
#                                                               #
# Engineering Design Senior Capstone 2 3 1/7/2019 4/24/2019 24 0#
#                                                               #
# Park, Younggil IST-1000 M Weekly 12:00:00 PM 12:50:00 PM 24 0 #
# Park, Younggil IST-1044 WF Weekly 12:00:00 PM 12:50:00 PM 24 0#
# Park, Younggil IST-1036 F Weekly 1:00:00 PM 1:50:00 PM 24 0   #
#################################################################
def parseCoursesTable(table):
    print("Parsing Courses Table...")
    



#################################################################################
#                           Assuming This Table Format                          #
#################################################################################
# Major(s):  Computer Engineering                                               #
# Birth Date:  8/1/2000                                                         #
# GPA Group: Undergraduate                                                      #
# Term: FA 2018                                                                 #
# Course Course Name Credits Grade Category                                     #
# CHM2045GENS Chemistry 1 3.00 - Curriculum                                     #
# CHM2045LGENS Chemistry 1 Laboratory 1.00 - Curriculum                         #
# ENC1101GEENG English Comp. 1: Expository and Argumentative 3.00 - Curriculum  #
# IDS1380ENGR Introduction to STEM 3.00 - Curriculum                            #
# MAC2311GEMTH Analytic Geometry and Calculus 1 4.00 - Curriculum               #
# SLS1106GE Academic and Professional Skills 1.00 - Curriculum                  #
#   Attempted Earned GPA Hours Grade Points GPA                                 #
# Term 15.00 0.00 0.00 0.00 0.00                                                #
# Cumulative 15.00 0.00 0.00 0.00 0.00                                          #
#################################################################################
def parseTranscriptTable(table):

    print("parsing table text")

    # Split table text at new line characters and extract program name
    program = table.split('\n')[0][11:]

    # Create empty database_data list
    database_data = []

    # Create basic outline of json data
    json_data = {'program': program, 'courses': []}

    # Split the table text at 'Term:'
    split_table = table.split("Term:")

    # Iterate through every term
    for term_block in split_table[1:]:
        # Get list of rows within the term
        rows = term_block.split('\n')
        # Get the term label
        term = rows[0][1:]
        # Get the year from the term label
        year = term.split(' ')[-1]
        # Get the FA or SP semester label
        semester = ' '.join(term.split(' ')[:-1])

        # Get each course row
        courses = rows[2:-3]
        # Create empty semester courses array
        semester_courses = []

        # Iterate through every course row of text
        for course in courses:
            # Skip this row
            if course == '  Attempted Earned GPA Hours Grade Points GPA':
                continue

            # Split the row at ' '
            course_data = course.split(' ')
            # Extract the course information
            code = course_data[0]
            name = ' '.join(course_data[1:-3])
            hours = int(float(course_data[-3]))
            grade = course_data[-2]

            # If not in proper format, set to more standardized format
            code = None if code == '-' else code
            year = None if year == 'NONE' else year
            semester = None if not semester else semester

            # Create course JSON
            course_json = {'course_code': code,
                           'course_name': name,
                           'credit_hours': hours,
                           'grade': grade}

            # Add course JSON to semester JSON
            semester_courses.append(course_json)

            # Add course information to database_data as a new row
            database_data.append((year,
                                  semester,
                                  code,
                                  name,
                                  hours,
                                  grade))

        # Add all the courses to the semester_courses key in json_data
        json_data['courses'].append({term:semester_courses})

    return json_data, database_data


def export_json(json_data):

    print("writing json to file")
    with open('course_json.json', 'w') as output:
        json.dump(json_data,
                  output,
                  indent=4,
                  separators=(',',': '))


def export_database(database_data):

    # Connect to database and get cursor
    con = sqlite3.connect('course_database.db')
    cur = con.cursor()

    # Create query for retrieving number of tables named 'courses'
    query = """
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE type='table' AND name='courses';"""

    # Execute query
    cur.execute(query)

    # If result of query doesn't = 1, create a new courses table
    if cur.fetchall()[0][0] != 1:
        # Create query for creating new courses table
        query = """
            CREATE TABLE courses
                (id integer primary key autoincrement,
                year text,
                semester text,
                course_code text,
                course_name text,
                credit_hours integer,
                letter_grade text)
            """
    else:
        # If table already exists, clear all records
        query = "DELETE FROM courses"

    # Execute titles query
    cur.execute(query)

    # Create query for inserting new courses
    query = """
            INSERT INTO courses
                (year,
                 semester,
                 course_code,
                 course_name,
                 credit_hours,
                 letter_grade)
                 VALUES (?,?,?,?,?,?)
        """

    # Execute fields query, replacing '?' with data for every row in database_data
    cur.executemany(query, database_data)
    # Save the database
    con.commit()
    # Close the connection
    con.close()


def parseCommandLineArguments(argv):
    # Modify global variables
    global username, password

    # Separate the options and argument inputs into separate lists with matching indicies
    try:
        opts, args = getopt.getopt(argv[1:], "hu:p:", ["username=", "password="])
    # If incorrect argument form, display help
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        # If -h option, show commandline usage and exit
        if opt == '-h':
            print("cams_scraper.py -u <username> -p <password>")
            sys.exit()
        # If -u option, update global username variable with argument
        elif opt in ("-u", "--username"):
            username = arg
        # If -p option, update global password variable with argument
        elif opt in ("-p", "--password"):
            password = arg


def main(argv):
    # Parse Command Line Arguments
    parseCommandLineArguments(argv)
    
    # Initialize and login
    initializeChromeDriver()
    loginCAMS()
    
    # Get Transcript Table
    tableTranscript = scrapeTranscript()

    # Get Course Offerings table
    tableCourses = scrapeCourseOfferings()

    # Close chrome_instance
    print("exiting webpage")
    chrome_instance.quit()

    jsonCoursesData, databaseCoursesData = parseCoursesTable(tableCourses)

    # Get JSON and database information from transcript table
    json_transcript_data, database_transcript_data = parseTranscriptTable(tableTranscript)

    # Export transcript data into JSON file
    export_json(json_transcript_data)
    
    # Export transcript data into database file
    export_database(database_transcript_data)


if __name__ == '__main__':
    main(sys.argv)
