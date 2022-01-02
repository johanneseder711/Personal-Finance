#!/usr/bin/env python
# coding: utf-8

# In[4]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import re
import time

import streamlit as st


# In[2]:


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


# In[5]:


# define the url to be scraped
URL = "https://www.flatex.at/login/"
# start the session
driver = webdriver.Safari()
driver.maximize_window()
driver.get(URL)
# accept cookies
driver.find_element(By.CLASS_NAME,"sg-cookie-optin-box-button-accept-all").click()

for key in credentials_dict.keys():
    if key.lower() in URL:
        user, pw = credentials_dict[key]
# wait until the site is fully loaded
time.sleep(1)
# store current window
current_window = driver.window_handles[0]

# enter credentials
driver.find_element_by_id('uname_app').send_keys(user)
driver.find_element_by_id("password_app").send_keys(pw)
# click the login button
driver.find_element(By.CSS_SELECTOR,"button.button").click()

# wait until webpage has loaded
time.sleep(3)

#get first child window
windows = driver.window_handles

# extract what the new window is
windows.remove(current_window)
new_window = windows[0]

# switch to the new window
driver.switch_to.window(new_window)


# expand overview of the account
driver.find_element(By.XPATH, "//td[text()='KONTO & DEPOT']").click()

# click on depotbestand to get to full overview
driver.find_element(By.XPATH, "//div[text()='Depotbestand']").click()

# wait to load
time.sleep(1)

# extract information on account balance
total_flatex_value = driver.find_elements(By.XPATH, "//td[@class='C4 footer']")[0].text.split()[0]
total_flatex_paid = driver.find_elements(By.XPATH, "//td[@class='C4 footer']")[1].text.split()[0]
absolute_profit = driver.find_elements(By.XPATH, "//td[@class='C5 footer']")[0].text.split()[0]
relative_profit = driver.find_elements(By.XPATH, "//td[@class='C5 footer']")[1].text.split()[0]

driver.close()

#get first child window
chwd = driver.window_handles

driver.switch_to.window(chwd[0])

driver.close()

st.metric(label="Flatex Total Value", value=total_flatex_value + " €", delta=absolute_profit + " €")

