import time
import csv
from threading import Thread
import requests
from lxml import html

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

    return oll_links


def get_info(oll_links):
    oll_info = []
    for link in oll_links:
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

        oll_info.append(
            {
                'title': tree.xpath('//*[@id="h1-name"]/text()'),
                'company': company,
                'salary': salary,
                'city': place,
            }
        )

    return oll_info


profession = input('Введите итересующую профессию: ')
pages = int(input('Введите к-во страниц для поиска: '))
info = get_info(vacancy_links(profession, pages))

with open(f'{profession}.csv', 'w') as f:
    writer = csv.writer(f, delimiter=',')
    for item in info:
        writer.writerow([item['title'], item['company'], item['salary'], item['city']])

'''def replace_unicode(info):
    salary = []
for i in info:
    info['salary'].append(i['salary'][0].replace('\u202f', ' ').replace('\u2009', ' '))
print(info)
for item in info:
    print(item)
for i in info:
    i['salary'].replace('\u202f', ' ')
    print(i['salary'])
НЕ ПОЛУЧАЕТСЯ УБРАТЬ ЛИШНИЕ СИМВОЛЫ В salary'''

# end = time.perf_counter()
# print(f'{end - start:0.2f}')

# start = time.perf_counter()         ##Не разобрался как теперь ко всему этому прикрутить потоки???
# threads = []
# for page in range(pages):
#     t = Thread(target=get_info, args=(page,))
#     t.start()
#     threads.append(t)
#
# for t in threads:
#     t.join()
# print(threads)
# with open(f'{profession}.csv', 'w') as f:
#     writer = csv.writer(f, delimiter=',')
#     for item in threads:
#         writer.writerow([item['title'], item['company'], item['salary'], item['city']])

# end = time.perf_counter()
# print(f'time with threads = {end - start:0.2f}')
