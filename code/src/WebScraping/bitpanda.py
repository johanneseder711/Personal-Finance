import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from WebScraping.helperfunctions.wait import wait_for_full_load
from WebScraping.helperfunctions.credentials import get_credentials
import time

def expand_shadow_element(driver, element):
  shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
  return shadow_root


def get_bitpanda_balance():
    # define the URL for this site
    URL = 'https://account.bitpanda.com/login'
    # get the correct login credentials for this site
    user,pw = get_credentials(URL)

    # start the session
    driver = webdriver.Safari()
    driver.get(URL)
    #driver.maximize_window()
    time.sleep(5)
    # find the shadow root element to accept cookies
    root1 = driver.find_element(By.TAG_NAME,'bpc-cookie-banner')
    shadow_root1 = expand_shadow_element(driver, root1)

    # accept cookies
    # FINISHED HERE -> STILL NOT WORKING TO FIND THE CORRECT ROOT SHADOW ELEMENT AND ACCEPT COOKIES
    # REFFERE https://stackoverflow.com/questions/37384458/how-to-handle-elements-inside-shadow-dom-from-selenium
    expanded_driver = shadow_root1.find_element(By.CLASS_NAME,"bpc-cookie-accept-button").click()

    # wait for full load
    wait_for_full_load(expanded_driver,"login-submit",how='id')
    # input username/email
    expanded_driver.find_element(By.ID,"email").send_keys(user)
    time.sleep(5)
    # input password
    expanded_driver.find_element(By.ID,"password']").send_keys(pw)

    # click login submit button
    expanded_driver.find_element(By.ID, "login-submit").click()
