from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request
import os

# open thepiratebay
main_page_link = 'https://thepiratebay.org'
browser = webdriver.Chrome('chromedriver.exe')
browser.get(main_page_link)

# go to "Registration"
registration_element_xpath = "//a[contains(text(),'Register')]"
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, registration_element_xpath)))
registration_link = browser.find_element_by_xpath(registration_element_xpath)
registration_link.click()

# captcha
captcha_element_id = 'recaptcha_challenge_image'
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, captcha_element_id)))
captcha_element = browser.find_elements_by_id('recaptcha_challenge_image')
assert len(captcha_element) == 1, 'More then one captcha link were found'  # error description
for i in captcha_element:
    urllib.request.urlretrieve(i.get_attribute('src'), "captcha.jpg")

# os.remove("captcha.jpg")