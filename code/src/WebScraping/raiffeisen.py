import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebScraping.helperfunctions.wait import wait_for_full_load
from WebScraping.helperfunctions.credentials import get_credentials


# cache this function in streamlit not to rerun it all the time when modifying the script
# Get Raiffeisen Account Information
@st.cache
def get_raiffaisen_balance():
    # define the url to be scraped
    URL = "https://sso.raiffeisen.at/mein-login/identify"
    # get the correct login credentials for this site
    user, pw = get_credentials(URL)
    
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

    # extract creditcard balance
    total_raiffeisen_creditcard_value = driver.find_elements(By.XPATH, """//*[@id="rds-scrub-item-1-1"]/div/rds-card/div/rds-card-content/span[2]""")[0].text.split()[0]

    # close driver
    driver.close()

    return (total_raiffeisen_giro_value,total_raiffeisen_creditcard_value)