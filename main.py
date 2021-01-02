import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  # 不要彈出webdriver視窗
import sys  # 結束程式
import getpass  # 使密碼在輸入時不被看見
import os  # 建立資料夾
import json
from bs4 import BeautifulSoup
import lxml
import time  # sleep函式

# 全域變數
first_time = False

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
        print('\n登入成功~\n==========')
        time.sleep(3)  # 等待3秒
        break  # 直到帳號密碼正確才能跳出while迴圈
    else:
        print('帳號或密碼輸入錯誤，請再試一次')

# INFO: 讀檔建檔
dirpath = './users'  # 存放使用者檔案的地方
if not os.path.isdir(dirpath):
    os.mkdir(dirpath)
try:
    with open(f'./users/{account}.json', 'r', encoding='utf-8') as obj:
        f = json.load(obj)
except:
    first_time = True  # 該使用者是第一次使用

# NOTE: 幫第一次使用的學生建立json檔
bsMain = BeautifulSoup(driver.page_source, 'lxml')  # BeautifulSoup抓課程總覽網頁
if first_time:
    print('看起來你是第一次使用，讓我們先幫你擷取課程資料...')
    time.sleep(3)
    new_dict = {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}}
    table = bsMain.find('table', {'id': 'myTable'})
    courseList = table.find_all('td', {'bgcolor': '#FFDCD7'})  # 粉紅色為本學期課程

    # NOTE: 表格有7欄，只有第2, 5欄是我們要的
    count = 0  # 範圍1~7，用來數現在爬到第幾欄，到7之後會歸零
    temp_course = str()
    temp_weekday = str()
    for td in courseList:
        count += 1
        if (count == 2):
            print('找到課程：', td.text)
            temp_course = td.text
        elif (count == 5):
            temp_weekday = td.text[1]
        elif (count == 7):
            count = 0
            new_dict[temp_weekday][temp_course] = []
    print('\n課程爬取完成，正在建立檔案...')
    with open(f'./users/{account}.json', 'w+', encoding='utf-8') as obj:
        json.dump(new_dict, obj, indent=4, ensure_ascii=False)
    print('已完成指定的工作！\n==========')

# INFO: 程式主選單
with open(f'./users/{account}.json', 'r', encoding='utf-8') as obj:
    userDict = json.load(obj)  # 讀檔
user_name = bsMain.find('table').find('font')  # 尋找學生姓名
print('哈囉！', user_name.getText(), '\n今天是', y, '年',
      m, '月', d, '日 ', wd_list[wd], sep='')

# NOTE: 根據禮拜幾來做出該有的互動，記得wd=0是星期一
# 列出今天的課程
if (wd == 0) or (wd == 1) or (wd == 2) or (wd == 3) or (wd == 4):
    print('這是今天要上的課，記得做完蛤~')
    for i in userDict[str(wd + 1)].keys():
        print(i)
else:
    print('今天放假喔~休息一下吧！')

# 列出明天的課程
if (wd == 0) or (wd == 1) or (wd == 2) or (wd == 3):
    print('\n明天要上的課')
    for i in userDict[str(wd + 2)].keys():
        print(i)
elif (wd == 6):
    print('\n明天要上的課')
    for i in userDict[str(wd - 5)].keys():
        print(i)
else:
    print('\n明天放假啦~去去去耍廢')
