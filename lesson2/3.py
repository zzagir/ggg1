# https://www.superjob.ru/vacancy/search/?keywords=python
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
import pandas as pd
import json

main_url = 'https://www.hh.ru'
params = {'area':'0'}
vac = input('Введите вакансию: ')
headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
response = requests.get(main_url+'/search/vacancy?&text='+vac+'&', headers=headers)

with open('hh.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

html = ''
with open('hh.html', 'r', encoding='utf-8') as f:
    html = f.read()

soup = bs(html, 'html.parser')

vacancies = soup.find_all(class_="vacancy-serp-item")
print(len(vacancies))

all_vacancies = []

for vacancy in vacancies:
    vacancies_info = {}

    vacancy_anchor = vacancy.find('a')
    for i in vacancy_anchor:
        vacancy_name = i.getText()
        vacancies_info['vacancy_name'] = vacancy_name

    vacancy_link = vacancy.find('a', class_='bloko-link')['href']
    vacancies_info['vacancy_link'] = vacancy_link

    salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if not salary:
        salary_min = None
        salary_max = None
        salary_currency = None
        if not salary_currency:
            vacancy_anchor = vacancy.find('span', class_='bloko-header-section-3')
    else:
        salary = salary.getText() \
            .replace(u'\xa0', u'')

        salary = re.split(r'\s|-', salary)
        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[1])
        salary_currency = salary[2]

    vacancies_info['salary_min'] = salary_min
    vacancies_info['salary_max'] = salary_max
    vacancies_info['salary_currency'] = salary_currency
    vacancies_info['site'] = main_url

    pprint(vacancies_info)
