import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebScraping.helperfunctions.wait import wait_for_full_load
import time

# define the path to the credentials file
PATH_CREDENTIALS = '../../data/Credentials/my_credentials.txt'

# read in the file line by line and store the credentials
# new credentials start with a # and the name of the credentials site
# in the next two lines there are the username and password stored in the file
credentials_dict = {}
with open(PATH_CREDENTIALS) as f:
    for line in f:
        if line.startswith('#'):
            credentials_dict[line.split()[1]] = [next(f).split()[0],next(f).split()[0]]


# cache this function in streamlit not to rerun it all the time when modifying the script
# Get Flatex Account Information
@st.cache
def get_flatex_balance():

    # define the url to be scraped
    URL = "https://www.flatex.at/login/"
    # start the session
    driver = webdriver.Safari()
    driver.get(URL)
    driver.maximize_window()

    for key in credentials_dict.keys():
        if key.lower() in URL:
            user, pw = credentials_dict[key]

    # accept cookies
    driver.find_element(By.CLASS_NAME,"sg-cookie-optin-box-button-accept-all").click()

    # enter credentials
    driver.find_element(By.ID,'uname_app').send_keys(user)
    time.sleep(1)
    driver.find_element(By.ID,"password_app").send_keys(pw)
    # click the login button
    driver.find_element(By.CSS_SELECTOR,"button.button").click()

    # close current tab
    driver.close()

    # get current window (the new tab)
    windows = driver.window_handles

    # switch to the new window
    driver.switch_to.window(windows[0])

    # wait for full load
    wait_for_full_load(driver, "//td[text()='KONTO & DEPOT']")

    # expand overview of the account
    driver.find_element(By.XPATH, "//td[text()='KONTO & DEPOT']").click()

    # click on depotbestand to get to full overview
    driver.find_element(By.XPATH, "//div[text()='Depotbestand']").click()

    # wait to load
    wait_for_full_load(driver, "//td[@class='C4 footer']")

    # extract information on account balance
    total_flatex_value = driver.find_elements(By.XPATH, "//td[@class='C4 footer']")[0].text.split()[0]
    total_flatex_paid = driver.find_elements(By.XPATH, "//td[@class='C4 footer']")[1].text.split()[0]
    absolute_profit = driver.find_elements(By.XPATH, "//td[@class='C5 footer']")[0].text.split()[0]
    relative_profit = driver.find_elements(By.XPATH, "//td[@class='C5 footer']")[1].text.split()[0]
    driver.close()
    print('total flatex value: ',total_flatex_value)
    print('total flatex paid: ', total_flatex_paid)
    return (total_flatex_value,absolute_profit)