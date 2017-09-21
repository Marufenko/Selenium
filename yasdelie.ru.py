from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests_

driver = webdriver.Chrome('D:\Selenium Testing\chromedriver_win32\chromedriver.exe')
driver.get("http://yasdelie.ru/")

#1 - verify title
assert "Ясделие" in driver.title

#2 - verify that link with text 'Ясделие' exists
element = driver.find_element_by_xpath("//div[@class='navbar-header page-scroll']/a[contains(text(),'Ясделие')]")

#3 - verify the link with text 'Ясделие' return user for start page which is the same as we use in driver.get
cur_page = driver.current_url
driver.find_element_by_xpath("//div[@class='navbar-header page-scroll']/a[contains(text(),'Ясделие')]").click()
# driver.implicitly_wait(3) # seconds
link_page = driver.current_url
assert cur_page == link_page

#4 - verify other links in navbar
driver.find_element_by_xpath('//li[@class="page-scroll"]/a[@href="#whatis"]')
driver.find_element_by_xpath('//li[@class="page-scroll"]/a[@href="#portfolio"]')
driver.find_element_by_xpath('//li[@class="page-scroll"]/a[@href="#about"]')
driver.find_element_by_xpath('//li[@class="page-scroll"]/a[@href="#contact"]')

#5 - verify that all images on page are available
for i in driver.find_elements_by_xpath('//img'):
    r = requests_.get(i.get_attribute('src'))  # verif that all img src returns 200 OK response by GET HTTP
    assert r.status_code == 200, 'image with src=%r is not available' %i.get_attribute('src')  # error description

driver.close()