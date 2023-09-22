from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import subprocess
import time

url = "http://ice.esosc.co.kr/"
id ='아이디'
pw='비밀번호'

options=Options()
options.add_experimental_option("detach",True)
options.add_argument("incognito")
options.add_argument("--mute-audio")
service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service, options=options)
driver.get(url)

#frame으로 들어가기
main_board=driver.find_element(By.XPATH,'/html/frameset/frame[2]')
driver.switch_to.frame(main_board)
#로그인 하기
driver.find_element(By.NAME,'user_id').send_keys(id)
driver.find_element(By.NAME,'pwd').send_keys(pw)
driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/form/fieldset/div[4]/div[1]/a').click()


#교육 정보 페이지 들어가기
driver.find_element(By.XPATH,'/html/body/main/section[2]/div/ul/li[1]').click()
driver.find_element(By.CSS_SELECTOR,'#container > section.sub-wrap > div > table > tbody > tr:last-child > td:nth-child(7) > button.lecture-list-btn1').click()
time.sleep(3)
driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/span[1]').click()

# 교육 정보 페이지에서 강의실 들어가기
driver.switch_to.window( driver.window_handles[1])
driver.find_element(By.XPATH,'/html/body/main/section/div[1]/article/a').click()
#######################################

#lecture_count : 강의의 수
lecture_count=int(driver.find_element(By.CSS_SELECTOR,'#student-container > section > div.board-list-wrap > table > tbody > tr:last-child > td.d-num').text)

#cur : 현재 재생되는 강의의 number
for cur in range(1,lecture_count+1):
    #진도율 갱신을 위한 화면 클릭
    driver.find_element(By.ID,'student-container').click()

    #진도율이 100%면 continue
    cur_progress=driver.find_element(By.CSS_SELECTOR,f'#student-container > section > div.board-list-wrap > table > tbody > tr:nth-child({cur}) > td.td-view')
    if cur_progress == '100%': continue

    driver.find_element(By.CSS_SELECTOR,f'#student-container > section > div.board-list-wrap > table > tbody > tr:nth-child({cur}) > td.td-file > a').click()
    driver.switch_to.window( driver.window_handles[2])
    go_frame=driver.find_element(By.XPATH,'/html/frameset/frame[2]')
    driver.switch_to.frame(go_frame)
    
    #한 강의 다 듣기
    while True:
        driver.find_element(By.TAG_NAME,'html').click()
        try:
            watch_time=driver.find_element(By.ID,'divCurrentTime').text
            if watch_time:
                cur,fin=watch_time.split(sep=' / ')
                time.sleep(int(fin)+1)
                driver.find_element(By.TAG_NAME,'html').click()
                driver.find_element(By.ID,'btn_nextPage').click()
        except:
            while True: pass
        
#################################################################