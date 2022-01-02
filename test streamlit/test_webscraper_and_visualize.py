from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import time

import streamlit as st


# Functions

def wait_for_full_load(driver, xpath):
    '''
    A function that takes in an xpath of an element and a driver (browser).
    The function will be exited as soon as the element is available on the site.
    '''
    waiting = True
    while waiting:
        # check if at least one element is already available on the site
        elements = driver.find_elements(By.XPATH, xpath)
        if len(elements)!=0: 
            return;
        else:
            time.sleep(1)


# define the path to the credentials file
PATH_CREDENTIALS = '../Credentials/my_credentials.txt'

# read in the file line by line and store the credentials
# new credentials start with a # and the name of the credentials site
# in the next two lines there are the username and password stored in the file
credentials_dict = {}
with open(PATH_CREDENTIALS) as f:
    for line in f:
        if line.startswith('#'):
            credentials_dict[line.split()[1]] = [next(f).split()[0],next(f).split()[0]]


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
    driver.find_element(By.ID,"password_app").send_keys(pw)
    # click the login button
    driver.find_element(By.CSS_SELECTOR,"button.button").click()

    # close current tab
    driver.close()

    # get current window (the new tab)
    window = driver.window_handles

    # switch to the new window
    driver.switch_to.window(window[0])

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


# Get Raiffeisen Account Information
@st.cache
def get_raiffaisen_balance():

    # define the url to be scraped
    URL = "https://sso.raiffeisen.at/mein-login/identify"
    # start the session
    driver = webdriver.Safari()
    driver.get(URL)
    driver.maximize_window()
    # wait for loading the page
    wait_for_full_load(driver, "//*[@id='rds-select-0']")

    # click on the drop down menu
    driver.find_element(By.XPATH,"//*[@id='rds-select-0']").click()
    # to select the right bank (Oberösterreich)
    driver.find_element(By.XPATH,"//*[@id='rds-option-4']/span").click()


    # extract login information from dict
    for key in credentials_dict.keys():
        if key.lower() in URL:
            user, pw = credentials_dict[key]

    # input username
    driver.find_element(By.XPATH,"//*[@id='rds-input-0']").send_keys(user)

    # input password
    driver.find_element(By.XPATH,"//*[@id='rds-input-1']").send_keys(pw)

    # click on submit button to log in
    driver.find_element(By.XPATH,"//*[@id='rds-grid-row-5-column-5']/button").click()

    # wait until the site has loaded
    wait_for_full_load(driver, """//*[@id="rds-scrub-item-1-0"]/div/rds-card/div/rds-card-content/span[2]""")

    # extract information on account balance
    total_raiffeisen_giro_value = driver.find_elements(By.XPATH, """//*[@id="rds-scrub-item-1-0"]/div/rds-card/div/rds-card-content/span[2]""")[0].text.split()[0]
    print('total raiffaisen giro balance: ',total_raiffeisen_giro_value)

    # extract creditcard balance
    total_raiffeisen_creditcard_value = driver.find_elements(By.XPATH, """//*[@id="rds-scrub-item-1-1"]/div/rds-card/div/rds-card-content/span[2]""")[0].text.split()[0]
    print('total raiffaisen creditcard balance: ',total_raiffeisen_creditcard_value)

    # close driver
    driver.close()

    return (total_raiffeisen_giro_value,total_raiffeisen_creditcard_value)


# call functions
total_flatex_value,absolute_profit = get_flatex_balance()
total_raiffeisen_giro_value,total_raiffeisen_creditcard_value = get_raiffaisen_balance()

# Display information with streamlit

# create page title
st.title('My first streamlit application')


# display values via metrics
col1, col2, col3 = st.columns(3)
col1.metric(label="Flatex Total Value", value=total_flatex_value + " €", delta=absolute_profit + " €")
col2.metric(label='Raiffeisen Giro Total Value', value = total_raiffeisen_giro_value + " €")
col3.metric(label='Raiffeisen Creditcard Total Value', value = total_raiffeisen_creditcard_value + " €")