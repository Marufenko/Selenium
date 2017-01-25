from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('D:\Selenium Testing\chromedriver_win32\chromedriver.exe')
driver.get("http://www.python.org")
assert "Python" in driver.title
print('Step1 - PASS')
elem = driver.find_element_by_name("q")
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
print('Step2 - PASS')
driver.close()