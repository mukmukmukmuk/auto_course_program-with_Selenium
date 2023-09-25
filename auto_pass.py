from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
import time
from tkinter import *
import tkinter.messagebox

# Url 및 driver option
url = "http://ice.esosc.co.kr/"
options=Options()
options.add_experimental_option("detach",True)
options.add_argument("incognito")
options.add_argument("--mute-audio")
service=Service(ChromeDriverManager().install())



def login():
    global driver
    global id
    global pw
    driver=webdriver.Chrome(service=service, options=options)
    driver.get(url)
    #frame으로 들어가기
    main_board=driver.find_element(By.XPATH,'/html/frameset/frame[2]')
    driver.switch_to.frame(main_board)
    #로그인 하기
    id=id_input.get()
    pw=pw_input.get()
    driver.find_element(By.NAME,'user_id').send_keys(id)
    driver.find_element(By.NAME,'pwd').send_keys(pw)
    driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/form/fieldset/div[4]/div[1]/a').click()

# 교육 정보 페이지, 강의실 들어가기
def go_chapter():
    global driver
    #교육 정보 페이지 들어가기
    driver.find_element(By.XPATH,'/html/body/main/section[2]/div/ul/li[1]').click()
    driver.find_element(By.CSS_SELECTOR,'#container > section.sub-wrap > div > table > tbody > tr:last-child > td:nth-child(7) > button.lecture-list-btn1').click()
    driver.implicitly_wait(3)
    driver.find_element(By.XPATH,'/html/body/div[2]/div[2]/div/div[2]/span[1]').click()
    # 교육 정보 페이지에서 강의실 들어가기
    driver.switch_to.window( driver.window_handles[1])
    driver.find_element(By.XPATH,'/html/body/main/section/div[1]/article/a').click()

def quiz():
    global driver
    result = tkinter.messagebox.showinfo("퀴즈!", "퀴즈를 모두 풀고, 확인 버튼을 눌러주세요")
    if result:
        driver.find_element(By.ID,'btn_nextPage').click()
        print("사용자가 확인을 눌렀습니다.")
        

def learn_class():
    global driver
    #chapter_count : 챕터의 수
    chapter_count=int(driver.find_element(By.CSS_SELECTOR,'#student-container > section > div.board-list-wrap > table > tbody > tr:last-child > td.d-num').text)

    #cur : 현재 재생되는 챕터의 number
    for cur in range(1,chapter_count+1):
        #진도율 갱신을 위한 화면 클릭
        driver.find_element(By.ID,'student-container').click()
        #진도율이 100%면 continue
        cur_progress=driver.find_element(By.CSS_SELECTOR,f'#student-container > section > div.board-list-wrap > table > tbody > tr:nth-child({cur}) > td.td-view').text
        if cur_progress == '100%': continue
        driver.find_element(By.CSS_SELECTOR,f'#student-container > section > div.board-list-wrap > table > tbody > tr:nth-child({cur}) > td.td-file > a').click()
        driver.switch_to.window(driver.window_handles[2])
        driver.switch_to.frame(driver.find_element(By.XPATH,'/html/frameset/frame[2]'))
        
        #한 챕터의 모든 강의 다 듣기################################

        # 처음 들어갈 때부터 퀴즈가 나올 수 있으므로 예외처리###############################
        try:
            driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[2]/div[3]/span').text[2:-2].split(sep=' / ')
        except:
            quiz()
        ###############################################################################

        driver.find_element(By.TAG_NAME,'html').click()
        cur_count,fin_count=map(int,driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[2]/div[3]/span').text[2:-2].split(sep=' / '))
        for _ in range(fin_count-cur_count+1):
            try:
                #시간을 확인하기 전에 현재 보고 있는 window가 강의 창이 맞는지 다시 점검
                driver.switch_to.window(driver.window_handles[2])
                driver.switch_to.frame(driver.find_element(By.XPATH,'/html/frameset/frame[2]'))

                driver.find_element(By.TAG_NAME,'html').click()
                watch_time=driver.find_element(By.ID,'divCurrentTime').text
                if watch_time:
                    cur_time,fin_time=map(int,watch_time.split(sep=' / '))
                    time.sleep(fin_time+3)
                    driver.find_element(By.TAG_NAME,'html').click()
                    driver.find_element(By.ID,'btn_nextPage').click()
            except Exception as ec:
                #퀴즈가 나왔을 때 예외처리
                print(ec)
                quiz()
        #한 챕터의 강의를 모두 시청했을 경우, 현재 켜져있는 강의 창을 닫고 window를 전환하며 반복문 종료
        #시간을 확인하기 전에 현재 보고 있는 window가 강의 창이 맞는지 다시 점검
        
        #창이 있다면 끄고 아니면 걍 go 하면 됨
        try:
            driver.switch_to.window(driver.window_handles[2])
            driver.close()
        except:  pass
        driver.switch_to.window( driver.window_handles[1])
        driver.find_element(By.XPATH,'/html/body/main/section/div[1]/article/a').click()


#자동강의 수강 동작
def all_task():
    login()
    go_chapter()
    learn_class()


#############################################################################################################
##############                                GUI                                   #########################
#############################################################################################################
root = Tk()
root.title('산업안전컨설팅')

id_label=Label(root, text = "ID")
id_label.grid(row=0,column=0)
id_input=Entry(root, width=30)
id_input.grid(row=0,column=1,padx=20,pady=5)

pw_label=Label(root,text="비밀번호")
pw_label.grid(row=1,column=0)
pw_input=Entry(root,width=30)
pw_input.grid(row=1,column=1,padx=20,pady=5)

submit_btn=Button(root,text='입력',command=all_task)
submit_btn.grid(row=2,column=1,padx=20,pady=5)

mainloop()
#############################################################################################################
##############                                GUI                                   #########################
#############################################################################################################


    
