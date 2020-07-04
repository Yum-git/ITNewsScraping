from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

import mysql.connector

import time

import re

import datetime

import sys

dt_now = datetime.datetime.now()
CurrentTime = int(dt_now.strftime('%y%m'))

try:
    #sqlpassword please
    SQLPass = ''
    conn = mysql.connector.connect(user = 'root', password = SQLPass, host = 'localhost', database = 'systemengine_pre')
except Exception:
    print('PassWord is incorrect.This App is Exit.')
    sys.exit()
cur = conn.cursor(buffered=True)

#ここからスクレイピング
URL = "https://www.itmedia.co.jp/news/subtop/archive/"
URL_base = "https://www.itmedia.co.jp/news/subtop/archive/"
Selector = "body"

op = Options()
op.add_argument("--disable-gpu");
op.add_argument("--disable-extensions");
op.add_argument("--proxy-server='direct://'");
op.add_argument("--proxy-bypass-list=*");
op.add_argument("--start-maximized");
op.add_argument("--headless");
driver = webdriver.Chrome(chrome_options=op)

driver_firstdown = webdriver.Chrome(chrome_options=op)

count = 0

sql_website = 'ITmediaNews'

for TwoRoup in range(2):
    driver.get(URL_base + str(CurrentTime) + '.html')
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, Selector))
    )   
    
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    
    for el1 in soup.select('.colBoxBacknumber'):
        for el2 in el1.select('li'):
            sql_url = 'https:' + el2.find('a').get('href')
            sql_title = el2.find('a').getText() + " | ITMediaNews"
            
            cur.execute("select * from news_db where title=%s", (sql_title, ))
            
            if cur.rowcount != 0:
                count += 1
                print('skip')
                continue
            
            driver_firstdown.get(sql_url)
            soup_day = BeautifulSoup(driver_firstdown.page_source, features="html.parser")
            
            sql_day = soup_day.find(id="cmsDate").getText()
            sql_day = re.sub("\\D", "", sql_day) + '00'
            
            print('Title=', sql_title)
            print('url=', sql_url)
            print('datetime=', sql_day)
            print()
            
            cur.execute("insert into news_db(title, url, posttime, itnewssite) values(%s, %s, %s, %s)", (sql_title, sql_url, sql_day, sql_website))
            conn.commit()
            time.sleep(15)
            
    CurrentTime -= 1
    if CurrentTime % 100 == 0:
        CurrentTime -= 88

cur.execute("SET @i := 0")
cur.execute("UPDATE news_db SET sort_id = (@i := @i +1) ORDER BY posttime DESC");

driver.quit()
driver_firstdown.quit()
cur.close()
conn.commit()
conn.close()