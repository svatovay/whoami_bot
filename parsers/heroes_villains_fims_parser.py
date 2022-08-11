import requests
from bs4 import BeautifulSoup


def heroes_films_parser():
    heroes_list = []
    url = 'https://toplists.ru/lucsie-personazi-filmov-vseh-vremen'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for tag in soup.find_all('div', class_='item-title-container'):
        hero_name = tag.find_next('a').get_text().strip()
        hero_films = tag.find_next('span', class_='common-description-snippet').get_text().strip()
        heroes_list.append((hero_name, hero_films))
    return heroes_list


def villians_films_parser():
    villians_list = []
    url = 'https://toplists.ru/lucsie-zlodei-kinematografa-vseh-vremen'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    for tag in soup.find_all('div', class_='item-title-container'):
        villian_name = tag.find_next('a').get_text().strip()
        villian_films = tag.find_next('span', class_='common-description-snippet').get_text().strip()
        villians_list.append((villian_name, villian_films))
    return villians_list
