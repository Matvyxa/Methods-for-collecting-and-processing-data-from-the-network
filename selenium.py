from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient
import time
import re

login = 'study.ai_172'
pwd = 'NextPassword172'
host = 'https://account.mail.ru/login'

chrome_options = Options()
chrome_options.add_argument('start-max')
driver = webdriver.Chrome(
    executable_path='C:\Учеба\chromedriver.exe',
    options=chrome_options
)

driver.get(host)

login_field = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME, 'username'))
)
time.sleep(3)
login_field.send_keys(login)
login_field.submit()
time.sleep(2)
password_field = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.NAME, 'password'))
)
password_field.send_keys(pwd)
password_field.submit()
time.sleep(2)
inbox_element = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'nav__item_active'))
)
time.sleep(2)
title = inbox_element.get_attribute('title')
regex = r"Входящие, (\d*) "
count_emails = int(re.search(regex, title).group(1))
print(f'Всего писем: {count_emails}')

url_marker = WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.CLASS_NAME, 'js-letter-list-item'))
)
url_list = driver.find_elements_by_class_name('js-letter-list-item')
url_set = set()

for a in url_list:
    url_set.add(a.get_attribute('href'))

while len(url_set) != count_emails:
    actions = ActionChains(driver)
    actions.move_to_element(url_list[-1])
    actions.perform()
    time.sleep(3)
    url_list = driver.find_elements_by_class_name('js-letter-list-item')
    for a in url_list:
        url_set.add(a.get_attribute('href'))
    print(f'Количество собранных ссылок: {len(url_set)}')

emails = []
for a in url_set:
    driver.get(a)
    letter_author_wrapper = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'letter_author')))
    email = {
        'letter_author': letter_author_wrapper.find_elements_by_class_name('letter-contact').get_attribute('title'),
        'letter_date': letter_author_wrapper.find_elements_by_class_name('letter__date').text,
        'letter_title': driver.find_elements_by_class_name('thread__subject').text,
        'letter_body': driver.find_elements_by_class_name('letter-body').text
    }
    emails.append(email)
    print(f'Обратная ссылка: {a}')

client = MongoClient('127.0.0,1', 27017)
db = client['emails']
db.inbox.insert_many(emails)

print('Конец')
