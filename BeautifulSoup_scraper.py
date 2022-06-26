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
    for i, element in enumerate(l):
        subcontent = requests.get('https://www7.animeseries.io/anime/'+element).text
        subsoup = BeautifulSoup(subcontent, 'lxml')
        print('Getting Anime Name...')
        anime_episodes = subsoup.find('span', class_="name")
        print('Getting Anime Latest Episode...')
        if anime_episodes is None:
            ae.append('No Episodes Uploaded...')
        else:
            ae.append(anime_episodes.text)
        uploaded_time = subsoup.find('span', class_="year")
        print("Getting Anime Latest Episode's Upload Date/Time...")
        if uploaded_time is None:
            ut.append('Not Released Yet...')
        else:
            ut.append(uploaded_time.text)
        thumbnail_link = subsoup.find('img', class_="img-responsive")
        print('Getting Anime Thumbnail Image...')
        if thumbnail_link is None:
            th.append('No Thumbnail Image Avilable Yet...')
        else:
            th.append(thumbnail_link.get('src'))
        description = subsoup.find('p')
        print('Getting Anime Description...')
        if description is None:
            desc.append('No Description Available Yet...')
        else:
            desc.append(description.text)
        status = subsoup.find('a', href="/completed-anime.html")
        print('Getting Anime Status..')
        if status is None:
            st.append('Status Not Confirmed Yet...')
        else:
            st.append(status.text)
        rdmatch = (re.search("/released-in-\w+",str(subsoup)))
        print('Getting Release Year of Anime...')
        if rdmatch is None:
            rd.append('Release Date Not Available..')
        else:
            rdmatch1 = rdmatch.group()
            releasedate = (rdmatch1.split('-')[2]).split('.')[0]
            rd.append(releasedate)
        gmatch1 = subsoup.find_all('p', class_="des")
        gmatch2 = re.findall("/genre/([\w\-\s]+)",str(gmatch1))
        print('Getting Anime Genre...')
        print('--------------------------------------------------------')
        genre = [g1.capitalize() for g1 in gmatch2]
        g.append(genre)
        tag1 = subsoup.find('div',{"class":"list_episode"})
        if tag1 is not None:
            tag2 = tag1.find('ul')
            tag3 = tag2.find_all('li')
        for val in tag3:
            ep_links = (val.find('a').get("href")).split('/')[2] # gets episode links
            ep_num = 'Episode ' + ((ep_links.split('-')[-1]).split('.')[0]) + ':' # gets episode number
            epl[i].append(ep_links)
            epn[i].append(ep_num)
    # print('***************************************************')
    # print("Getting Anime's Video Box and Download Links...")
    # print('***************************************************')
    print('**************************************')
    print("Getting Anime's Video Box Links...")
    print('**************************************')
    for sublist in epl:
        vid= []
        for link in sublist:
            content = requests.get('https://www7.animeseries.io/watch/'+ link).text
            soup = BeautifulSoup(content, 'lxml')
            tagA = soup.find('div', class_="watch_video watch-iframe")
            if tagA is not None:
                vidbox_links = tagA.find('iframe').get('src')
                vid.append(vidbox_links)
        vids.append(vid)

    # for sublist in vids:
    #     dow = []
    #     for dlink in sublist:
    #         ###################
    #     dows.append(dow)


    k = len(an)
    for i in range(k):
        print('Name of The Series       -->' ,an[i])
        print('Thumbnail Image Link     -->' ,th[i])
        print('Description              -->' ,desc[i])
        print('Status                   -->' ,st[i])
        print('Anime Released           -->' ,rd[i])
        print('Genre                    -->' ,g[i])
        print('Latest Episode           -->' ,ae[i]) 
        print('Latest Release Date/Time -->' ,ut[i])
        print('|---------------------------|')
        print('| ↓↓↓↓  EPISODE LINKS ↓↓↓↓  |')
        print('|---------------------------|')
        #print(epn[i])
        print('Video Box Link       -->',vids[i])
        print('================================================================================================================')
 
        #char = 'Special Charecter'
        #write_csv(char,an[i],th[i],ae[i],ut[i],epn[i],vids[i])
    #print('Data Updated to CSV File (Opened with Excel)')
        #write_mysql(char,an[i],th[i],ae[i],ut[i])
    #print('Data Updated to AnimeDB - Full_Scraper Table in MySQL')

def Letter_Scraper():
    # SCRAPES THE LETTERS (A to Z) PAGE OF animeseries.io
    content = requests.get('https://www7.animeseries.io/search/character='+char).text
    soup = BeautifulSoup(content, 'lxml')
    anime_name = soup.find_all('div', class_="name")
    for n in anime_name:
        an.append(n.text)
    k = len(an)
    for link in soup.find_all('a', href=True):
        match = (re.search('/anime/-?'+char.lower(),link['href']) or 
                 re.search('/anime/-?'+char,link['href']) or 
                 re.search('/anime/z-kai-cross-road.html',link['href']) or 
                 re.search('/anime/valvrave-the-liberator.html',link['href']) or 
                 re.search('/anime/ore-no-nounai-sentakushi-ga-gakuen-lovecome-o-zenryoku-de-jama-shiteiru.html',link['href']) or 
                 re.search('/anime/om-and-jerry-movie-the-great-chases.html',link['href']) or 
                 re.search('/anime/pilots-love-song.html',link['href']) or 
                 re.search('/anime/romance-of-the-three-kingdoms.html',link['href']))
        if match != None:
            url = (link['href'].split('/'))[2]
            if url not in l:
                l.append(url)
    epn=[[] for j in range(len(l))]
    epl=[[] for j in range(len(l))]
    for i, element in enumerate(l):
        subcontent = requests.get('https://www7.animeseries.io/anime/'+element).text
        subsoup = BeautifulSoup(subcontent, 'lxml')
        print('Getting Anime Name...')
        anime_episodes = subsoup.find('span', class_="name")
        print('Getting Anime Latest Episode...')
        if anime_episodes is None:
            ae.append('No Episodes Uploaded...')
        else:
            ae.append(anime_episodes.text)
        uploaded_time = subsoup.find('span', class_="year")
        print("Getting Anime Latest Episode's Upload Date/Time...")
        if uploaded_time is None:
            ut.append('Not Released Yet...')
        else:
            ut.append(uploaded_time.text)
        thumbnail_link = subsoup.find('img', class_="img-responsive")
        print('Getting Anime Thumbnail Image...')
        if thumbnail_link is None:
            th.append('No Thumbnail Image Avilable Yet...')
        else:
            th.append(thumbnail_link.get('src'))
        description = subsoup.find('p')
        print('Getting Anime Description...')
        if description is None:
            desc.append('No Description Available Yet...')
        else:
            desc.append(description.text)
        status = subsoup.find('a', href="/completed-anime.html")
        print('Getting Anime Status..')
        if status is None:
            st.append('Status Not Confirmed Yet...')
        else:
            st.append(status.text)
        rdmatch = (re.search("/released-in-\w+",str(subsoup)))
        print('Getting Release Year of Anime...')
        if rdmatch is None:
            rd.append('Release Date Not Available..')
        else:
            rdmatch1 = rdmatch.group()
            releasedate = (rdmatch1.split('-')[2]).split('.')[0]
            rd.append(releasedate)
        gmatch1 = subsoup.find_all('p', class_="des")
        gmatch2 = re.findall("/genre/([\w\-\s]+)",str(gmatch1))
        print('Getting Anime Genre...')
        print('--------------------------------------------------------')
        genre = [g1.capitalize() for g1 in gmatch2]
        g.append(genre)
        tag1 = subsoup.find('div',{"class":"list_episode"})
        if tag1 is not None:
            tag2 = tag1.find('ul')
            tag3 = tag2.find_all('li')
        for val in tag3:
            ep_links = (val.find('a').get("href")).split('/')[2] # gets episode links
            ep_num = 'Episode ' + ((ep_links.split('-')[-1]).split('.')[0]) + ':' # gets episode number
            epl[i].append(ep_links)
            epn[i].append(ep_num)
    # print('***************************************************')
    # print("Getting Anime's Video Box and Download Links...")
    # print('***************************************************')
    print('**************************************')
    print("Getting Anime's Video Box Links...")
    print('**************************************')
    for sublist in epl:
        vid= []
        for link in sublist:
            content = requests.get('https://www7.animeseries.io/watch/'+ link).text
            soup = BeautifulSoup(content, 'lxml')
            tagA = soup.find('div', class_="watch_video watch-iframe")
            if tagA is not None:
                vidbox_links = tagA.find('iframe').get('src')
                vid.append(vidbox_links)
        vids.append(vid)

    # for sublist in vids:
    #     dow = []
    #     for dlink in sublist:
    #         ###################
    #     dows.append(dow)


    k = len(an)
    for i in range(k):
        print('Name of The Series       -->' ,an[i])
        print('Thumbnail Image Link     -->' ,th[i])
        print('Description              -->' ,desc[i])
        print('Status                   -->' ,st[i])
        print('Anime Released           -->' ,rd[i])
        print('Genre                    -->' ,g[i])
        print('Latest Episode           -->' ,ae[i]) 
        print('Latest Release Date/Time -->' ,ut[i])
        print('|---------------------------|')
        print('| ↓↓↓↓  EPISODE LINKS ↓↓↓↓  |')
        print('|---------------------------|')
        #print(epn[i])
        print('Video Box Link       -->',vids[i])
        print('================================================================================================================')

        #write_csv(char,an[i],th[i],ae[i],ut[i],epn[i],vids[i])
    #print('Data Updated to CSV File (Opened with Excel)')
        #write_mysql(char,an[i],th[i],ae[i],ut[i])
    #print('Data Updated to AnimeDB - Full_Scraper Table in MySQL')
    
if search.upper() == '#':
    Special_Charecter_Scraper()
elif search.upper() == 'A' or 'B' or 'C' or 'D' or 'E' or 'F' or 'G' or 'H' or 'I' or 'J' or 'K' or 'L' or 'M' or 'N' or 'O' or 'P' or 'Q' or 'R' or 'S' or 'T' or 'U' or 'V' or 'W' or 'X' or 'Y' or 'Z':
    char = search.upper()
    Letter_Scraper()