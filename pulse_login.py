# **************************************************************************** #
#                                                                              #
#                                                             |\               #
#    pulse_login.py                                     ------| \----          #
#                                                       |    \`  \  |  p       #
#    By: cshepard6055 <cshepard6055@floridapoly.edu>    |  \`-\   \ |  o       #
#                                                       |---\  \   `|  l       #
#    Created: 2018/09/27 01:11:35 by cshepard6055       | ` .\  \   |  y       #
#    Updated: 2018/10/25 09:39:44 by cshepard6055       -------------          #
#                                                                              #
# **************************************************************************** #

from selenium import webdriver
from time import sleep
from os import system
import selenium
import getpass


# DEFINE GLOBALS
WEBDRIVER_SLEEP     = 5
DEBUG_MODE          = True
CANVAS_URL          = "https://pulse.floridapoly.edu"


def chromedriver_get(url, chrome_instance):
    chrome_instance.get(url)
    sleep(WEBDRIVER_SLEEP)


# print debug messages when debug mode is active; otherwise just ignore
def print_debug_messages(debug_message):
    if DEBUG_MODE is True:
        print(debug_message)
    else:
        pass


def pulse_login(chrome_instance):
    print_debug_messages("exec canvas_login()")

    chromedriver_get(CANVAS_URL, chrome_instance)

    # Enter username, password, and submit
    username = input("Username: ")
    password = getpass.getpass("Password: ")

    chrome_instance.find_element_by_id("userNameInput").send_keys(username)
    chrome_instance.find_element_by_id ("passwordInput").send_keys(password)
    chrome_instance.find_element_by_id("submitButton").click()
