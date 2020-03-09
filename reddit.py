from bs4 import BeautifulSoup
from selenium import webdriver

# import urllib.parse

BASE_URL = "https://www.reddit.com/r/ProgrammingHumor/"
FILE = "html-selenium.txt"
FILE_WAIT = "html-selenium-wait.txt"
# first try
driver = webdriver.Firefox()
driver.get(BASE_URL)
html = driver.page_source
with open(FILE, "w+", encoding="UTF-8") as f:
    f.write(html)
# second try
driver.get(BASE_URL)
driver.implicitly_wait(10)
html = driver.page_source
driver.close()
with open(FILE_WAIT, "w+") as f:
    f.write(html)

soup = BeautifulSoup(html, "html.parser")
title_a_class = ""