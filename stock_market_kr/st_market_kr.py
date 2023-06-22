import sys
sys.path.append('c:\\programdata\\anaconda3\\envs\\ai\\lib\\site-packages')

import os
from datetime import datetime
now = datetime.now()
now = now.strftime("%Y_%m_%d_%H_%M_%S.%f")

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Chrome()
browser.maximize_window()

# 1. 페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?sosok=0&page='
browser.get(url)

# 2. 기본 조회 항목 해제
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected(): # 체크되어 있으면
        checkbox.click()   # 클릭해서 해제
        
# 3. 조회 항목 설정
items_to_select = ['영업이익', '자산총계', '매출액']
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..') # 부모 element 찾기
    label = parent.find_element(By.TAG_NAME, 'label')
    # print(label.text) # test 용
    if label.text in items_to_select: # 선택한 항목과 일치하면
        checkbox.click() # 체크하기!
        
# 4. 적용하기 버튼 클릭 (조회)
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()

for idx in range(1, 40): # 1 이상 40 미만 페이지에 반복 수행
    # 사전 작업 - 페이지 이동
    browser.get(url + str(idx))
    
    # 5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all', inplace=True)
    df.dropna(axis='columns', how='all', inplace=True)

    if len(df) == 0:
        break
    
    # 6. 파일 저장
    file_name = 'sise_' + str(now) + '.csv'
    if os.path.exists(file_name): # 파일이 있으면 헤더는 제외 (column명은 1번만 저장)
        df.to_csv(file_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else: # 파일이 없으면 헤더랑 같이 저장
        df.to_csv(file_name, encoding='utf-8-sig', index=False)
    print(f'{idx} 페이지 저장 완료')
    
browser.quit() # 브라우저 종료
print("완료")