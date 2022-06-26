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
vids = []
dows = []

def random_header_list():
    user_agent_list = []
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
    # Firefox 77 Windows
    {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
    "DNT": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
    },
    # Chrome 83 Mac
    {
    "Connection": "keep-alive",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
    },
    # Chrome 83 Windows 
    {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Referer": "https://www.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
    }
    ]
    ordered_headers_list = []
    for headers in headers_list:
        h = OrderedDict()
    for header,value in headers.items():
        h[header]=value
        ordered_headers_list.append(h)
    url = 'https://httpbin.org/headers'
    for i in range(1,4):
        headers = random.choice(headers_list) #Pick a random browser headers
        r = requests.Session() #Create a request session
        r.headers = headers
        response = r.get(url)
    #print("Request #%d\nUser-Agent Sent:%s\n\nHeaders Recevied by HTTPBin:"%(i,headers['User-Agent']))
    print(response.json())

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
    print('Getting Anime Names...')
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
        tag1 = subsoup.find('div',{"class":"list_episode"})
        tag2 = tag1.find('ul')
        tag3 = tag2.find_all('li')
        for val in tag3:
            ep_links = (val.find('a').get("href")).split('/')[2] # gets episode links
            ep_num = 'Epsidode ' + ((ep_links.split('-')[-1]).split('.')[0]) + ':' # gets episode number
            epl[i].append(ep_links)
            epn[i].append(ep_num)
    print('***************************************************')
    print("Getting Anime's Video Box and Download Links...")
    print('***************************************************')
    for sublist in epl:
        vid= []
        for link in sublist:
            op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            # op.add_argument("--log-level=3")
            #op = webdriver.ChromeOptions()
            op.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome('chromedriver.exe',options=op)#,chrome_options=op)
            headers = [{"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94"},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20060110 Debian/1.5.dfsg-4 Firefox/1.5"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.19 Safari/537.36 Edg/91.0.864.11"}]
            driver.execute_cdp_cmd('Network.setUserAgentOverride', random.choice(headers))
            #print(driver.execute_script("return navigator.userAgent;"))
            driver.get('https://www7.animeseries.io/watch/'+ link)
            sleep(randint(5,15))
            driver.refresh()
            sleep(randint(5,15))
            driver.maximize_window()
            sleep(randint(5,15))
            action = ActionChains(driver)
            action.move_to_element(driver.find_element_by_id("specialButton"))
            action.perform()
            sleep(randint(10,30))
            #sleep(10000)
            driver.refresh()
            video_link = driver.find_element_by_tag_name("iframe").get_attribute('src')
            vid.append(video_link)
            driver.close()
        vids.append(vid)
    for sublist in vids:
        dow = []
        for dlink in sublist:
            op = webdriver.ChromeOptions()
            op.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome('chromedriver.exe',options=op)#,chrome_options=op)
            headers = [{"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94"},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20060110 Debian/1.5.dfsg-4 Firefox/1.5"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.19 Safari/537.36 Edg/91.0.864.11"}]
            driver.execute_cdp_cmd('Network.setUserAgentOverride', random.choice(headers))
            #print(driver.execute_script("return navigator.userAgent;"))
            element = driver.find_element_by_xpath("//div[@aria-label='Play']")
            originalHandle = driver.window_handles[0];    
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            download_link = driver.find_element_by_xpath("//video").get_attribute('src')
            dow.append(download_link)
            sleep(randint(10,20))
            driver.close()
        dows.append(dow)
        

    k = len(an)
    for i in range(k):
        print('Name of The Series   -->' ,an[i])
        print('Thumbnail Image Link -->' ,th[i])
        print('Latest Episode       -->' ,ae[i]) 
        print('Release Date/Time    -->' ,ut[i])
        print('|---------------------------|')
        print('| ↓↓↓↓  EPISODE LINKS ↓↓↓↓  |')
        print('|---------------------------|')
        print(epn[i])
        print('Video Box Link       -->', vids[i])
        print('Download Link        -->', dows[i])
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
    print('Getting Anime Names...')
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
        tag1 = subsoup.find('div',{"class":"list_episode"})
        tag2 = tag1.find('ul')
        tag3 = tag2.find_all('li')
        for val in tag3:
            ep_links = (val.find('a').get("href")).split('/')[2] # gets episode links
            ep_num = 'Epsidode ' + ((ep_links.split('-')[-1]).split('.')[0]) + ':' # gets episode number
            epl[i].append(ep_links)
            epn[i].append(ep_num)
    print('***************************************************')
    print("Getting Anime's Video Box and Download Links...")
    print('***************************************************')
    for sublist in epl:
        vid= []
        for link in sublist:
            op = webdriver.ChromeOptions()
            # op.add_argument('headless')
            # op.add_argument("--log-level=3")
            #op = webdriver.ChromeOptions()
            op.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome('chromedriver.exe',options=op)#,chrome_options=op)
            headers = [{"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94"},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20060110 Debian/1.5.dfsg-4 Firefox/1.5"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.19 Safari/537.36 Edg/91.0.864.11"}]
            driver.execute_cdp_cmd('Network.setUserAgentOverride', random.choice(headers))
            #print(driver.execute_script("return navigator.userAgent;"))
            driver.get('https://www7.animeseries.io/watch/'+ link)
            sleep(randint(5,15))
            driver.refresh()
            sleep(randint(5,15))
            driver.maximize_window()
            sleep(randint(5,15))
            action = ActionChains(driver)
            action.move_to_element(driver.find_element_by_id("specialButton"))
            action.perform()
            sleep(randint(10,30))
            #sleep(10000)
            driver.refresh()
            video_link = driver.find_element_by_tag_name("iframe").get_attribute('src')
            vid.append(video_link)
            driver.close()
        vids.append(vid)
    for sublist in vids:
        dow = []
        for dlink in sublist:
            op = webdriver.ChromeOptions()
            op.add_experimental_option('excludeSwitches', ['enable-logging'])
            driver = webdriver.Chrome('chromedriver.exe',options=op)#,chrome_options=op)
            headers = [{"userAgent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/540.0 (KHTML, like Gecko) Ubuntu/10.10 Chrome/8.1.0.0 Safari/540.0"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36 OPR/76.0.4017.94"},
                    {"userAgent": "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8) Gecko/20060110 Debian/1.5.dfsg-4 Firefox/1.5"},
                    {"userAgent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.19 Safari/537.36 Edg/91.0.864.11"}]
            driver.execute_cdp_cmd('Network.setUserAgentOverride', random.choice(headers))
            #print(driver.execute_script("return navigator.userAgent;"))
            element = driver.find_element_by_xpath("//div[@aria-label='Play']")
            originalHandle = driver.window_handles[0];    
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            download_link = driver.find_element_by_xpath("//video").get_attribute('src')
            dow.append(download_link)
            sleep(randint(10,20))
            driver.close()
        dows.append(dow)       

    k = len(an)
    for i in range(k):
        print('Name of The Series   -->' ,an[i])
        print('Thumbnail Image Link -->' ,th[i])
        print('Latest Episode       -->' ,ae[i]) 
        print('Release Date/Time    -->' ,ut[i])
        print('|---------------------------|')
        print('| ↓↓↓↓  EPISODE LINKS ↓↓↓↓  |')
        print('|---------------------------|')
        print(epn[i])
        print('Video Box Link       -->', vids[i])
        print('Download Link        -->', dows[i])
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