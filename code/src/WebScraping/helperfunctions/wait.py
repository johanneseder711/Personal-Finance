import time
from selenium.webdriver.common.by import By

def wait_for_full_load(driver, path, how='xpath'):
    '''
    A function that takes in an xpath of an element and a driver (browser).
    The function will be exited as soon as the element is available on the site.
    '''
    waiting = True
    while waiting:
        # check if at least one element is already available on the site
        if how == 'xpath': 
            elements = driver.find_elements(By.XPATH, path)
            print(len(elements))
        elif how == 'css':
            elements = driver.find_elements(By.CSS_SELECTOR, path)
        elif how == 'id':
            elements = driver.find_elements(By.ID, path)
        
        if len(elements)!=0: 
            waiting = False
            return;
        else:
            time.sleep(1)