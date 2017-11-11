from selenium import webdriver

browser = webdriver.Chrome('C:\Program Files (x86)\Python36-32\Scripts\chromedriver.exe')
browser.get('http://localhost:8000')

assert 'Django' in browser.title

