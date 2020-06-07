from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import mysql.connector

import time

import re

conn = mysql.connector.connect(user = 'root', password = 'uinndouzu7', host = 'localhost', database = 'systemengine_pre')
cur = conn.cursor(buffered=True)

#ここからスクレイピング
URL_base = "https://xtech.nikkei.com/top/it/?bn=column&M=20&P="
Selector = "body"

op = Options()
op.add_argument("--disable-gpu");
op.add_argument("--disable-extensions");
op.add_argument("--proxy-server='direct://'");
op.add_argument("--proxy-bypass-list=*");
op.add_argument("--start-maximized");
op.add_argument("--headless");
driver = webdriver.Chrome(chrome_options=op)

driver_main_search = webdriver.Chrome(chrome_options=op)

count = 0

sql_website = 'NikkeiXTech'


for url_Number in range(1, 11):
    driver.get(URL_base + str(url_Number))
    
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Selector))
    )   
    
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    
    print('URL:' + URL_base + str(url_Number))
    print()
    
    for el1 in soup.select('.l-main_primary'):
        News_count = 0
        News_Limit = 0
        
        for el2 in el1.select('.l-section'):
            if News_count == 1:
                News_count += 1
                continue
            elif News_count == 3:
                break
            else:
                for el3 in el2.select('li'):
                    try:
                        if News_Limit == 20:
                            raise AttributeError
                        sql_url = 'https://xtech.nikkei.com' + el3.find('a').get('href')

                        driver_main_search.get(sql_url)
                        
                        WebDriverWait(driver_main_search, 30).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, Selector))
                        )   
                        
                        soup_main_search = BeautifulSoup(driver_main_search.page_source, features="html.parser")
                        
                        sql_title = soup_main_search.find('title').getText()
                        
                        sql_day = soup_main_search.select_one('.p-article_header_date').getText()
                        sql_day = re.sub("\\D", "", sql_day) + '000000'
                        
                        print('Title=', sql_title)
                        print('url=', sql_url)
                        print('datetime=', sql_day)
                        print()
                        
                        time.sleep(15)

                        
                        News_Limit += 1
                        
                    except AttributeError:
                        time.sleep(15)
                        break
                News_count += 1
                    