from selenium import webdriver
from selenium.webdriver.chrome import options
from bs4 import BeautifulSoup
from datetime import datetime
import json
import time
import requests
import csv
import re


def get_page_data(url):
    
    headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36'
    }

    url = url
    r = requests.get(url = url, headers = headers)
    with open('page_source.html', 'w', encoding='UTF-8') as file:
        file.write(r.text)

def get_all_pages():
    headers ={
        'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.837 YaBrowser/23.9.4.837 Yowser/2.5 Safari/537.36'
    }

    with open('page_source.html', encoding = 'UTF-8') as file:
        src = file.read()
    soup = BeautifulSoup(src, 'lxml')
    page_count = int(soup.find('div', class_ = 'paginator-count color-darkest-gray').find('b').text)
    j=1
    num = 1
    for i in range(1, page_count, 20):
        r = requests.get(f'https://domik65.ru/list?city=ys&page={j}&search_query=714d18e323a2577bf49a71bfbf7834ee')
        with open(f'data/page_source_{j}.html', 'w', encoding = 'UTF-8') as file:
            file.write(r.text)
        print(f'Create page_{j}')
        time.sleep(0.5)
        j+=1 
        num+=1  
    return num

def get_data(page_count):

    cur_date = datetime.now().strftime('%d_%m_%Y')

    with open (f'Apartinfo_{cur_date}.csv', 'w', encoding = 'UTF-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Название',
                'Адрес',
                'Ссылка',
                'Цена'
            )
        )

    for page in range(1, page_count):
        with open(f'data/page_source_{page}.html', encoding = 'UTF-8') as file:
            src = file.read()
        
        soup = BeautifulSoup(src, 'lxml')
        all_cards = soup.find_all('div', class_ = 'relative w-100')

        for card in all_cards:
            price_data = card.find('span', class_ = 'offer-price-value').text.strip()
            name_data = card.find('div', class_ = 'list-card-title').text.strip()
            adress_data = card.find('div', class_ = 'list-card-address flex y-center').text.strip()
            link_data = f"https://domik65.ru{card.find('a').get('href').replace('?search_query=714d18e323a2577bf49a71bfbf7834ee', '').rstrip()}"


            with open (f'Apartinfo_{cur_date}.csv', 'a', encoding = 'UTF-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        name_data,
                        adress_data,
                        link_data,
                        price_data
                    )
                )
            




def main():
    get_page_data('https://domik65.ru/list?city=ys&page=1&search_query=714d18e323a2577bf49a71bfbf7834ee')
    page_count = get_all_pages()
    get_data(page_count = page_count)

if __name__ == '__main__':
    main()