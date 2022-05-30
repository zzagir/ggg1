from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time


s = Service('../chromedriver.exe')
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)

driver.get('https://account.mail.ru/login')

input = driver.find_element(By.NAME, "username")
input.send_keys("study.ai_172@mail.ru")
input.send_keys(Keys.ENTER)

input = driver.find_element(By.NAME, "password")
input.send_keys("NextPassword172#")
input.send_keys(Keys.ENTER)


mails = []

for i in range(1):
    time.sleep(3)
    items = driver.find_elements(By.XPATH, "//a[contains(@class,'llc llc_normal')]")
    actions = ActionChains(driver)

    for item in items:
        link = item.get_attribute('href')
        info = item.find_element(By.CLASS_NAME, 'llc__content')
        author = info.find_element(By.CLASS_NAME, 'll-crpt').get_attribute('title')
        subject = info.find_element(By.CLASS_NAME, 'll-sj__normal').text
        date = item.find_element(By.CLASS_NAME, 'llc__item_date').get_attribute('title')
        mail = {'author': author, 'date': date, 'subject': subject, 'link': link}
        mails.append(mail)


    actions.move_to_element(items[-1])
    actions.perform()

for mail in mails:
    driver.get(mail['link'])
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, "//*[contains(@id, '_BODY')]")))
    mail['text'] = driver.find_element(By.XPATH, "//*[contains(@id, '_BODY')]").text
    driver.back()
    WebDriverWait(driver, 5).until(EC.title_contains('Входящие'))

driver.quit()

print()

db_name = 'mails_db'
client = MongoClient('127.0.0.1', 27017)
db = client[db_name]
db.mails_db.insert_many(mails)
