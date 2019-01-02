from selenium import webdriver
from time import sleep
from datetime import datetime, timedelta
import poplib
from email.parser import Parser
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import pandas as pd
from pandas import DataFrame

account = ''
password = ''
mail = ''
mailpwd = ''


data = pd.read_excel('圈米资料.xlsx')
num = data.iloc[:,0].size
i = data['状态'].count()+1

def get_parsed_msg():
    # 邮箱个人信息
    useraccount = mail
    password = mailpwd
    # 邮件服务器地址
    pop3_server = 'pop.163.com'
    # 开始连接到服务器
    server = poplib.POP3(pop3_server)
    # 开始进行身份验证
    try:
        server.user(useraccount)
        server.pass_(password)
    except Exception:
        print('邮箱密码错误，或者未开启POP3')
        return '','','',''
    # 使用list()返回所有邮件的编号，默认为字节类型的串
    resp, mails, octets = server.list()
    # 下面单纯获取最新的一封邮件
    total_mail_numbers = len(mails)
    # 默认下标越大，邮件越新，所以total_mail_numbers代表最新的那封邮件
    response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
    msg_content = b'\r\n'.join(mail_message_lines).decode('gbk')
    # 邮件原始数据没法正常浏览，因此需要相应的进行解码操作
    msg = Parser().parsestr(text=msg_content)
    #获取发件人
    fromstr = msg.get('From')
    # 获取主题信息，也就是标题内容
    subject = msg.get('Subject')
    # 关闭与服务器的连接，释放资源
    server.close()
    return msg,fromstr,subject,total_mail_numbers

def transfer():
    oldlenmail = get_parsed_msg()[3]
    if oldlenmail == '':
        data.loc[i - 1, '报错内容'] = '邮箱密码错误，或者未开启POP3'
        DataFrame(data).to_excel('圈米资料.xlsx', index=False, header=True)
        return
    driver.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/div[2]/div/i').click()
    while driver.find_element_by_class_name('token-message').text != 'Token Created Succesfully':
        sleep(1)
    else:
        print('发送验证码成功')
        outnum = 0

        while get_parsed_msg()[3] == oldlenmail:
            sleep(10)
            outnum += 10
            if outnum > 100:
                print('100秒内没有找到验证码，请稍后再试')
                content = 0
                break
        else:
            msg, fromstr, subject, lenmail = get_parsed_msg()
            if fromstr == 'Airbit Club <no-reply@airbitclub.com>' and subject == 'Request token':
                content = str(msg).split('*The Token your requested for Transfer is* ')[1][:6]
                print(content)
            else:
                print('邮箱收到新邮件打断了邮件查找')

    return content

def searchWallet():
    while 'btn btn-grey margin-bottom' not in driver.page_source:
        sleep(1)
    else:
        try:
            rewards = WebDriverWait(driver, 20, 2).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div[2]/div[3]/div[2]'))).text
        except Exception:

            print('可能因网络原因未查到静态钱包的金额')
        try:
            commissions = WebDriverWait(driver, 20, 1).until(
                EC.presence_of_element_located((By.XPATH,
                                                '//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div[2]/div[2]/div[2]'))).text
        except Exception:
            print('可能因网络原因未查到动态钱包的金额')

    commissions = commissions.split('$')[1]
    rewards = rewards.split('$')[1]
    try:
        commissions = float(commissions)
    except Exception:
        c1 = commissions.split(',')[0]
        c2 = commissions.split(',')[1]
        commissions = float(c1+c2)
    try:
        rewards = float(rewards)
    except Exception:
        r1 = rewards.split(',')[0]
        r2 = rewards.split(',')[1]
        rewards = float(r1+r2)

    print('该账户动态钱包为:{0},静态钱包为:{1}'.format(commissions,rewards))

    return commissions,rewards

def TransferMain(commissions,rewards,i):
    v = 0
    # 动静态都有或者有动态无静态
    while commissions > 0 or rewards > 0:
        if (commissions > 0 and rewards > 0) or (commissions > 0 and rewards == 0):
            Select(driver.find_element_by_id("wallet")).select_by_value('2: 1')
            driver.find_element_by_id('amount').send_keys(commissions)
            content = transfer()
            v = 1
        # 有静态无动态
        elif commissions == 0 and rewards > 0:
            Select(driver.find_element_by_id("wallet")).select_by_value('3: 3')
            driver.find_element_by_id('amount').send_keys(rewards)
            content = transfer()
            v = 2
        if content == 0:
            data.loc[i - 1, '报错内容'] = '获取验证码超时'
            DataFrame(data).to_excel('圈米资料.xlsx', index=False, header=True)
            return
        try:
            WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.ID, 'username'))).send_keys('bjyh001')
            WebDriverWait(driver, 10, 1).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="header"]/div[2]/app-transfer/div/form/div[1]/div/i'))).click()
        except Exception:
            data.loc[i - 1, '报错内容'] = '未填入账号'
            DataFrame(data).to_excel('圈米资料.xlsx', index=False, header=True)
            print('未填入目标账号')

        sleep(1)

        while 'class="notify-serve"' not in driver.page_source:
            sleep(1)
        else:
            print(WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'notify-serve'))).text)

        driver.find_element_by_id('code').send_keys(content)
        sleep(2)
        driver.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/button').click()
        if WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="header"]/div[2]/app-transfer/app-response-messages/div/p/span'))).text == "You don't have enough traxalt to execute the transaction.":
            data.loc[i - 1, '报错内容'] = 'T币不足'
            DataFrame(data).to_excel('圈米资料.xlsx', index=False, header=True)
            print('T币不足')
            break
        sleep(5)
        try:
            WebDriverWait(driver, 20, 2).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/app-root/app-backoffice/div/app-modal/div/i'))).click()
        except Exception :
            print('转账完成后未找到公告')
        finally:
            commissions, rewards = searchWallet()
            if commissions == 0.0 and v == 1:
                data.loc[i - 1, '动态'] = commissions
                print('该账户的动态奖金：{0}已转账成功'.format(commissions))
            elif rewards == 0.0 and v == 2:
                data.loc[i - 1, '静态'] = rewards
                print('该账户的静态奖金：{0}已转账成功'.format(rewards))

    # 动静都无
    else:
        print('该账户没有米')
        print(i)
        now_time = datetime.now()
        print(now_time)
        # 精确到秒的时间
        new_time = now_time.strftime('%Y-%m-%d %H:%M:%S')
        data.loc[i - 1,'时间'] = new_time
        if v == 0:
            data.loc[i - 1, '动态'] = 0
            data.loc[i - 1, '静态'] = 0
        data.loc[i - 1,'状态'] = '已完成'
        DataFrame(data).to_excel('圈米资料.xlsx', index=False, header=True)
        while '登出' not in driver.page_source:
            sleep(1)
        else:
            WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-backoffice/div/app-sidebar/nav/ul/li[9]/a'))).click()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('window-size=1920x3000') #指定浏览器分辨率
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/local/bin/chromedriver')
driver.implicitly_wait(20)

driver.get('https://backoffice.airbitclub.com/zh-CN/login')


while i <= num:
    account = data.loc[i - 1][1]
    password = data.loc[i - 1][2]
    mail = data.loc[i - 1][3]
    mailpwd = data.loc[i - 1][4]
    print('开始账户为：{0}'.format(account))
    while 'btn-login' not in driver.page_source:
        sleep(1)
    else:
        driver.find_element_by_id('user').clear()
        driver.find_element_by_id('user').send_keys(account)
        sleep(1)
        driver.find_element_by_id('password').clear()
        driver.find_element_by_id('password').send_keys(password)
        sleep(1)
        driver.find_element_by_name('action').click()

    while 'Direct Personal Partners' not in driver.page_source:
        sleep(1)
        if WebDriverWait(driver, 20, 1).until(EC.presence_of_element_located(
                (By.XPATH, '/html/body/app-root/app-login/div/div[1]/p'))).text == ' the password is incorrect ' or ' wrong username or password ':
            data.loc[i - 1, '报错内容'] = '账号或者密码有误，请检查'
            DataFrame(data).to_excel('圈米资料.xlsx', index=False, header=True)
            print('账号或者密码有误，请检查')
    else:
        driver.get('https://backoffice.airbitclub.com/zh-CN/app/transfer')
    try:
        WebDriverWait(driver,20,1).until(EC.presence_of_element_located((By.XPATH,'/html/body/app-root/app-backoffice/div/app-modal/div/i'))).click()
    except Exception:
        print('未找到公告')
    finally:
        try:
            commissions,rewards = searchWallet()
            TransferMain(commissions, rewards,i)
        except Exception:
            pass
        finally:
            i += 1
