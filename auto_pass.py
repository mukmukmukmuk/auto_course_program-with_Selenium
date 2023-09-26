from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
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

def next_page_button():
    global driver
    global root
    global quiz_page
    quiz_page.destroy()
    driver.find_element(By.ID,'btn_nextPage').click()
    
def quiz():
    global driver
    global root
    global quiz_page
    quiz_page=Toplevel(root)
    quiz_page.title('퀴즈!')
    quiz_text=Label(quiz_page, text = "퀴즈를 모두 풀고, 확인 버튼을 눌러주세요")
    quiz_text.grid(row=0,column=0)
    quiz_complete=Button(quiz_page,text='확인',command=next_page_button)
    quiz_complete.grid(row=2,column=1,padx=20,pady=5)
    
    #result = tkinter.messagebox.showinfo("퀴즈!", "퀴즈를 모두 풀고, 확인 버튼을 눌러주세요")
    #if result:
    #    driver.find_element(By.ID,'btn_nextPage').click()
    #    print("사용자가 확인을 눌렀습니다.")
        

def learn_class():
    global driver
    time_error=time.sleep(0)
    #chapter_count : 챕터의 수
    chapter_count=int(driver.find_element(By.CSS_SELECTOR,'#student-container > section > div.board-list-wrap > table > tbody > tr:last-child > td.d-num').text)
    #cur : 현재 재생되는 챕터의 number
    cur=1
    while chapter_count>=cur:
        #진도율 갱신을 위한 화면 클릭
        driver.find_element(By.ID,'student-container').click()
        #진도율이 100%면 continue
        cur_progress=driver.find_element(By.CSS_SELECTOR,f'#student-container > section > div.board-list-wrap > table > tbody > tr:nth-child({cur}) > td.td-view').text
        if cur_progress == '100%': 
            cur+=1
            continue
        driver.find_element(By.CSS_SELECTOR,f'#student-container > section > div.board-list-wrap > table > tbody > tr:nth-child({cur}) > td.td-file > a').click()
        try:
            #예상치 못한 강의 창 꺼짐에 대한 예외처리
            alert=Alert(driver)
            alert.accept()
            cur-=1
            continue
        except: 
            driver.switch_to.window(driver.window_handles[2])
            driver.switch_to.frame(driver.find_element(By.XPATH,'/html/frameset/frame[2]'))
        #한 챕터의 모든 강의 다 듣기################################
        # 처음 들어갈 때부터 퀴즈가 나올 수 있으므로 예외처리###############################
        try:
            driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[2]/div[3]/span').text[2:-2].split(sep=' / ')
        except Exception as ec:
            quiz()
        ###############################################################################

        driver.find_element(By.TAG_NAME,'html').click()
        # 강의가 뜨기까지 로딩 시간이 존재하므로, 이에 대한 예외처리를 해줌
        WebDriverWait(driver,10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div/div[2]/div[2]/div[2]/div[3]/span')))

        cur_count,fin_count=map(int,driver.find_element(By.XPATH,'/html/body/div/div[2]/div[2]/div[2]/div[3]/span').text[2:-2].split(sep=' / '))
        total_continue=fin_count-cur_count+1
        for _ in range(total_continue):
            try:
                #시간을 확인하기 전에 현재 보고 있는 window가 강의 창이 맞는지 다시 점검
                driver.switch_to.window(driver.window_handles[2])
                driver.switch_to.frame(driver.find_element(By.XPATH,'/html/frameset/frame[2]'))

                driver.find_element(By.TAG_NAME,'html').click()
                watch_time=driver.find_element(By.ID,'divCurrentTime').text
                if watch_time:
                    cur_time,fin_time=map(int,watch_time.split(sep=' / '))
                    time.sleep(fin_time+2)
                    driver.find_element(By.TAG_NAME,'html').click()
                    WebDriverWait(driver,3).until(EC.visibility_of_element_located((By.ID,'btn_nextPage')))
                    #driver.implicitly_wait(3)
                    #time.sleep(0.5)
                    driver.find_element(By.ID,'btn_nextPage').click()
                
                
            except Exception as ec:
                #퀴즈가 나왔을 때 예외처리
                print(ec)
                quiz()
                continue
                continue
        #한 챕터의 강의를 모두 시청했을 경우, 현재 켜져있는 강의 창을 닫고 window를 전환하며 반복문 종료
        #시간을 확인하기 전에 현재 보고 있는 window가 강의 창이 맞는지 다시 점검
        
        #창이 있다면 끄고 아니면 그냥 두기
        driver.switch_to.window(driver.window_handles[2])
        driver.close()
        driver.switch_to.window( driver.window_handles[1])
        cur+=1
    driver.quit()

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


    