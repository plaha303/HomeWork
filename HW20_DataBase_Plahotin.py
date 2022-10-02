import time
import csv
from threading import Thread
import sqlite3
import requests
from lxml import html


def create_vakancy_db(table: str, item: dict):
    keys = list(item.keys())
    req = f'CREATE TABLE IF NOT EXISTS {table}('

    for i in range(len(keys)):
        req += f'{keys[i]} TEXT, '
    req = req[:-2] + ')'

    connect = sqlite3.connect('vacancy.db')
    cursor = connect.cursor()
    cursor.execute(req)
    connect.commit()


def add_db_info(info: dict, table):
    connect = sqlite3.connect('vacancy.db')
    cursor = connect.cursor()

    keys = list(info.keys())
    req = f'INSERT INTO {table}('

    for i in range(len(keys)):
        req += f'{keys[i]}, '
    req = req[:-2] + ')VALUES('
    for i in range(len(keys)):
        req += "'" + info[keys[i]] + "', "
    req = req[:-2] + ');'
    # cursor.execute(f'SELECT * FROM {table}')    #ВОЗМОЖНО ЛИ СДЕДАТЬ ПРОВЕРКУ ЗАПИСИ НА НАЛИЧИЕ
    # if cursor.fetchall() is None:               #БЕЗ УНИКАЛЬНЫХ ЗНАЧЕНИЙ ЗАПИСИ???
    cursor.execute(req)
    connect.commit()
    print('запись данных закончена')


HOST = 'https://www.work.ua'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def vacancy_links(profession: str, page: int):
    oll_links = []
    for i in range(page):
        r = requests.get(f'https://www.work.ua/ru/jobs-{profession}/?page={page + 1}',
                         headers=HEADERS)
        tree = html.fromstring(r.text)

        links = tree.xpath('//*[@id="pjax-job-list"]/div[*]/h2/a/@href')
        for link in links:
            oll_links.append(link)

    return oll_links, profession


def get_info(oll_links):
    oll_info = []
    prof = oll_links[1]
    for link in oll_links[0]:
        r = requests.get(HOST + link)
        tree = html.fromstring(r.text)
        company = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[1]/p[1]/a/img/@title')
        if company == []:
            company = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[1]/p[3]/a/b/text()')
        if company == []:
            company = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[1]/p[2]/a/b/text()')
        if company == []:
            company = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[2]/p[2]/a/b/text()')
        if company == []:
            company = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[2]/p[4]/a/b/text()')
        salary = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[1]/p[2]/b/text()')
        if salary == []:
            salary = tree.xpath('//*[@id="center"]/div/div[2]/div[1]/div[3]/div[2]/p[3]/b/text()')
        if salary == []:
            salary = ['обсуждается на собеседовании']
        place = tree.xpath('//*[@id="center"]/div/div[1]/div/ol/li[2]/a/span[1]/text()')

        vacancy_info = {
            'title': tree.xpath('//*[@id="h1-name"]/text()')[0],
            'company': company[0],
            'salary': salary[0],
            'city': place[0],
        }

        oll_info.append(vacancy_info)
    create_vakancy_db(prof, oll_info[0])
    for item in oll_info:
        add_db_info(item, prof)

    return oll_info


profession = input('Введите итересующую профессию: ')
pages = int(input('Введите к-во страниц для поиска: '))
info = get_info(vacancy_links(profession, pages))
