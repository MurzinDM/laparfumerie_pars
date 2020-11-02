import requests
import re
from bs4 import BeautifulSoup
import math
from multiprocessing import Pool

USERNAME = 'vcp-1-2016@yandex.ru'
PASSWORD = '9s25JpBt7n5qS2W'
CITY = 'Санкт-Петербург'
cookies = ''


def auth_in_site(user_name: str, password: str) -> requests.cookies.RequestsCookieJar:
    url1 = 'http://www.laparfumerie.org/index.php?app=core&module=global&section=login&do=process'
    headers1 = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Length': '197',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'www.laparfumerie.org',
        'Origin': 'http://www.laparfumerie.org',
        'Referer': 'http://www.laparfumerie.org/index.php?app=core&module=global&section=login',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'}
    data1 = {'referer': 'http://www.laparfumerie.org/index.php?',
             'username': user_name,
             'password': password,
             'anonymous': '1',
             'rulesagreement': '1'}
    s = requests.post(url1, headers=headers1, data=data1)
    global cookies
    cookies = s.cookies


def site_data() -> str:
    url2 = 'http://www.laparfumerie.org/index.php?app=fillings&category=Все&gorod=' + CITY + 'fftype=2&st=0'
    params = {'app': 'fillings', 'gorod': 'Санкт-Петербург', 'fftype': '2'}
    s2 = requests.get(url2, cookies=cookies, params=params)
    return s2.text


def get_number_offer(text: str = None) -> int:
    text = site_data()
    soup = BeautifulSoup(text, features="lxml")
    soup = soup.find_all('option', selected='selected', title='Санкт-Петербург')
    offer_number = int(re.findall(r'\(+(\d+)', str(soup))[0])
    page_number = math.ceil(offer_number // 30) + 1
    return page_number


def get_link_list(page_number: int = None) -> list:
    page_number = get_number_offer()
    link_list = []
    for st_value in range(0, page_number):
        base_url = 'http://www.laparfumerie.org/index.php?app=fillings&category=Все&gorod=' + CITY \
                   + 'fftype=2&st=' + str(st_value * 30)
        link_list.append(base_url)
    return link_list


def get_text(url: str = None) -> str:
    params = {'app': 'fillings', 'gorod': 'Санкт-Петербург', 'fftype': '2'}
    data = requests.get(url, cookies=cookies, params=params)
    return data.text


def adapt_text(text: str) -> list:
    soup = BeautifulSoup(text, 'lxml')
    data = soup.find_all('div', style="position:relative;top:2px;left:20px;width:140px;height:1.5em;")
    lot_number = []
    brand = []
    name = []
    quantity_on_sale = []
    quantity_all = []
    price = []
    unit = []
    for i in range(0, len(data)):
        data2 = BeautifulSoup(str(data[i]), 'lxml')
        lot_number.append(int(re.findall(r'lot\/+(\d+)-', str(data2.a['href']))[0]))
        sep = str(data2.a.text).partition(',')
        brand.append(sep[0])
        name.append(sep[2])
    return brand, name


def save_file(text: str):
    with open('file_db.txt', 'a', encoding='utf-8') as file:
        file.write(text)
    print('запись')


def make_all(url):
    text = get_text(url)
    data = adapt_text(text)
    save_file(data)
пше

# def main():
#     auth_in_site(USERNAME, PASSWORD)
#     link_list = get_link_list()
#     with Pool(35) as p:
#         p.map(make_all, link_list)

def main():
    text = get_text('http://www.laparfumerie.org/index.php?app=fillings&category=Все&gorod=' + CITY + 'fftype=2&st=0')
    data = adapt_text(text)
    return print(data, len(data))


if __name__ == '__main__':
    main()
