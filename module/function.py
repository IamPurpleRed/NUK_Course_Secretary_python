import time
import json


# INFO: 建立使用者資料
def create_dict(bsMain, account):
    new_dict = {'1': {}, '2': {}, '3': {}, '4': {}, '5': {}}
    table = bsMain.find('table', {'id': 'myTable'})
    course_table = table.find_all('td', {'bgcolor': '#FFDCD7'})  # 粉紅色為本學期課程

    # NOTE: 表格有7欄，只有第2, 5欄是我們要的
    count = 0  # 範圍1~7，用來數現在爬到第幾欄，到7之後會歸零
    temp_course = str()
    temp_weekday = str()
    for td in course_table:
        count += 1
        if (count == 2):
            print('找到課程：', td.text)
            temp_course = td.text  # 取出課程名稱
        elif (count == 5):
            temp_weekday = td.text[1]  # 取出禮拜幾的那一個數字
        elif (count == 7):
            count = 0
            new_dict[temp_weekday][temp_course] = []
    print('\n課程爬取完成，正在建立檔案...')
    with open(f'./users/{account}.json', 'w+', encoding='utf-8') as obj:
        json.dump(new_dict, obj, indent=4, ensure_ascii=False)
    obj.close()
    print('已完成指定的工作！')
    time.sleep(2)  # 等待2秒
    print('==========')


# INFO: 初始化course_list
def init_course_list(user_dict, course_list):
    for i, j in zip(range(len(user_dict.keys())), user_dict.keys()):
        for k in user_dict[j].keys():
            course_list[i].append(k)


# INFO: 列出今明課程及備忘錄
def list_course(user_dict, wd):
    # NOTE: wd=0~6分別是星期一到星期日
    # 列出今天的課程
    if (wd >= 0) and (wd <= 4):
        print('\n這是今天要上的課以及備忘錄，記得做完蛤~')
        for i in user_dict[str(wd + 1)].keys():
            print(' ', i, sep='')
            for j in user_dict[str(wd + 1)][i]:
                print(' - ', j, sep='')
            if (len(user_dict[str(wd + 1)][i]) == 0):
                print('  <此課程沒有備忘錄>')
    else:
        print('\n今天放假喔~休息一下吧！')

    # 列出明天的課程
    if (wd >= 0) and (wd <= 3):
        print('\n明天要上的課以及備忘錄：')
        for i in user_dict[str(wd + 2)].keys():
            print(' ', i, sep='')
            for j in user_dict[str(wd + 2)][i]:
                print(' - ', j, sep='')
            if (len(user_dict[str(wd + 2)][i]) == 0):
                print('  <此課程沒有備忘錄>')

    elif (wd == 6):
        print('\n明天要上的課以及備忘錄：')
        for i in user_dict[str(wd - 5)].keys():
            print(' ', i, sep='')
            for j in user_dict[str(wd - 5)][i]:
                print(' - ', j, sep='')
            if (len(user_dict[str(wd - 5)][i]) == 0):
                print('  <此課程沒有備忘錄>')
    else:
        print('\n明天放假啦~去去去耍廢')

    time.sleep(2)  # 等待2秒
    print('==========')


# INFO: 選擇課程
def course_select(wd_list, course_list):
    while (1):
        row = int(input('\n請選擇星期(1~5，按0離開) '))
        if (row == 0):
            print('動作已中斷')
            time.sleep(2)  # 等待2秒
            print('==========')
            break
        elif (row >= 1) and (row <= 5):
            print('以下是', wd_list[row - 1], '的課程：', sep='')
            for i, j in zip(range(1, len(course_list[row - 1]) + 1), course_list[row - 1]):
                print(' ', i, ' ', j, sep='')
            print(' 0 回到上一步')
            while (1):
                col = int(input('\n請選擇課程編號 '))
                if (col == 0):
                    break
                elif (col >= 1) and (col <= len(course_list[row - 1])):
                    return [row - 1, col - 1]
                else:
                    print('輸入的數值無效，請再試一次！')
        else:
            print('輸入的數值無效，請再試一次！')


# INFO: 建立備忘錄
def create_note(course_list, index, user_dict, account):
    course = course_list[index[0]][index[1]]
    print('\n選定的課程為「', course, '」', sep='')
    new_note = input('請輸入新的備忘事項 ')
    while (1):
        print('\n即將於課程「', course, '」新增備忘事項：', new_note, sep='')
        confirm = int(input('你要確定餒？(0: 否/1: 是) '))
        if (confirm == 0):
            print('動作已中斷')
            time.sleep(2)  # 等待2秒
            print('==========')
            break
        elif (confirm == 1):
            user_dict[str(index[0] + 1)][course].append(new_note)
            with open(f'./users/{account}.json', 'w+', encoding='utf-8') as obj:
                json.dump(user_dict, obj, indent=4, ensure_ascii=False)
            obj.close()
            print('已完成指定的工作！')
            time.sleep(2)  # 等待2秒
            print('==========')
            break
        else:
            print('輸入的數值無效，請再試一次！')


# INFO: 刪除備忘錄
def delete_note(course_list, index, user_dict, account):
    back = False  # 為了要跳出外面的while迴圈而設立的布林值
    course = course_list[index[0]][index[1]]
    select_list = user_dict[str(index[0] + 1)][course]
    print('\n以下是「', course, '」的所有備忘事項：', sep='')
    for i, j in zip(range(1, len(select_list) + 1), select_list):
        print(' ', i, ' ', j, sep='')
    while (1):
        select = int(input('\n請選擇要刪除的備忘事項(按0離開) '))
        if (select == 0):
            print('動作已中斷')
            time.sleep(2)  # 等待2秒
            print('==========')
            break
        elif (select >= 1) and (select <= len(select_list)):
            while (1):
                print('\n即將於課程「', course, '」刪除備忘事項：', select_list[select - 1], sep='')
                confirm = int(input('刪除後就不能復原了，你要確定餒？(0: 否/1: 是) '))
                if (confirm == 0):
                    back = True  # 為了要跳出外面的while迴圈而設立的布林值
                    print('動作已中斷')
                    time.sleep(2)  # 等待2秒
                    print('==========')
                    break
                elif (confirm == 1):
                    back = True  # 為了要跳出外面的while迴圈而設立的布林值
                    user_dict[str(index[0] + 1)][course].remove(select_list[select - 1])
                    with open(f'./users/{account}.json', 'w+', encoding='utf-8') as obj:
                        json.dump(user_dict, obj, indent=4, ensure_ascii=False)
                    obj.close()
                    print('已完成指定的工作！')
                    time.sleep(2)  # 等待2秒
                    print('==========')
                    break
                else:
                    print('輸入的數值無效，請再試一次！')
        else:
            print('輸入的數值無效，請再試一次！')

        if (back):
            break


# INFO: 列出所有課程及備忘錄
def list_all(user_dict, wd_list, course_list):
    for i in user_dict.keys():
        print(wd_list[int(i) - 1], '：', sep='')
        for j in course_list[int(i) - 1]:
            print(' ', j, sep='')
            if (len(user_dict[i][j]) == 0):
                print('  <此課程沒有備忘錄>')
            for k in user_dict[i][j]:
                print(' - ', k, sep='')
        print('\n', end='')
    time.sleep(2)  # 等待2秒
    print('==========')
