
#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import os
import time

#os.chdir('/Users/hj/dev/meetup_crawl')
#os.getcwd()
print(os.getcwd())

#%%
#phantomJS 실행
driver = webdriver.PhantomJS('/Users/hj/dev/meetup_crawl/enviroments/phantomjs-2.1.1-macosx/bin/phantomjs')

#코드 확인용 크롬 드라이버
#driver = webdriver.Chrome('./enviroments/chromedriver')

#%%
#페이지 로드 대기시간 설정
driver.implicitly_wait(5)#웹 자원 로드를 위해 5초까지 기다림.
driver.set_script_timeout(5)


#%%
#baseURL
base_URL = 'https://event-us.kr' #온오프믹스

#교육 페이지로 이동
driver.get('https://event-us.kr/Search?search=&category=%EC%A7%80%EC%8B%9D/%EA%B5%90%EC%9C%A1&area=All&cost=All')


#%% [markdown]
#상세 페이지 추가 로드 css selector
#app > div.container.main-container > div > div.col.s12.m-t-b-30 > div > div

#상세 페이지 추가 로드 했을 시 마지막 항목 (처음12개, 6개씩 추가)
#app > div.container.main-container > div > div:nth-child(12) > a


#%%
#각 교육 상세 페이지 URL 추출 함수 지정
temp_URL = []
def getURL(epoch):   
    for v in range(epoch):
        driver.find_element_by_css_selector('#app > div.container.main-container > div > div.col.s12.m-t-b-30 > div > div > img').click()
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, '#app > div.container.main-container > div > div:nth-child('+str(12+6*(v+1))+') > a')))
            print(v)
        except:
            print('error')
            print(v)

    #페이지를 soup로 만듦
    html = driver.page_source
    list_soup = BeautifulSoup(html, 'html.parser')
    list_selector = '#app > div.container.main-container > div > div > a'
    selected = list_soup.select(list_selector)
        #print(1)
        #print(selected)
        #print(list_soup.select(list_selector))
    
        #각 타겟 페이지 URL추출
    for i in selected:
        temp_URL.append(i.get("href"))
        print(i.get("href"))

    return temp_URL
#%%
#각 상세 페이지
epoch = 4
target_URL = getURL(epoch)
print(target_URL)
print(len(target_URL))
print(str(12+6*(epoch)))


#%%
#selector들
#제목
title_selector = 'body > div.leftside-info.white > div.leftside-info-contents > div.blog > div > div.card-content.leftside-info-title > h5'
#모임기간
date_selector = 'body > div.leftside-info.white > div.leftside-info-contents > div.leftside-info-title > div:nth-child(3) > div > div.col.push-s1.s8.colstyle > span'
#모임장소
place_selector = 'body > div.leftside-info.white > div.leftside-info-contents > div.leftside-info-title > div:nth-child(5) > div > div.col.push-s1.s8.colstyle > span > a'
#모집정원
limitation_selector = 'body > div.leftside-info.white > div.leftside-info-contents > div.leftside-info-title > div:nth-child(8) > div.fontstyle > span:nth-child(2)'
#강연자 이름
name_selector = 'body > div.leftside-info.white > div.m-t5 > div:nth-child(2) > div:nth-child(1) > span'
#강연자 email
email_selector = 'body > div.leftside-info.white > div.m-t5 > div:nth-child(2) > div:nth-child(2) > span > a'
#강연자 전화번호
phone_selector = 'body > div.leftside-info.white > div.m-t5 > div:nth-child(2) > div:nth-child(3) > span > a'


#%%
#csv파일이 존재하는지 확인하고 없으면 폴더 및 csv파일 생성
if os.path.exists('./data/eventus_data.csv'):
    old_data = pd.read_csv('./data/eventus_data.csv', index_col=0)
else:
    if not os.path.exists('./data'):
        os.mkdir('./data/')
    
    df = pd.DataFrame(columns=['이름', '연락처', '이메일', '제목', '장소', '시간', '인원제한', 'URL'])
    df.to_csv('./data/eventus_data.csv')
    old_data = pd.read_csv('./data/eventus_data.csv', index_col=0)


    

#%%
name_list = []
limitation_list = []
place_list = []
date_list = []
title_list = []
email_list = []
phone_list = []
url_list = []
for i in target_URL:
    
    #타겟 URL지정해서 get
    driver.get(base_URL+i)

    #soup 타겟 페이지
    target_html = driver.page_source
    target_soup = BeautifulSoup(target_html, 'html.parser')
    #target_soup

    #soup에서 요소들 추출해서 list로 저장
    url_list.append(base_URL+i)

    title_selected = target_soup.select(title_selector)
    if 0 < len(title_selected) :
        title_list.append(title_selected[0].text[33:-29])
        print(title_selected[0].text[33:-29])
    else:
        title_list.append('no_title')
        print('no_title')


    date_selected = target_soup.select(date_selector)
    if 0 < len(date_selected):
        date_list.append(date_selected[0].text[41:-37])
        print(date_selected[0].text[41:-37])
    else:
        date_list.append('no_date')
        print('no_date')

    place_selected = target_soup.select(place_selector)
    if 0 < len(place_selected):
        place_list.append(place_selected[0].text[:-1])
        print(place_selected[0].text[:-1])
    else:
        place_list.append('no_place')
        print('no_place')

    limitation_selected = target_soup.select(limitation_selector)
    if 0 < len(limitation_selected):
        limitation_list.append(limitation_selected[0].text[1:])
        print(limitation_selected[0].text[1:])
    else: 
       limitation_list.append('no_limitation')
       print('no_limitation')

    name_selected = target_soup.select(name_selector)
    if 0 < len(name_selected):
        name_list.append(name_selected[0].text[4:])
        print(name_selected[0].text[4:])
    else:
        name_list.append('no_name')
        print('no_name')

    email_selected = target_soup.select(email_selector)
    if 0 < len(email_selected):
        email_list.append(email_selected[0].text[1:])
        print(email_selected[0].text[1:])
    else:
        email_list.append('no_email')
        print('no_email')

    phone_selected = target_soup.select(phone_selector)
    if 0 < len(phone_selected):
        phone_list.append(phone_selected[0].text[1:])
        print(phone_selected[0].text[1:])
    else:
        phone_list.append('no_phone')
        print('no_phone')



#%%
#데이터 추가
new_data = pd.DataFrame({'이름':name_list, '연락처':phone_list, '이메일':email_list, '제목':title_list, '장소':place_list, '시간':date_list, '인원제한':limitation_list, 'URL':url_list})
result_data = old_data.append(new_data, ignore_index=True)

#중복항목 제거
result_data.drop_duplicates(subset='URL', inplace=True)

#파일로 내보내기
result_data.to_csv(os.getcwd() + '/data/eventus_data.csv')
print('eventus_data.csv')
#%%
driver.quit()




#%%
print('name:' , len(name_list))
print('phone:', len(phone_list))
print('email:', len(email_list))
print('title:', len(title_list))
print('place:', len(place_list))
print('date:', len(date_list))
print('limit:', len(limitation_list))
print('URL:', len(url_list))