'''
from selenium import webdriver
#from selenium.webdriver.common.action_chains import ActionChains
import re
import requests
from pprint import pprint
import random 
from collections import OrderedDict
# from seleniumwire import webdriver
# import Action chains 
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.common.keys import Keys
import time

'''
headers_list = [
{
"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0",
"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
"Accept-Language": "en-US,en;q=0.5",
"Referer": "https://www.google.com/",
"DNT": "1",
"Connection": "keep-alive",
"Upgrade-Insecure-Requests": "1"
},
]
'''
# #headers_list = ["Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0"]
# driver = webdriver.Chrome("chromedriver.exe")
# def interceptor(request):
#     del request.headers['User-Agent']  
#     request.headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'

# driver.request_interceptor = interceptor
# action = ActionChains(driver)
# driver.get('https://www7.animeseries.io/watch/hackgu-returner-episode-1.html')
# print(driver.execute_script("return navigator.userAgent;"))

# time.sleep(20)
# # action.send_keys(Keys.chord(Keys.CONTROL + Keys.SHIFT + "n"))
# # driver.execute_script("window.location.href = https://www.google.com/")
# driver.get('www.google.com')
op = webdriver.ChromeOptions()
op.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome('chromedriver.exe',options=op)
headers = [{"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
           {"userAgent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0"},
           {"userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94"},
           {"userAgent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20060110 Debian/1.5.dfsg-4 Firefox/1.5"},
           {"userAgent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.19 Safari/537.36 Edg/91.0.864.11"}]
#driver.execute_cdp_cmd('Network.setUserAgentOverride', headers)
driver.execute_cdp_cmd('Network.setUserAgentOverride', random.choice(headers))
print(driver.execute_script("return navigator.userAgent;"))
driver.get('https://httpbin.org/headers')
'''
from bs4 import BeautifulSoup
import requests
import re
from urllib.parse import *
import pandas as pd
import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from time import sleep
from random import randint
import random
from collections import OrderedDict

print('***************************************************')
print('#: Anime Starting With Numbers or Symbols')
print('A to Z: Anime Starting With Letter (A to Z)')
print('***************************************************')
search = input('Enter To Get Anime List: ')
print('***************************************************')

an = []
ae= []
ut = []
l = []
th = []
desc = []
g = []
rd = []
st = []
vids = []
dows = []

def write_csv(char,a,b,c,d,e,f):
    data = pd.DataFrame({'Letter': [char],
                         'Name of The Series': [a], 'Thumbnail Image Link': [b], 'Latest Episode': [c],
                         'Release Date/Time': [d], 'Episode Number':[e], 'Video Box Link':[f]})
    #data.to_csv(r'C:\Users\nrohi\Desktop\Anime_Data.csv',index = False) # Write to csv
    data.to_csv(r'C:\Users\nrohi\Desktop\Anime_Data.csv',mode ='a',header = False,index = False) # Append to csv

def write_mysql(char,a,b,c,d):
    conn = mysql.connector.connect(host= "localhost",user= "root",passwd= "password",database= "AnimeDB",)
    cur = conn.cursor()
    #cur.execute("CREATE DATABASE AnimeDB")
    cur.execute("CREATE TABLE Full_Scraper(Letter VARCHAR(250),Name of The Series VARCHAR(250),Thumbnail Image Link VARCHAR(250),Latest Episode VARCHAR(250),Release Date/Time VARCHAR(250)")
    df = pd.DataFrame({'Letter': [char],
                       'Name of The Series': [a], 'Thumbnail Image Link': [b], 'Latest Episode': [c],
                       'Release Date/Time': [d]})
    df.to_sql('Full_Scraper', conn, if_exists='append', index = False, flavor='mysql')
    conn.commit()
    #cur.execute('''SELECT * FROM Full_Scraper''')
    conn.close()

def Special_Charecter_Scraper():
    # SCRAPES THE SPECIAL CHARECTERS (Symbols and Numbers) PAGE OF animeseries.io
    content = requests.get('https://www7.animeseries.io/search/character=special').text
    soup = BeautifulSoup(content, 'lxml')
    anime_name = soup.find_all('div', class_="name")
    #print('Getting Anime Names...')
    for n in anime_name:
        an.append(n.text)
    k = len(an)
    for link in soup.find_all('a', href=True):
        match = re.search('/anime/(hack|eiyuu|eldlive|[0-9]|-2)',link['href'])
        if match != None:
            url = (link['href'].split('/'))[2]
            if url not in l:
                l.append(url)
    epn=[[] for j in range(len(l))]
    epl=[[] for j in range(len(l))]
    gen=[[] for k in range(len(l))]
    for i, element in enumerate(l):
        subcontent = requests.get('https://www7.animeseries.io/anime/'+element).text
        subsoup = BeautifulSoup(subcontent, 'lxml')
        anime_episodes = subsoup.find('span', class_="name")
        #print('Getting Anime Latest Episode...')
        if anime_episodes is None:
            ae.append('No Episodes Uploaded...')
        else:
            ae.append(anime_episodes.text)
        uploaded_time = subsoup.find('span', class_="year")
        #print("Getting Anime Latest Episode's Upload Date/Time...")
        if uploaded_time is None:
            ut.append('Not Released Yet...')
        else:
            ut.append(uploaded_time.text)
        thumbnail_link = subsoup.find('img', class_="img-responsive")
        #print('Getting Anime Thumbnail Image...')
        if thumbnail_link is None:
            th.append('No Thumbnail Image Avilable Yet...')
        else:
            th.append(thumbnail_link.get('src'))
        description = subsoup.find('p')
        if description is None:
            desc.append('No Description Available Yet...')
        else:
            desc.append(description.text)
        status = subsoup.find('a', href="/completed-anime.html")
        if status is None:
            st.append('Status Not Confirmed Yet...')
        else:
            st.append(status.text)
        rdmatch = (re.search("/released-in-\w+",str(subsoup)))
        rdmatch1 = rdmatch.group()
        releasedate = (rdmatch1.split('-')[2]).split('.')[0]
        if rdmatch is None:
            rd.append('Release Date Not Available..')
        else:
            rd.append(releasedate)
        gmatch1 = subsoup.find_all('p', class_="des")
        gmatch2 = re.findall("/genre/([\w\-\s]+)",str(gmatch1))
        genre = [g1.capitalize() for g1 in gmatch2]
        g.append(genre)
    print(len(g))

if search.upper() == '#':
    Special_Charecter_Scraper()