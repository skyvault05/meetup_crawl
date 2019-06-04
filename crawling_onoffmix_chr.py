#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import os
import time

#os.chdir('/Users/hj/dev/meetup_crawl')
#os.getcwd()
print(os.getcwd() + '/enviroments/chromedriver')


# # 구글 드라이버 실행

# In[2]:


options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')
options.add_argument("disable-gpu")
# 혹은 options.add_argument("--disable-gpu")

driver = webdriver.Chrome(os.getcwd() + '/enviroments/chromedriver', chrome_options=options)
#driver = webdriver.Chrome(os.getcwd() + '/enviroments/chromedriver')


# In[3]:


driver.implicitly_wait(5)#웹 자원 로드를 위해 5초까지 기다림.
driver.set_script_timeout(5)


# In[4]:


#baseURL
base_URL = 'https://www.onoffmix.com' #온오프믹스
driver.get(base_URL+'/account/login') #get 로그인 페이지


# try:
#     element1 = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.CLASS_NAME, 'btn_submit'))
#     )
#     print(element1)
# except:
#     print(2)
#     pass

# In[5]:


#로그인
driver.find_element_by_class_name('email').send_keys('kimzombie@hotmail.com')
driver.find_element_by_class_name('password').send_keys('asdf65851242!@')

driver.find_element_by_class_name('btn_submit').click()


# #로그인 완료될때까지 기다리는 구문 필요 or css찾기
# try:
#     element2 = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, "header"))
#     )
#     print(element2)
# except:
#     print(2)
#     pass
#     
# #finally:

# In[6]:


time.sleep(1)
driver.get(base_URL+'/event/main/?c=085')
driver.get(base_URL+'/event/main/?c=085')


# # <로그인 완료>

# In[7]:


#menu_selector ='#header > div.header_bottom > div:nth-child(1) > div > div > button'
#driver.find_element_by_css_selector(menu_selector).click()

#driver.get(base_URL+'/event/main/?c=085')

#최근순으로 이동
recent_selector = '#content > div > section.event_main_area > div.title_bar > ul.sort_menu > li:nth-child(2) > a'
driver.find_element_by_css_selector(recent_selector).click()


# In[8]:


#baseURL
base_URL = 'https://www.onoffmix.com' #온오프믹스
#get 교육 페이지
'''list_URL = base_URL + '/event/main/?c=085' #모임 리스트
driver.get(list_URL)'''

#최근순으로 이동
recent_selector = '#content > div > section.event_main_area > div.title_bar > ul.sort_menu > li:nth-child(2) > a'
driver.find_element_by_css_selector(recent_selector).click()


# In[15]:


#페이지 추출, URL추출
target_URL = []
def getURL():
    move = ['3', '4', '5', '6'] # 각 selector 선택을 위한 변수
    for v in move:
        time.sleep(2)
        html = driver.page_source
        list_soup = BeautifulSoup(html, 'html.parser')
        list_selector = '#content > div > section.event_main_area > ul > li > article > a'
        selected = list_soup.select(list_selector)
        #print(1)
        #print(selected)
    
        #각 타겟 페이지 URL추출
        for i in selected:
            target_URL.append(i.get("href"))
            #print(target_URL)

        #다음페이지로 이동
        driver.find_element_by_css_selector('#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child('+v+')').click()
        #print(v)
    return target_URL


# In[10]:


#target_URL
#driver.set_script_timeout(10)
target_URL = getURL()
target_URL
#content > div > section.event_main_area > div.pagination_wrap > div > a:nth-child(6)


# In[11]:


#광고 페이지 제거 - /cs/를 포함하면 광고
cs = []
for n in target_URL:
    cs.append(n.find("/cs/"))
    
del target_URL[cs.index(0)]
target_URL


# In[12]:


#selector들
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


# In[13]:


#각 페이지 정보 크롤링
for i in target_URL:
    time.sleep(15)
    #타겟 URL지정해서 get
    driver.get(base_URL+i)

    #get 타겟 페이지
    target_html = driver.page_source
    target_soup = BeautifulSoup(target_html, 'html.parser')
    #target_soup

    date_selected = target_soup.select(date_selector)
    print(date_selected[0].text)

    place_selected = target_soup.select(place_selector)
    print(place_selected[0].text)

    limitation_selected = target_soup.select(limitation_selector)
    print(limitation_selected[0].text)

    name_selected = target_soup.select(name_selector)
    print(name_selected[0].text)

    email_selected2 = target_soup.select(email_selector)
    print(email_selected2[0].text)

    phone_selected = target_soup.select(phone_selector)
    print(phone_selected[0].text)


# In[ ]:





# In[ ]:





# In[14]:


driver.quit()


# In[ ]:




