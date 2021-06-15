import os
import sys
import time

import requests
from bs4 import BeautifulSoup

from common.common import BASE_URL
from common.db_command import start_session, add_category, add_product, add_image, update_status, update_all_status,\
    check_start_category


def take_data_get(address):
    attempt = 1
    while attempt <= 20:
        try:
            response = requests.get(address)
            return response
        except:
            print(f'Ошибка соеденения с адресом {address} попытка №{attempt}')
            time.sleep(1)
            attempt += 1
    print(f'Нет доступа к адресу {address}')
    exit(1)


def check_dir(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def parse_link(session, elem, parent):
    link = elem.find('a')
    name = link.text
    command = link['href'].split('/')[-2]
    description = ''
    if command != 'All_Product':
        return add_category(session, name, command, description, parent)


def parce_category_product(session, cat, Category):
    link = cat.find('a')['href']
    response_cat = take_data_get(BASE_URL + link)
    cat_soup = BeautifulSoup(response_cat.text, 'lxml')
    products = cat_soup.find_all('a', class_='productItem__image')
    prod_list = []
    for prod in products:
        prod_list.append(prod['href'])
    for product_url in list(set(prod_list)):
        response_prod = take_data_get(BASE_URL + product_url)
        product_soup = BeautifulSoup(response_prod.text, 'lxml')
        try:
            command = product_soup.find('div', class_='productInfo__top-code').text.split('#')[-1]
            name = product_soup.find('div', class_='productInfo__title').text
            description = product_soup.find('div', class_='productInfo__description').text
        except AttributeError:
            print(f" не удалось найти атрибут по адресу {BASE_URL + product_url}")
            print(AttributeError)
            raise AttributeError
        print(f'Сканируем товар {command} ({name})')
        product = add_product(session, name, description, command, None, Category, UPDATE)
        short_image_url = product_soup.find(class_='productInfoImage__preview-image')
        if short_image_url:
            image_url = "https:" + short_image_url['data-big']
            add_image(session, product, image_url)


def start_parce(UPDATE):
    session = start_session()
    if UPDATE:
        start_command = None
    else:
        start_command = check_start_category(session)
    response = take_data_get(BASE_URL + '/shop/')
    soup = BeautifulSoup(response.text, 'lxml')
    parents = soup.find_all('li', class_='subMenu__list-item--more')
    for parent in parents:
        parent_category = parse_link(session, parent, None)
        sub_cat = parent.find_all('li')
        if not sub_cat and parent_category:
            parce_category_product(session, parent, parent_category)
        for cat in sub_cat:
            if start_command is None or parent_category.command == start_command or cat.find('a')['href'].split('/')[-2] == start_command:
                start_command = None
                sub_category = parse_link(session, cat, parent_category)
                parce_category_product(session, cat, sub_category)
                update_status(sub_category, True)
                session.commit()
            if parent_category is not None:
                update_status(parent_category, True)
            session.commit()
        update_all_status(session)
        session.commit()


if __name__ == "__main__":
    try:
        UPDATE = sys.argv[1]
    except IndexError:
        UPDATE = False
    start_parce(UPDATE)
