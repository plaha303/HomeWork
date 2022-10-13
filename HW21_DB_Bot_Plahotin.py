# -*- coding: utf-8 -*-
import time
from threading import Thread
import csv
import requests
from lxml import html
import sqlite3

HOST = 'https://www.say7.info/cook/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'
}


def get_dish_links(url):
    dish_links = []
    r = requests.get(HOST, headers=HEADERS)
    tree = html.fromstring(r.text)
    last_page = tree.xpath('//*[@id="content"]/div[4]/ul/li[13]/a/@href')
    last_page = int(last_page[0].split('start-')[1][:-5])
    page = 20
    while page <= last_page + 20:
        r = requests.get(f'{url}' + f'linkz_start-{page}.html', headers=HEADERS)
        tree = html.fromstring(r.text)
        links = tree.xpath('//*[@id="content"]/div[5]/ul/li/a/@href')
        if links[0] == '//www.say7.info/cook/':
            links = tree.xpath('//*[@id="content"]/div[4]/ul/li/a/@href')
        for link in links:
            dish_links.append(f'https:' + f'{link}')
        page += 20

    return dish_links


def get_info(links: list):
    info = []
    for item in links:
        r = requests.get(item, headers=HEADERS)
        tree = html.fromstring(r.text)
        product_name = tree.xpath('//*[@id="content"]/div[3]/h1/text()')
        if product_name == []:
            product_name = tree.xpath('//*[@id="content"]/div[4]/h1/text()')
        description = tree.xpath('//*[@id="content"]/div[3]/div[1]/text()')[:-2]
        if description == []:
            description = tree.xpath('//*[@id="content"]/div[4]/div[1]/text()')[:-2]
        description = ''.join(description)
        ingredients = tree.xpath('//*[@class="p-ingredient"]/text()')
        ingredients = '\n'.join(ingredients)
        recipe = tree.xpath('//*[@itemprop="recipeInstructions"]/text()')
        recipe = '\n'.join(recipe)
        product = {
            'category': tree.xpath('//*[@id="sitepos"]/ul/li[2]/a/text()')[0],
            'img link': tree.xpath('/html/body/div[4]/a/img/@src')[0],
            'product name': product_name[0],
            'description': description,
            'ingredients': ingredients,
            'recipe': recipe,
        }
        info.append(product)
    return info


link = get_dish_links(HOST)
link_2 = link[0: 5]
# print(link_2)

info = get_info(link_2)
print(info)

# r = requests.get(url='https://www.say7.info/cook/recipe/581-Zapekanka-risom.html')
# tree = html.fromstring(r.text)
# pages = tree.xpath('/html/body/div[5]/div[1]/div[4]/div[5]/p/text()')
# print(r.status_code)
# print(pages)
