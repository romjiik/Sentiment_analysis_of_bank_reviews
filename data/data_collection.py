import requests
from bs4 import BeautifulSoup
from lxml import html
import re
import json
import pandas as pd
import numpy as np
from tqdm import tqdm
from datetime import datetime
from collections import Counter

url = 'https://www.banki.ru/services/responses/list/?is_countable=on&page={}'
num_of_web_pages = 20
new_url = []
for x in tqdm(range(num_of_web_pages)):#500 это примерно 12к отзывов
    response = requests.get(url.format(x), timeout=(10, 200))
    soup = BeautifulSoup(response.text, features='lxml')
    for link in soup.find_all('a', class_="link-simple", href=re.compile('/services/responses/bank/response/')):
        if link not in new_url:
            new_url.append(link['href'])

new_url = ['https://www.banki.ru' + elem for elem in new_url]   

#класс для того, чтобы избавиться от слэша в исходном джсоне и каких-то других ненужных символов
#https://stackoverflow.com/questions/65910282/jsondecodeerror-invalid-escape-when-parsing-from-python
class LazyDecoder(json.JSONDecoder):
    def decode(self, s, **kwargs):
        regex_replacements = [
            (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
            (re.compile(r',(\s*])'), r'\1'),
        ]
        for regex, replacement in regex_replacements:
            s = regex.sub(replacement, s)
        return super().decode(s, **kwargs)
        
results = pd.DataFrame()

for i in tqdm(range(num_of_web_pages)):
    print(new_url[i])
    response = requests.get(new_url[i], timeout=(10, 200))
    #review and so on
    if response.status_code != 204:
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
        except ValueError:
            print('empty json')
    scripts = soup.find('script', type="application/ld+json")
    extract = json.loads(str(scripts)[38:-11], cls=LazyDecoder, strict=False)
    
    #datetime, number of views and comments
    spans = soup.find_all('span', {'class': "l10fac986"})
    date = spans[0].get_text().strip().replace('.','/')
    dttm = datetime.strptime(date, '%d/%m/%Y %H:%M')
    view = spans[1].get_text().strip()
    if len(spans) > 2:
        comments = spans[2].get_text().strip()
    else:
        comments = 0
    
    #более детальная оценка
    #названия категорий
    rating_title = soup.find_all('div', {'class': 'text-size-6'})
    for i in range(len(rating_title)):
        rating_title[i] = rating_title[i].get_text()
    #значения категорий
    multilabel = soup.find_all('div', {'class': ['l61f54b7b','le102b2d3']}) #l61f54b7b-закрашенный, le102b2d3-пустой
    # [multilabel[i] = multilabel[i]['class'] for i in range(len(multilabel))]
    if len(multilabel) > 0:
        for i in range(len(multilabel)):
            multilabel[i] = multilabel[i]['class']
        multilabel = np.array(multilabel).reshape((len(rating_title),3))
        multilabel[0]
        multilabel_rating = []
        for i in range(len(multilabel)):
            multilabel_rating.append(Counter(multilabel[i]).get('l61f54b7b'))
    res = {rating_title[i]: multilabel_rating[i] for i in range(len(rating_title))}
    empty = {'Прозрачные условия': None, 'Вежливые сотрудники': None, 
             'Доступность и поддержка': None, 'Удобство приложения, сайта': None}
    for key, values in empty.items():
        if key not in res:
            res[key] = empty[key]
    res = sorted(res.items())
    
    #bank
    image = soup.find('img', {'class': 'lazy-load'})
    bank = image['alt']
    
    #into dataset
    to_insert = {
        'bank': bank,
        'type': [extract['author']['@type']],
        'user_name': [extract['author']['name']],
        'review_title': [extract['name']],
        'review': extract['author']['reviewBody'],
        'review_dttm': dttm,
        'review_views': view,
        'review_comments': comments,
        'rating_value': extract['reviewRating']['ratingValue'],
        res[0][0]: res[0][1], 
        res[1][0]: res[0][1],
        res[2][0]: res[0][1],
        res[3][0]: res[0][1]
    }
    results = pd.concat([results, pd.DataFrame(to_insert)], ignore_index=True)
    #итеративное сохранение
    if num_of_web_pages % 1000 == 0:
        results.to_csv('/Users/r.berdyshev/Documents/Programs/HSE/Course_work/raw_review_dataset.csv', 
                       index=False, date_format='%d/%m/%Y %H:%M')

results.to_csv('/Users/r.berdyshev/Documents/Programs/HSE/Course_work/raw_review_dataset.csv', 
               index=False, date_format='%d/%m/%Y %H:%M')
# убираем все небуквенные символы
regex = re.compile(r'[А-Яа-яёЁ0-9!?.,()-]+')

def words_only(text, regex=regex):
    try:
        return ' '.join(regex.findall(text))
    except:
        return []

df = pd.read_csv('raw_review_dataset.csv')
df['review'] = df['review'].apply(words_only)
df['review_title'] = df['review_title'].apply(words_only)
df.to_csv('/Users/r.berdyshev/Documents/Programs/HSE/Course_work/review_dataset.csv', 
               index=False, date_format='%d/%m/%Y %H:%M')