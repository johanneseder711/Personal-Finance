import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebScraping.helperfunctions.wait import wait_for_full_load
from WebScraping.helperfunctions.credentials import get_credentials
import time

driver = None
total_dvag_value = 0
counter = 0

# cache this function in streamlit not to rerun it all the time when modifying the script
# should be cached if running test mode but should be turned off when in production mode
# @st.cache(suppress_st_warning=True)
def get_dvag_balance():

    global driver
    global total_dvag_value
    global counter 

    if counter == 0:
        # define the URL for this site
        URL = 'https://www.banking.co.at/banking/login.xhtml?m=45&f=2'
        # get the correct login credentials for this site
        user,pw = get_credentials(URL)

        # start the session
        driver = webdriver.Safari()
        driver.get(URL)
        #driver.maximize_window()

        # wait for full load
        wait_for_full_load(driver,"loginform:benutzername",how='id')
        # enter user and click button
        driver.find_element(By.ID,"loginform:benutzername").send_keys(user)
        driver.find_element(By.ID,"loginform:loginButtonNext").click()

        wait_for_full_load(driver,"loginform:password2c",how='id')
        # enter password and click button
        driver.find_element(By.ID,"loginform:password2c").send_keys(pw)
        driver.find_element(By.ID,"loginform:loginButton").click()
            
        wait_for_full_load(driver,"scastep2:authentication-mobiletan:j_id_gt:tan-per-sms",how='id')
        driver.find_element(By.ID,"scastep2:authentication-mobiletan:j_id_gt:tan-per-sms").click()

        placeholder = st.empty()
        ret = placeholder.number_input('Please insert the LoginTAN that was sent to your phone!',value=0, key='tan',on_change = input_tan)
        if ret != 0:
            placeholder.empty()

        return 0
    elif counter == 1:
        return(total_dvag_value)

def input_tan():
    global driver
    global total_dvag_value
    global counter
    counter += 1
    print(counter)

    tan = st.session_state['tan']

    driver.find_element(By.ID,"scastep2:authentication-mobiletan:mobiletan").send_keys(tan)
    driver.find_element(By.ID,"scastep2:authentication-mobiletan:j_id_gt:login-button-finish").click()

    wait_for_full_load(driver, "content:produkte-tab:form:produkte:produkteTable:table:1:j_id_cr_2_sw_3_2_18:produkt",how='id')

    total_dvag_value = driver.find_element(By.XPATH,"""//*[@id="content:produkte-tab:form:produkte:produkteTable:table:1:j_id_cr_2_sw_3_2_18:produkt"]/div[2]/div/p/span/span[1]""").text.split()[0]

    driver.close()


   