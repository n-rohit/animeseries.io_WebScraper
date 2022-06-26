from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import re
from urllib.parse import *
import pandas as pd
import mysql.connector

print('***************************************************')
print('#: Anime Starting With Numbers or Symbols')
print('A to Z: Anime Starting With Letter (A to Z)')
print('***************************************************')
search = input('Enter To Get Anime List: ')
print('***************************************************')

op = webdriver.ChromeOptions()
op.add_argument('headless')

an = []
ae= []
ut = []
l = []
th = []
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
    global op
    driver = webdriver.Chrome('chromedriver.exe',options=op)
    driver.get("https://www7.animeseries.io/search/character=special")
    anime_name = driver.find_elements_by_class_name("name")
    for n in anime_name:
        an.append(n.text)
    for link in driver.find_elements_by_tag_name("a"):
        print(link.text)
        '''
        url = (link.split('/'))
        print(url)
        driver.close()
        
            if url not in l:
                l.append(url)
    epn=[[] for j in range(len(l))]
    epl=[[] for j in range(len(l))]
    for i, element in enumerate(l):
        subcontent = requests.get('https://www7.animeseries.io/anime/'+element).text
        subsoup = BeautifulSoup(subcontent, 'lxml')
        anime_episodes = subsoup.find('span', class_="name")
        if anime_episodes is None:
            ae.append('No Episodes Uploaded...')
        else:
            ae.append(anime_episodes.text)
        uploaded_time = subsoup.find('span', class_="year")
        if uploaded_time is None:
            ut.append('Not Released Yet...')
        else:
            ut.append(uploaded_time.text)
        thumbnail_link = subsoup.find('img', class_="img-responsive")
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
    for sublist in epl:
        vid= []
        for link in sublist:
            driver = webdriver.Chrome('chromedriver.exe')
            driver.get('https://www7.animeseries.io/watch/'+ link)
            video_link = driver.find_element_by_tag_name("iframe").get_attribute('src')
            vid.append(video_link)
            driver.close()      
        vids.append(vid)
    for sublist in vids:
        dow = []
        for dlink in sublist:
            driver = webdriver.Chrome('chromedriver.exe')
            driver.get("https:"+ dlink)
            element = driver.find_element_by_xpath("//div[@aria-label='Play']")
            originalHandle = driver.window_handles[0];    
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            download_link = driver.find_element_by_xpath("//video").get_attribute('src')
            dow.append(download_link)
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
'''
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
        anime_episodes = subsoup.find('span', class_="name")
        if anime_episodes is None:
            ae.append('No Episodes Uploaded...')
        else:
            ae.append(anime_episodes.text)
        uploaded_time = subsoup.find('span', class_="year")
        if uploaded_time is None:
            ut.append('Not Released Yet...')
        else:
            ut.append(uploaded_time.text)
        thumbnail_link = subsoup.find('img', class_="img-responsive")
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
    for sublist in epl:
        vid= []
        for link in sublist:
            driver = webdriver.Chrome('chromedriver.exe')
            driver.get('https://www7.animeseries.io/watch/'+ link)
            video_link = driver.find_element_by_tag_name("iframe").get_attribute('src')
            vid.append(video_link)
            driver.close()      
        vids.append(vid)
    for sublist in vids:
        dow = []
        for dlink in sublist:
            driver = webdriver.Chrome('chromedriver.exe')
            driver.get("https:"+ dlink)
            element = driver.find_element_by_xpath("//div[@aria-label='Play']")
            originalHandle = driver.window_handles[0];    
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            ActionChains(driver).move_to_element(element).click().perform()
            driver.switch_to.window(originalHandle)
            download_link = driver.find_element_by_xpath("//video").get_attribute('src')
            dow.append(download_link)
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