import requests
import re
from bs4 import BeautifulSoup


def actors_parser():
    actors_list = []
    actor_name_re = r'[а-яА-ЯеЁё ]+'
    url = 'https://cinewest.ru/amerikanskie-aktery-top-50-gollivudskih-muzhchin/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for tag in soup.find_all('h2'):
        actor_name = re.match(actor_name_re, tag.get_text())
        if actor_name:
            actors_list.append(actor_name[0])
    return tuple(actors_list)


def actresses_parser():
    actresses_list = []
    url = 'https://iglamour.com.ua/samyye-krasivyye-aktrisy/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for tag in soup.find_all('figcaption'):
        actresses_list.append(tag.get_text().split(': ')[1])
    return tuple(actresses_list)


def characters_films_parser(character: str):
    result_list = []
    urls = {
        'heroes': 'https://toplists.ru/lucsie-personazi-filmov-vseh-vremen',
        'villians': 'https://toplists.ru/lucsie-zlodei-kinematografa-vseh-vremen'
    }
    response = requests.get(urls[character])
    soup = BeautifulSoup(response.content, 'html.parser')
    for tag in soup.find_all('div', class_='item-title-container'):
        _name = tag.find_next('a').get_text().strip()
        _films = tag.find_next('span', class_='common-description-snippet').get_text().strip()
        result_list.append((_name, _films))
    return tuple(result_list)
