import threading

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
import time
import random 
import io
import os
import database

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# mock data  
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

sizes = {
    '24.0': '.lbl0', '24.5': '.lbl1', '25.0': '.lbl2', '25.5': '.lbl3', '26.0':'.lbl4', '26.5': '.lbl5',
    '27.0': '.lbl6', '27.5': '.lbl7', '28.0': '.lbl8', '28.5': '.lbl9', '29.0': '.lbl10', '30.0': '.lbl11'
} 

def booking_architectureandsneakers(url, size, amount, id):
    # driver = webdriver.Chrome(executable_path="/Volumes/Data/ProjectPrograming/python/seleniumdriver/chromedriver")
    # driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.set_window_size(1366, 728)

    driver.get(url)
    print('url', url)

    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'btnCartin')))
        # size
        driver.find_element_by_css_selector(sizes[size]).click()
        driver.find_element_by_css_selector(sizes[size]).click()

        driver.find_element_by_css_selector("#btnCartin").click()
        driver.find_element_by_css_selector("#btnCartin").click()
    except TimeoutException:
        print('time to much 1')  
        # size
        driver.find_element_by_css_selector(sizes[size]).click()
        driver.find_element_by_css_selector(sizes[size]).click()

        driver.find_element_by_css_selector("#btnCartin").click()
        driver.find_element_by_css_selector("#btnCartin").click()

    # add to cart
    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'button--is_light')))
        max_product = int(driver.find_element_by_xpath("//cms-flexible-number-field").get_attribute('max'))
        if int(amount) < max_product:
            driver.find_element_by_xpath(
                "//cms-flexible-number-field/div/div/select/option[@value="+str(amount)+"]").click()
        else:
            driver.find_element_by_xpath(
                "//cms-flexible-number-field/div/div/select/option[@value=" + str(max_product) + "]").click()

        # click booking
        driver.find_element_by_css_selector(".button.button--is_primary.button--is_light").click()
    except TimeoutException:
        print('time to much 2')

    # go to cart
    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'cart')))
        print('xong')
        driver.find_element_by_xpath("//li[@id='cart']/a[not (@class)]").click()
    except TimeoutException:
        print('time to much 3')

    # payment click
    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'checkout_button')))
        print('xong')
        driver.find_element_by_xpath("//div[@class='checkout_button_container']/button").click()
    except TimeoutException:
        print('time to much 4')

    # fill info
    delay = 10  # seconds
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'address_name')))

        # # login
        # driver.find_element_by_css_selector('.customerbar__status').click()
        # delay = 10  # seconds
        # try:
        #     WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'email')))
        #
        #     # driver.find_element_by_xpath("//input[@id='email']").__setattr__('value', 'abc')
        #
        #     email = driver.find_element_by_id("email")
        #     driver.execute_script("arguments[0].click();", email)
        #     driver.execute_script("arguments[0].click();", email)
        #     # email.clear()
        #     # email.send_keys("bot.restock1010@gmail.com")
        #     #
        #     # password = driver.find_element_by_id("password")
        #     # password.clear()
        #     # password.send_keys("Brf3Zdi")
        #     #
        #     # # login click
        #     # driver.find_element_by_css_selector(".button.button--is_success").submit()
        #
        # except TimeoutException:
        #     print('time to much email')

        address_name = driver.find_element_by_id("address_name")
        address_name.clear()
        address_name.send_keys("Le Hong Phuong")

        furigana = driver.find_element_by_id("furigana")
        furigana.clear()
        furigana.send_keys("")

        address_postal_code = driver.find_element_by_id("address_postal_code")
        address_postal_code.clear()
        address_postal_code.send_keys("1508512")

        address_address1 = driver.find_element_by_id("address_address1")
        address_address1.clear()
        address_address1.send_keys("渋谷区桜丘町")

        address_address2 = driver.find_element_by_id("address_address2")
        address_address2.clear()
        address_address2.send_keys("123 address_address2")

        address_phone_number = driver.find_element_by_id("address_phone_number")
        address_phone_number.clear()
        address_phone_number.send_keys("08000123456")

        fax = driver.find_element_by_id("fax")
        fax.clear()
        fax.send_keys("0312341234")

        email = driver.find_element_by_id("email")
        email.clear()
        email.send_keys("helloitpdu@gmail.com")

        # click radio
        radio = driver.find_element_by_xpath("//input[@id='payment_method_650079']")
        driver.execute_script("arguments[0].click();", radio)

        # click booking
        driver.find_element_by_css_selector(".button.button--is_primary").submit()

    except TimeoutException:
        print('time to much 5')

    print('end job booking')
    database.update_status(id)
    # time.sleep(5)
    driver.close() 

def booking(store, pid, size, amount, id):
    print('start job booking')
    if store == 'architectureandsneakers':
        url = 'https://store.architectureandsneakers.com/?pid=' + pid
        booking_architectureandsneakers(url, size, amount, id)

# store = 'architectureandsneakers'
# pid = '151555065'
# size = '27.0'
# amount = 2 

# arrayThreads = []
# for x in range(0, 2):
#     arrayThreads.append(threading.Thread(target=booking, args=(store, pid, size, amount)))

# for x in range(0, 2):
#     arrayThreads[x].start()

# for x in range(0, 2):
#     arrayThreads[x].join()











