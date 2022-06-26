from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

op = webdriver.ChromeOptions()
op.add_argument('headless')
op.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(r'D:\MyStuff\Internship Stuff\Germa Software Solutions\animeseries.io webscraper\chromedriver.exe',options=op)#,chrome_options=op)
driver.get('https://www7.animeseries.io/watch/hackgu-returner-episode-1.html')
action = ActionChains(driver)
action.move_to_element(driver.find_element_by_id("specialButton"))
action.perform()
video_link = driver.find_element_by_tag_name("iframe").get_attribute('src')
print(video_link)
driver.close()