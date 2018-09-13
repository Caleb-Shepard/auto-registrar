from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep

import json
from pprint import pprint, pformat
import sqlite3

def scrape():
    
    cams_url = "https://cams.floridapoly.org/student/login.asp"

    print("setting up browser")
    option = webdriver.ChromeOptions()
    option.add_argument("--incognito")
    browser = webdriver.Chrome(chrome_options=option)
    browser.get(cams_url)

    sleep(10)
    
    print("waiting for the user to sign in (1 min timeout)")
    try:
        check_item = (By.XPATH, "//*[@id='LeftSide']")
        is_visible = EC.visibility_of_element_located(check_item)
        WebDriverWait(browser, 60).until(is_visible)
    except TimeoutException:
        print("Timed Out")
        browser.quit()

    print("navigating to transcript")
    browser.find_element_by_id('spTranscript').click()
    table = browser.find_element_by_xpath("//*[@id='mainBody']/div[2]").text

    print("exiting webpage")
    browser.quit()
    return table

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

    titles = """CREATE TABLE courses
                (id integer primary key autoincrement,
                 year text,
                 semester text,
                 course_code text,
                 course_name text,
                 credit_hours integer,
                 letter_grade text)"""

    fields = """INSERT INTO courses
                (year,
                 semester,
                 course_code,
                 course_name,
                 credit_hours,
                 letter_grade)
                 VALUES (?,?,?,?,?,?)"""

    con = sqlite3.connect('course_database.db')
    cur = con.cursor()
    cur.execute(titles)
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
