import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebScraping.helperfunctions.wait import wait_for_full_load

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