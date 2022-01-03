import time
from selenium.webdriver.common.by import By

def wait_for_full_load(driver, path, xpath=True):
    '''
    A function that takes in an xpath of an element and a driver (browser).
    The function will be exited as soon as the element is available on the site.
    '''
    waiting = True
    while waiting:
        # check if at least one element is already available on the site
        if xpath: 
            elements = driver.find_elements(By.XPATH, path)
        else:
            elements = driver.find_elements(By.CSS_SELECTOR, path)
        if len(elements)!=0: 
            return;
        else:
            time.sleep(1)