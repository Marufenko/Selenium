import io
import os
import random
import string
import time
import urllib

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# elements farm
main_page_link             = 'https://en.wikipedia.org'
registration_element_xpath = "//a[contains(text(), 'Create account')]"
log_out_element_xpath      = "//a[contains(text(), 'Log out')]"
captcha_img_class          = 'fancycaptcha-image'
username_field_id          = 'wpName2'
password_field_id          = 'wpPassword2'
re_password_field_id       = 'wpRetype'
email_field_id             = 'wpEmail'
captcha_field_id           = 'mw-input-captchaWord'
create_account_button_id   = 'wpCreateaccount'


# go to..
browser = webdriver.Chrome('chromedriver.exe')
browser.get(main_page_link)

# where is our 'registration' page?
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, registration_element_xpath)))
registration_link = browser.find_element_by_xpath(registration_element_xpath)
registration_link.click()

# let's fetch captcha
WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, captcha_img_class)))
captcha_element = browser.find_elements_by_class_name(captcha_img_class)
assert len(captcha_element) == 1, 'More then one captcha element were found'  # error description
for i in captcha_element:
    urllib.request.urlretrieve(i.get_attribute('src'), "captcha.jpg")




# Magic happens here

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    'captcha.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs text detection on the image file

response = client.document_text_detection(image=image)
document = response.full_text_annotation

for page in document.pages:
    for block in page.blocks:
        block_words = []
        for paragraph in block.paragraphs:
            block_words.extend(paragraph.words)

        block_symbols = []
        for word in block_words:
            block_symbols.extend(word.symbols)

        # there is our captcha
        block_text = ''
        for symbol in block_symbols:
            block_text = block_text + symbol.text

os.remove("captcha.jpg")


# generate some test data

username_data    = 'strelock_' + random.choice(string.ascii_letters) + str(random.randint(1990, 2005))
password_data    = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) \
                   + str(random.randint(1990, 2005)) + random.choice(string.ascii_letters)
re_password_data = password_data
email_data       = username_data + '@hotmail.com'
captcha_data     = block_text

time.sleep(1)

# let's fill the form
username_element    = browser.find_element_by_id(username_field_id)
password_element    = browser.find_element_by_id(password_field_id)
re_password_element = browser.find_element_by_id(re_password_field_id)
email_element       = browser.find_element_by_id(email_field_id)
captcha_elememt     = browser.find_element_by_id(captcha_field_id)

username_element.send_keys(username_data)
password_element.send_keys(password_data)
re_password_element.send_keys(re_password_data)
email_element.send_keys(email_data)
captcha_elememt.send_keys(captcha_data)

time.sleep(5)

browser.find_element_by_id(create_account_button_id).click()

# verify registration
try:
    log_out_element = WebDriverWait(browser, 5).until(EC.presence_of_element_located((By.XPATH, log_out_element_xpath)))
    print('Done')
    print('username: {}'.format(username_data))
    print('password: {}'.format(password_data))
except TimeoutException:
    print("It's FAIL")