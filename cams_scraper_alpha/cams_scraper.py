# **************************************************************************** #
#                                                                              #
#                                                             |\               #
#    cams.py                                            ------| \----          #
#                                                       |    \`  \  |  p       #
#    By: mattgiallourakis <mattgiallourakis@floridapoly.edu>`-\   \ |  o       #
#                                                       |---\  \   `|  l       #
#    Created: 2018/09/25 19:53:53 by mattgiallourakis   | ` .\  \   |  y       #
#    Updated: 2018/09/25 19:54:33 by cshepard6055       -------------          #
#                                                                              #
# **************************************************************************** #

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

# DEFINE GLOBALS
WEBPAGE_GET_WAIT_TIME   = 10
LOGIN_WAIT_TIME         = 60

TRANSCRIPT_TABLE_XPATH  = "//*[@id='mainBody']/div[2]"
CAMS_LOGIN_BOX_XPATH    = "//*[@id='LeftSide']"

CAMS_URL                = "https://cams.floridapoly.org/student/login.asp"
CAMS_TRANSCRIPT_URL     = "https://cams.floridapoly.org/student/cePortalTranscript.asp"
CHROME_LAUNCH_ARGS      = "--incognito"


def scrape():

    print("Launching ChromeDriver instance")

    # Create chrome instance with pre-defined options and naviage to CAMS
    option = webdriver.ChromeOptions()
    option.add_argument(CHROME_LAUNCH_ARGS)
    chrome_instance = webdriver.Chrome(chrome_options=option)
    chrome_instance.get(CAMS_URL)

    # Switch to alert and dismiss it
    chrome_instance.switch_to.alert.accept()

    # Get term drop down menu and select first item
    dropDownTermMenu = Select(chrome_instance.find_element_by_id("idterm"))
    dropDownTermMenu.select_by_index(0)

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

    print("navigating to transcript")

    # Navigate to Unofficial Transcript Page
    chrome_instance.get(CAMS_TRANSCRIPT_URL)
    
    # Get inner text of transcript table
    transcript_table = chrome_instance.find_element_by_xpath("//*[@id='mainBody']/div[2]").text

    # Exit and return table HTML text
    print("exiting webpage")
    chrome_instance.quit()
    return transcript_table

def parse(table):

    print("parsing table text")
    program = table.split('\n')[0][11:]

    database_data = []
    json_data = {'program': program, 'courses': []}

    split_table = table.split("Term:")

    for term_block in split_table[1:]:
        rows = term_block.split('\n')
        term = rows[0][1:]
        year = term.split(' ')[-1]
        semester = ' '.join(term.split(' ')[:-1])

        courses = rows[2:-3]
        semester_courses = []

        for course in courses:
            if course == '  Attempted Earned GPA Hours Grade Points GPA':
                continue
            course_data = course.split(' ')
            code = course_data[0]
            name = ' '.join(course_data[1:-3])
            hours = int(float(course_data[-3]))
            grade = course_data[-2]

            code = None if code == '-' else code
            year = None if year == 'NONE' else year
            semester = None if not semester else semester

            course_json = {'course_code': code,
                           'course_name': name,
                           'credit_hours': hours,
                           'grade': grade}

            semester_courses.append(course_json)

            database_data.append((year,
                                  semester,
                                  code,
                                  name,
                                  hours,
                                  grade))

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
    con = sqlite3.connect('course_database.db')
    cur = con.cursor()

    query = """
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE type='table' AND name='courses';"""

    cur.execute(query)

    if cur.fetchall()[0][0] != 1:
        titles = """
            CREATE TABLE courses
                (id integer primary key autoincrement,
                year text,
                semester text,
                course_code text,
                course_name text,
                credit_hours integer,
                letter_grade text)
            """
        cur.execute(titles)

    fields = """INSERT INTO courses
                (year,
                 semester,
                 course_code,
                 course_name,
                 credit_hours,
                 letter_grade)
                 VALUES (?,?,?,?,?,?)"""

    cur.executemany(fields, database_data)
    con.commit()
    con.close()


def main():

    table = scrape()
    json_data, database_data = parse(table)
    export_json(json_data)
    export_database(database_data)


if __name__ == '__main__':
    main()
