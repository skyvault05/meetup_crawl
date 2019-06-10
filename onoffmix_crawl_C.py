
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
#chrome driver 실행
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--profile-directory=Default')
options.add_argument('--incognito')
options.add_argument('--disable-plugins-discovery')
options.add_argument('--start-maximized')
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
driver = webdriver.Chrome('./enviroments/chromedriver', chrome_options=options)


#%%
#페이지 로드 대기시간 설정
driver.implicitly_wait(5)#웹 자원 로드를 위해 5초까지 기다림.
driver.set_script_timeout(5)


#%%
#baseURL
base_URL = 'https://www.onoffmix.com' #온오프믹스
driver.get(base_URL+'/account/login') #get 로그인 페이지

#%%
#로그인
driver.find_element_by_class_name('email').send_keys('kimzombie@hotmail.com')
driver.find_element_by_class_name('password').send_keys('asdf65851242!@')

driver.find_element_by_class_name('btn_submit').click()

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "user_name")))
except:
    print('error')

#%%
#time.sleep(1)

#교육 페이지로 이동
driver.get(base_URL+'/event/main/?c=085')

#최근순으로 이동
recent_selector = '#content > div > section.event_main_area > div.title_bar > ul.sort_menu > li:nth-child(2) > a'
driver.find_element_by_css_selector(recent_selector).click()


#%% [markdown]
# #페이지이동
# #driver.find.element_by_ccs_selector()
# 
# #content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(3)
# #content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(4)
# 
# '#content > div > section.event_main_area > div.pagination_wrap > div > a.btn_prev'
# '#content > div > section.event_main_area > div.pagination_wrap > div > a.page_move.active.disabled'
# '#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(3)'
# '#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(4)'
# '#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(5)'
# '#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(6)'
# '#content > div > section.event_main_area > div.pagination_wrap > div > a.btn_next'

#%%
#각 교육 상세 페이지 URL 추출 함수 지정
def getURL():
    temp_URL = []
    move = ['3', '4', '5', '6'] # 각 selector 선택을 위한 변수
    for v in move:
        #time.sleep(1)

        try:
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child('+v+')')))
            #print(v)
        except:
            print('error')

        html = driver.page_source
        list_soup = BeautifulSoup(html, 'html.parser')
        list_selector = '#content > div > section.event_main_area > ul > li > article > a'
        selected = list_soup.select(list_selector)
        #print(1)
        #print(selected)
        #print(list_soup.select(list_selector))
    
        #각 타겟 페이지 URL추출
        for i in selected:
            temp_URL.append(i.get("href"))
            #print(i.get("href"))

        
        
        #다음페이지로 이동
        driver.find_element_by_css_selector('#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child('+v+')').click()
        #print(v)
    return temp_URL


#%%
#각 교육 상세 페이지 URL 추출
target_URL = []
epoch = 2
for i in range(epoch):
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#content > div > section.event_main_area > div.pagination_wrap > div > a.btn_next')))
    except:
        print('error')
    target_URL = target_URL + getURL()
    
    driver.find_element_by_css_selector('#content > div > section.event_main_area > div.pagination_wrap > div > a.btn_next').click()

#len(target_URL)


#%%
#광고 페이지 제거 - /cs/를 포함하면 광고
cs = []
for n in target_URL:
    cs.append(n.find("/cs/"))

    
del target_URL[cs.index(0)]
target_URL


#%%
#selector들
#제목
title_selector = '#content > div.content_wrapping.max_width_area > section.event_summary > div.right_area > h3'
#모임기간
date_selector = "#content > div.content_wrapping.max_width_area > section.event_summary > div.right_area > ul > li:nth-child(1) > p"
#모임장소
place_selector = "#content > div.content_wrapping.max_width_area > section.event_summary > div.right_area > ul > li:nth-child(2) > p > span"
#모집정원
limitation_selector = '#content > div.content_wrapping.max_width_area > section.event_summary > div.right_area > ul > li:nth-child(3) > p > span.total > span'
#강연자 이름
name_selector ="#hostInfo > li.host_name > a"
#강연자 email
email_selector = "#hostInfo > li.host_mail"
#강연자 전화번호
phone_selector ="#hostInfo > li.host_phone"


#%%
#csv파일이 존재하는지 확인하고 없으면 폴더 및 csv파일 생성
if os.path.exists(os.getcwd() + "/data/data.csv"):
    old_data = pd.read_csv(os.getcwd() + '/data/data.csv', index_col=0)
else:
    os.mkdir(os.getcwd() + '/data/')
    df = pd.DataFrame(columns=['이름', '연락처', '이메일', '제목', '장소', '시간', '인원제한', 'URL'])
    df.to_csv(os.getcwd() + '/data/data.csv')
    old_data = pd.read_csv(os.getcwd() + '/data/data.csv', index_col=0)


    

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
    #time.sleep(11)
    

    #soup 타겟 페이지
    target_html = driver.page_source
    target_soup = BeautifulSoup(target_html, 'html.parser')
    #target_soup

    #soup에서 요소들 추출해서 list로 저장
    url_list.append(base_URL+i)

    title_selected = target_soup.select(title_selector)
    if 0 < len(title_selected) :
        title_list.append(title_selected[0].text[21:-16])
        print(title_selected[0].text[21:-16])
    else:
        title_list.append('no_title')
        print('no_title')


    date_selected = target_soup.select(date_selector)
    if 0 < len(date_selected):
        date_list.append(date_selected[0].text)
        print(date_selected[0].text)
    else:
        date_list.append('no_date')
        print('no_date')

    place_selected = target_soup.select(place_selector)
    if 0 < len(place_selected):
        place_list.append(place_selected[0].text)
        print(place_selected[0].text)
    else:
        place_list.append('no_place')
        print('no_place')

    limitation_selected = target_soup.select(limitation_selector)
    if 0 < len(limitation_selected):
        limitation_list.append(limitation_selected[0].text)
        print(limitation_selected[0].text)
    else: 
       limitation_list.append('no_limitation')
       print('no_limitation')

    name_selected = target_soup.select(name_selector)
    if 0 < len(name_selected):
        name_list.append(name_selected[0].text)
        print(name_selected[0].text)
    else:
        name_list.append('no_name')
        print('no_name')

    email_selected = target_soup.select(email_selector)
    if 0 < len(email_selected):
        email_list.append(email_selected[0].text)
        print(email_selected[0].text)
    else:
        email_list.append('no_email')
        print('no_email')

    phone_selected = target_soup.select(phone_selector)
    if 0 < len(phone_selected):
        phone_list.append(phone_selected[0].text)
        print(phone_selected[0].text)
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
result_data.to_csv(os.getcwd() + '/data/data.csv')

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