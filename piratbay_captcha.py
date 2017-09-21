import io
import os
import random
import string
import urllib.request
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

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


# Google API

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

# Performs label detection on the image file

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

time.sleep(2)

# credentials of new user
username = 'strelock' + random.choice(string.ascii_letters) + str(random.randint(1990, 2005))
email = username + '@hotmail.com'
password = random.choice(string.ascii_letters) + random.choice(string.ascii_letters) + random.choice(string.ascii_letters) \
           + str(random.randint(1990, 2005)) + random.choice(string.ascii_letters)
repeat_password = password
captcha = block_text

# fill registration form
username_element_id  = "username"
email_element_id     = "email"
password_element_id  = "password"
password2_element_id = "password2"
captcha_eleemnt_id   = "recaptcha_response_field"

username_element  = browser.find_element_by_id(username_element_id)
email_element     = browser.find_element_by_id(email_element_id)
password_element  = browser.find_element_by_id(password_element_id)
password2_element = browser.find_element_by_id(password2_element_id)
captcha_elememt   = browser.find_element_by_id(captcha_eleemnt_id)

username_element.send_keys(username)
email_element.send_keys(email)
password_element.send_keys(password)
password2_element.send_keys(repeat_password)
captcha_elememt.send_keys(captcha)