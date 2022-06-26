from bs4 import BeautifulSoup
import requests
from urllib.parse import *

print('***************************************************')
print('Home: Anime in Home Page')
print('***************************************************')
search = input('Enter To Get Anime List: ')
print('***************************************************')

an = []
ae= []
ut = []

def Home_Scraper():
    # SCRAPES THE HOME PAGE OF animeseries.io (ALL PAGES)
    content = requests.get('https://www7.animeseries.io/').text
    soup = BeautifulSoup(content, 'lxml')
    anime_name = soup.find_all('div', class_="name")
    for n in anime_name:
        an.append(n.text)
    anime_episodes = soup.find_all('div', class_="episode")
    for e in anime_episodes:
        ae.append(e.text)
    uploaded_time = soup.find_all('span', class_="time_ago")
    for t in uploaded_time:
        ut.append(t.text)
    k = len(an)
    for i in range(k):
        print('Name of the series -->',an[i])
        print('Latest Episode -->',ae[i])
        print('Released -->',ut[i])
        print('===================================================================================')


if search.upper() == 'HOME':
    Home_Scraper()