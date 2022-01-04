import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebScraping.helperfunctions.wait import wait_for_full_load
from WebScraping.helperfunctions.credentials import get_credentials
import time

# cache this function in streamlit not to rerun it all the time when modifying the script
@st.cache
def get_bank99_balance():
    # define the URL for this site
    URL = 'https://banking.ing.at/online-banking/wicket/login?0'
    # get the correct login credentials for this site
    user,pw = get_credentials(URL)

    # start the session
    driver = webdriver.Safari()
    driver.get(URL)
    #driver.maximize_window()

    wait_for_full_load(driver,"number",how='id')

    # enter credentials and click button
    driver.find_element(By.ID,"number").send_keys(user)
    driver.find_element(By.ID,"pin").send_keys(pw)
    # click the login button
    driver.find_element(By.XPATH,"//*[@id='id3']/fieldset/div[5]/input").click()

    wait_for_full_load(driver,"""//*[@id="idd"]/div[3]/div/div/div/table/tbody/tr[2]/td[4]/span""")

    total_bank99_balance = driver.find_element(By.XPATH,"""//*[@id="idd"]/div[3]/div/div/div/table/tbody/tr[2]/td[4]/span""").text.split()[1]
    driver.close()

    return total_bank99_balance