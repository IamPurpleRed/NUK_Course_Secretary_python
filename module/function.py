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
            temp_course = td.text
        elif (count == 5):
            temp_weekday = td.text[1]
        elif (count == 7):
            count = 0
            new_dict[temp_weekday][temp_course] = []
    print('\n課程爬取完成，正在建立檔案...')
    with open(f'./users/{account}.json', 'w+', encoding='utf-8') as obj:
        json.dump(new_dict, obj, indent=4, ensure_ascii=False)
    obj.close()
    print('已完成指定的工作！\n==========')


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

    print('==========')


# INFO: 選擇課程
def course_select(wd_list, course_list):
    while (1):
        row = int(input('\n請選擇星期(1~5，按0離開) '))
        if (row == 0):
            print('動作已中斷\n==========')
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
        confirm = int(input('確認加入？(0: 否/1: 是) '))
        if (confirm == 0):
            print('動作已中斷\n==========')
            break
        elif (confirm == 1):
            user_dict[str(index[0] + 1)][course].append(new_note)
            with open(f'./users/{account}.json', 'w+', encoding='utf-8') as obj:
                json.dump(user_dict, obj, indent=4, ensure_ascii=False)
            obj.close()
            print('已完成指定的工作！\n==========')
            break
        else:
            print('輸入的數值無效，請再試一次！')
