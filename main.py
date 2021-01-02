import time  # sleep函式
import lxml
from bs4 import BeautifulSoup
import json
import os  # 建立資料夾
import getpass  # 使密碼在輸入時不被看見
import sys  # 結束程式
from selenium.webdriver.chrome.options import Options  # 不要彈出webdriver視窗
from selenium import webdriver
import datetime

#INFO: 匯入自訂模組
sys.path.append('./module/')  # 添加函式庫來源路徑
import function  # 自定義module

# INFO: 全域變數
first_time = False
user_dict = dict()
course_list = [[], [], [], [], []]

# INFO: 日期初始化
y = datetime.date.today().year
m = datetime.date.today().month
d = datetime.date.today().day
wd = datetime.datetime(y, m, d).weekday()
wd_list = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']

# INFO: webdriver初始化
print('正在開啟高大e平台...', end='')
options = Options()
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

# INFO: e平台登入畫面(selenium)
try:
    driver.get('http://elearning.nuk.edu.tw/default.php')
    login_btn = driver.find_element_by_class_name('login_stu')  # 尋找學生登入按鈕
    login_btn.click()
except:
    print('\n出事啦阿伯！打不開\n請檢查你的網路連線，或是等待校方伺服器修理好')
    sys.exit(0)
while (1):
    account = input('\n請輸入帳號 ')
    password = getpass.getpass('請輸入密碼 ')
    driver.switch_to.frame(driver.find_element_by_id('lhgfrm'))  # 進入iframe框架
    account_text = driver.find_element_by_id('stuid')  # 尋找帳號輸入欄
    account_text.send_keys(account)
    password_text = driver.find_element_by_id('stupw')  # 尋找密碼輸入欄
    password_text.send_keys(password)
    driver.switch_to.default_content()  # 跳出iframe
    enter_btn = driver.find_element_by_id('close')
    enter_btn.click()
    if (driver.current_url == 'http://elearning.nuk.edu.tw/m_student/m_stu_index.php'):
        bsMain = BeautifulSoup(driver.page_source, 'lxml')  # BeautifulSoup抓課程總覽網頁
        print('\n登入成功~\n==========')
        time.sleep(2)  # 等待2秒
        break  # 直到帳號密碼正確才能跳出while迴圈
    else:
        print('帳號或密碼輸入錯誤，請再試一次')

# INFO: 讀檔建檔
dirpath = './users'  # 存放使用者檔案的地方
if not os.path.isdir(dirpath):
    os.mkdir(dirpath)
try:
    with open(f'./users/{account}.json', 'r', encoding='utf-8') as obj:
        user_dict = json.load(obj)  # 讀檔並轉成python字典型別，用user_dict接住
    obj.close()
except:
    first_time = True  # 該使用者是第一次使用

# NOTE: 幫第一次使用的學生建立json檔
if first_time:
    print('看起來你是第一次使用，讓我們先幫你擷取課程資料...')
    time.sleep(2)  # 等待2秒
    function.create_dict(bsMain, account)  # function.py
    with open(f'./users/{account}.json', 'r', encoding='utf-8') as obj:
        user_dict = json.load(obj)  # 讀檔並轉成python字典型別，用user_dict接住
    obj.close()  # 關檔


# INFO: 程式主選單
user_name = bsMain.find('table').find('font')  # 尋找學生姓名
print('哈囉！', user_name.getText(), '\n今天是', y, '年', m, '月', d, '日 ', wd_list[wd], sep='')  # 印出學生姓名跟今天日期
function.init_course_list(user_dict, course_list)  # function.py
function.list_course(user_dict, wd)  # function.py

# NOTE: 選單選項
while (1):
    print('主選單：\n 1 新增備忘錄\n 2 刪除備忘錄\n 3 列出今明兩天課程及備忘錄\n 4 重新建立使用者課程資料\n 5 列出所有課程及備忘清單\n 0 離開\n')
    choose = int(input('請選擇項目 '))
    if (choose == 0):
        print('掰波！')
        sys.exit(0)
    elif (choose == 1):
        index = function.course_select(wd_list, course_list)  # function.py
        if (index != None):
            function.create_note(course_list, index, user_dict, account)
    elif (choose == 2):
        index = function.course_select(wd_list, course_list)  # function.py
        if (index != None):
            function.delete_note(course_list, index, user_dict, account)
    elif (choose == 3):
        function.list_course(user_dict, wd)  # function.py
    elif (choose == 4):
        while (1):
            confirm = int(input('警告：重新爬取課程將會取代原本的檔案，之前建立的備忘錄也會一併消失，你要確定餒？(0: 否/1: 是) '))
            if (confirm == 0):
                print('動作已中斷')
                time.sleep(2)  # 等待2秒
                print('==========')
                break
            elif (confirm == 1):
                function.create_dict(bsMain, account)  # function.py
                with open(f'./users/{account}.json', 'r', encoding='utf-8') as obj:
                    user_dict = json.load(obj)  # 讀檔並轉成python字典型別，用user_dict接住
                course_list = [[], [], [], [], []]
                function.init_course_list(user_dict, course_list)
                break
            else:
                print('輸入的數值無效 請再試一次！\n')
    elif (choose == 5):
        function.list_all(user_dict, wd_list, course_list)
    else:
        print('輸入的數值無效 請再試一次！\n==========')
