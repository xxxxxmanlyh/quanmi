from selenium import webdriver
import time
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import poplib
from email.parser import Parser
from pymongo import MongoClient
import string

class Quanmi(object):

    #登录函数
    def login(self,account,pw,wd):
        wd.get("https://backoffice.airbitclub.com/zh-CN/login")  # 打开登录界面
        wd.find_element_by_id("user").clear()
        wd.find_element_by_id("user").send_keys(account)  # 清除输入框并且输入账户
        wd.find_element_by_id("password").clear()
        wd.find_element_by_id("password").send_keys(pw)  # 清除输入框并且输入密码
        wd.find_element_by_name('action').click()  # 点击登录

        time.sleep(5)

        wd.get('https://backoffice.airbitclub.com/zh-CN/app/transfer')
        time.sleep(2)
        wd.find_element_by_xpath('/html/body/app-root/app-backoffice/div/app-modal/div/i').click()
        return wd

    #获取验证码
    def gettoken(self,wd,usermail,mailusermailpassword):
        acounttime = 0
        maillen = self.get_parsed_msg(usermail, mailusermailpassword)[1]
        while maillen > 0:
            time.sleep(10)
            maillens = self.get_parsed_msg(usermail, mailusermailpassword)[1]
            if maillens > maillen:
                msg = self.get_parsed_msg(usermail, mailusermailpassword)[0]
                parts = msg
                try:
                    content = str(parts).split('<hr style=3D"border-bottom:1px solid #FFC300;">')[1][:6].strip()
                    print(content)
                except Exception as e:
                    while maillens > 0:
                        maillenmax = self.get_parsed_msg(usermail, mailusermailpassword)[1]
                        if maillenmax > maillens:
                            msg = self.get_parsed_msg(usermail, mailusermailpassword)[0]
                            parts = msg.get_payload()
                            content = str(parts).split('<hr style=3D"border-bottom:1px solid #FFC300;">')[1][:9].strip()
                            break
                        else:
                            time.sleep(5)
                        print(content)

                wd.find_element_by_id("code").send_keys(content)
                time.sleep(1)
                maillen = -1
                acounttime = 0
            # else:
            #     if acounttime >= 900:
            #         wd.find_element_by_xpath(
            #             '//a[@class="btn btn-flat btn-danger btn-xs cancel-token pull-right col-md-3 btn-ripple"]').click()
            #         time.sleep(2)
            #         wd.find_element_by_id('submit-token').click()
            #         self.gettoken(wd,usermail,mailusermailpassword)
            #     else:
            #         time.sleep(8)
            #         acounttime = acounttime + 8


    #查看 动静态钱包数
    def getCR(self,wd):
        locator = (By.XPATH, '//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div/div[2]/div[2]')
        locators = (By.XPATH, '//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div/div[3]/div[2]')
        try:
            WebDriverWait(wd, 20, 1).until(EC.presence_of_element_located(locator))
            comm = wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div[2]/div[2]/div[2]').text  # 获取动态钱包钱数
            WebDriverWait(wd, 20, 1).until(EC.presence_of_element_located(locators))
            re = wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div[2]/div[3]/div[2]').text  # 获取静态钱包钱数
        except Exception as e:
            WebDriverWait(wd, 20, 1).until(EC.presence_of_element_located(locator))
            comm = wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div[2]/div[2]/div[2]').text  # 获取动态钱包钱数
            WebDriverWait(wd, 20, 1).until(EC.presence_of_element_located(locators))
            re = wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/app-carrousel-wallets-detail/div/div/div[2]/div[3]/div[2]').text  # 获取静态钱包钱数
        if len(comm.split('$')[1].split(',')) == 1 :
            if float(comm.split('$')[1]) == 0.00:
                newcomm = comm = 0.00
            elif float(comm.split('$')[1]) > 0:
                comm = float(comm.split('$')[1])
                newcomm = comm
        else:
            newcomm = comm.split('$')[1].split(',')[0] + comm.split('$')[1].split(',')[1]
            comm = float(newcomm)
        if len(re.split('$')[1].split(',')) == 1 :
            if float(re.split('$')[1]) == 0.00:
                newre = re = 0.00
            elif float(re.split('$')[1]) > 0:
                # re = re[1:].translate(str.maketrans('', '', string.punctuation))
                re = float(re.split('$')[1])
                newre = re
        else:
            newre = re.split('$')[1].split(',')[0] + re.split('$')[1].split(',')[1]
            # re = float(newre)

        return comm,re,newcomm,newre

    #转账算法
    def Transfer(self,wd,i,sponsor,account,maxnum,name,handler,usermail,mailusermailpassword):
        wd.find_element_by_xpath('/html/body/app-root/app-backoffice/div/app-modal/div/i').click()
        counts = self.mongod()[1]
        comm = self.getCR(wd)[0]
        re = self.getCR(wd)[1]
        newcomm = self.getCR(wd)[2]
        newre = self.getCR(wd)[3]
        if i == maxnum:
            print("第{0}个账户动态钱包：{1}美金，静态：{2}美金".format(1, comm, re))
        else:
            print("第{0}个账户动态钱包：{1}美金，静态：{2}美金".format(i + 1, comm, re))
        if comm == 0 and re == 0:
            wd.quit()
        while comm >0 or re >0:
            locatoruser = (By.ID, 'username')
            try:
                WebDriverWait(wd, 60, 2).until(EC.element_to_be_clickable(locatoruser))
                wd.find_element_by_id('username').send_keys(sponsor)
            except Exception as e:
                print('没有填进去')
            time.sleep(1)
            if wd.find_element_by_id('username').text == '':
                wd.find_element_by_id('username').clear()
                wd.find_element_by_id('username').send_keys(sponsor)
            time.sleep(2)
            wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/div[1]/div/i').click()
            # wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/div[1]/div/i').click()
            time.sleep(2)
            wd.find_element_by_xpath(
                '//*[@id="header"]/div[2]/app-transfer/div/form/div[2]/div/i').click()  # 点击发送token请求
            self.gettoken(wd, usermail, mailusermailpassword)
            a = 5
            while True:
                time.sleep(a)
                sname = wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/div[1]/div/span').text
                if sname == '':
                    a = a + 5
                    if a == 30:
                        self.Transfer(wd,i,sponsor,account,maxnum,name,handler,usermail,mailusermailpassword)
                    else:
                        wd.find_element_by_id('username').clear()
                        wd.find_element_by_id('username').send_keys(sponsor)
                        wd.find_element_by_id('//*[@id="header"]/div[2]/app-transfer/div/form/div[1]/div/i').click()
                else:
                    break
            if comm > 0 and re == 0:
                Select(wd.find_element_by_id("wallet")).select_by_value('2: 1')
                wd.find_element_by_id('amount').send_keys(newcomm)
                wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/button').click()
                time.sleep(2)
                wd.get('https://backoffice.airbitclub.com/zh-CN/app/transfer')
                time.sleep(2)
                wd.find_element_by_xpath('/html/body/app-root/app-backoffice/div/app-modal/div/i').click()
                time.sleep(2)
                comms = self.getCR(wd)[0]
                res = self.getCR(wd)[1]
                while True:
                    if comms == 0 and res == 0:
                        print("{0}账户：动态金额：{1},已转入{2}账号中".format(account, newcomm, sponsor))
                        oldcomm = counts.find_one({'name': name, 'handler': handler})['comm']
                        counts.update_one({'name': name, 'handler': handler}, {'$set': {'comm': newcomm+oldcomm}})
                        print("{0}账户：动态金额：{1},已转入{2}账号中".format(account, newcomm+oldcomm, sponsor))
                        comm = 0
                        newcomm = comm
                        wd.quit()
                        break
                    else:
                        time.sleep(5)
                        # wd.refresh()
                        comms = self.getCR(wd)[0]
                        res = self.getCR(wd)[1]
            elif re > 0 and comm == 0:
                Select(wd.find_element_by_id("wallet")).select_by_value('3: 3')
                wd.find_element_by_id('amount').send_keys(newre)
                wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/button').click()
                time.sleep(2)
                wd.get('https://backoffice.airbitclub.com/zh-CN/app/transfer')
                time.sleep(2)
                wd.find_element_by_xpath('/html/body/app-root/app-backoffice/div/app-modal/div/i').click()
                time.sleep(2)
                comms = self.getCR(wd)[0]
                res = self.getCR(wd)[1]
                while True:
                    if comms == 0 and res == 0:
                        oldre = counts.find_one({'name': name, 'handler': handler})['re']
                        counts.update_one({'name': name, 'handler': handler}, {'$set': {'re': oldre+newre}})
                        print("{0}账户：静态金额：{1},已转入{2}账号中".format(account, newre+oldre, sponsor))
                        re = 0
                        newre = re
                        wd.quit()
                        break
                    else:
                        time.sleep(5)
                        # wd.refresh()
                        comms = self.getCR(wd)[0]
                        res = self.getCR(wd)[1]
            elif comm > 0 and re > 0:
                Select(wd.find_element_by_id("wallet")).select_by_value('3: 3')
                wd.find_element_by_id('amount').send_keys(newre)
                wd.find_element_by_xpath('//*[@id="header"]/div[2]/app-transfer/div/form/button').click()
                time.sleep(2)
                wd.get('https://backoffice.airbitclub.com/zh-CN/app/transfer')
                time.sleep(2)
                wd.find_element_by_xpath('/html/body/app-root/app-backoffice/div/app-modal/div/i').click()
                time.sleep(2)
                comms = self.getCR(wd)[0]
                res = self.getCR(wd)[1]
                while True:
                    if comms > 0 and res == 0:
                        print("{0}账户：静态金额：{1},已转入{2}账号中".format(account, newre, sponsor))
                        counts.update_one({'name': name, 'handler': handler}, {'$set': {'re': newre}})
                        re = 0
                        newre = re
                        break
                    else:
                        time.sleep(5)
                        wd.refresh()
                        comms = self.getCR(wd)[0]
                        res = self.getCR(wd)[1]
        if i == maxnum:
            comm = counts.find_one({'name':name,'handler':handler})['comm']
            re = counts.find_one({'name': name, 'handler': handler})['re']
            if comm == 0 and re == 0:
                pass
            else:
                self.getacount(comm, re, name, handler)

    #主函数
    def main(self,namelist,handler):
        counts = self.mongod()[1]
        memberlist = self.mongod()[0]
        cur = memberlist.find()
        curs = counts.find()
        maxlist = namelist
        newnamelist = []
        for i in cur:
            if i['handler'] == handler:
                # if i['name'] in maxlist:
                #     pass
                # else:
                #     countnum = counts.find_one({'name': i['name'], 'handler': handler})['countnum']
                #     if countnum > i['acc_number']:
                #         pass
                #     else:
                #         newnamelist.append(i['name'])
                # if i['name'] in ['张丽','张克成','程纪余','张如梅','段永生','刘军','张淑芬','朱斌','包建东','廖菊','张文革','寿立庆','牟艳丽','王玉荣','霍棠椿','尤蕊','王福亮','周爱莲','牛和美','王晓芝2','吕志强','蔡丽娟','王海微','鄢林华','路晓平','路统州']:#,'吕志强','陈艳梅','李红岗','范晨','将记山','张树枝','宋清华','吴燕','吴君兰','吕志强', '刘庆云', '裴新韦','周爱莲','汪佳洁','齐德修','王修华','张银菊'
                if i['name'] in ['刘勇豪']:
                    countnum = counts.find_one({'name': i['name'], 'handler': '刘勇豪'})['countnum']

                    if countnum > i['acc_number']:
                        pass
                    else:
                        newnamelist.append(i['name'])
                else:
                   pass
        for name in newnamelist:
            if counts.find_one({'name': name, 'handler': handler})['countnum'] == 0:
                i = counts.find_one({'name': name, 'handler': handler})['countnum'] + 1
            else:
                i = counts.find_one({'name': name, 'handler': handler})['countnum']
            maxnum = memberlist.find_one({'name': name, 'handler': handler})['acc_number']
            account_1 = memberlist.find_one({'name': name, 'handler': handler})['account']
            pw = memberlist.find_one({'name': name, 'handler': handler})['pw']
            usermail = memberlist.find_one({'name': name, 'handler': handler})['Email']
            Rusermail = usermail
            mailusermailpassword = memberlist.find_one({'name': name, 'handler': handler})['Emailpw']
            Rmailusermailpassword = mailusermailpassword
            sponsor = 'bjyh001'
            print("{0}的账户一共有{1}个".format(name, maxnum))
            while i <= maxnum:
                if i >= 9:
                    account = account_1 + "0" + str(i + 1)
                    if name == '寿立庆' and i == 9:
                        account = account_1 + "00" + str(i + 1)
                else:
                    account = account_1 + "00" + str(i + 1)
                    if name == '江国华' and i == 3:
                        account = account_1 + str(i + 1)

                if i == maxnum:
                    break
                    print("开始第{0}个账户圈米".format(1))
                elif i < maxnum:
                    print("开始第{0}个账户圈米".format(i + 1))
                wd = webdriver.Chrome("/usr/local/bin/chromedriver")
                wd.implicitly_wait(10)
                print(account,pw)
                self.login(account,pw,wd)
                if len(usermail) == 2 and i == maxnum:
                    if len(mailusermailpassword) ==2:
                        Rmailusermailpassword = mailusermailpassword[0]
                    Rusermail= usermail[0]
                elif len(usermail) == 2 and i < maxnum:
                    if len(mailusermailpassword) ==2:
                        Rmailusermailpassword = mailusermailpassword[1]
                    Rusermail = usermail[1]
                if len(usermail) == 3 and i == maxnum:
                    if len(mailusermailpassword) >1:
                        Rmailusermailpassword = mailusermailpassword[0]
                    Rusermail = usermail[0]
                elif len(usermail) == 3 and i == 1:
                    if len(mailusermailpassword) >1:
                        Rmailusermailpassword = mailusermailpassword[1]
                    Rusermail = usermail[1]
                elif len(usermail) == 3 and i == 2:
                    if len(mailusermailpassword) >1:
                        Rmailusermailpassword = mailusermailpassword[2]
                    Rusermail = usermail[2]

                self.Transfer(wd,i,sponsor,account,maxnum,name,handler,Rusermail,Rmailusermailpassword)
                i = i + 1
                counts.update_one({'name': name, 'handler': handler}, {'$set': {'countnum': i}})
        self.collect(handler)

    # 邮箱连接
    def get_parsed_msg(self,usermail, password):
        # 邮箱个人信息
        useraccount = usermail
        password = password
        if useraccount.split("@")[1:][0] == "126.com":
            # 邮件服务器地址
            pop3_server = 'pop.126.com'
        elif useraccount.split("@")[1:][0] == "163.com":
            # 邮件服务器地址
            pop3_server = 'pop.163.com'
        # 开始连接到服务器
        try:
            server = poplib.POP3(pop3_server)
        except Exception as e:
            time.sleep(10)
            server = poplib.POP3(pop3_server)
        # 开始进行身份验证
        server.user(useraccount)
        server.pass_(password)
        # 使用list()返回所有邮件的编号，默认为字节类型的串
        resp, mails, octets = server.list()
        # 下面单纯获取最新的一封邮件
        total_mail_numbers = len(mails)
        # 默认下标越大，邮件越新，所以total_mail_numbers代表最新的那封邮件
        response_status, mail_message_lines, octets = server.retr(total_mail_numbers)
        msg_content = b'\r\n'.join(mail_message_lines).decode('gbk')
        # 邮件原始数据没法正常浏览，因此需要相应的进行解码操作
        msg = Parser().parsestr(text=msg_content)
        # print('解码后的邮件信息:\n{}'.format(msg))
        # 关闭与服务器的连接，释放资源
        server.close()
        return msg, total_mail_numbers

    #连接数据库
    def mongod(self):
        client = MongoClient()  # 连接mongoDB
        db = client.BTC  # 连接数据库
        memberlist = db.member  # 找到合集
        counts = db.countnum  # 钱和计数的记录
        return memberlist,counts

    # 提现格式计算
    def getacount(self,missUSD, rewardUSD, name,handler):
        datetime = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
        missRMB = (float(missUSD)) * 6.8
        rewardRMB = float(rewardUSD) * 6.8
        allUSD = float(missUSD) + float(rewardUSD)
        counts = self.mongod()[1]
        # 改
        counts.update_one({'name':name, 'handler':handler},{'$set':{'text':'{0}\n姓名：{1}\n分享收益:({2})＄*6.8={3}元\n理财收益:{4}＄*6.8={5}元\n总计：({6}美金)×6.8=({7})人民币'.format(datetime,name,missUSD,int(missRMB),rewardUSD,int(rewardRMB),allUSD,int(missRMB + rewardRMB)),'datetime':datetime, 'cash':int(missRMB + rewardRMB)}})

    #汇总
    def collect(self,handler):
        datetime = time.strftime('%Y年%m月%d日', time.localtime(time.time()))
        counts = self.mongod()[1]
        cur = counts.find()
        price = 0
        for i in cur:
            if i['handler'] == handler and i['datetime'] == datetime:
                price = price + i['cash']
                if i['cash'] > 0:
                    print(i['text'])
                    print('\n')
                # itchat.send('{0}需发人民币：{1}'.format(i['name'], i['cash']),toUserName='{0}'.format(fromusername))
                counts.update_one({'name':i['name'], 'handler':handler},{'$set':{'countnum': 0, 'comm': 0, 're': 0, 'datetime':'', 'cash':0,'text':''}})
        print("{0}{1}团队总共需要发人民币：{2}元".format(datetime, handler, price))


handler = '刘勇豪'
namelist = ['徐莉媛','鄢林华','朱冬', '龙敬东', '范筑华', '尹昊雯霞','陈慧丽','覃玉连','李彩娟','杨东梅','方亚文','秦小龙','查乙丁','寿立庆','张晓梅','周忠玺','张建春']
# namelist = ['刘勇豪', '张丽', '牟艳丽', '张克成', '杨翠芝', '周爱莲', '寿立庆', '吕志强', '朱冬', '刘庆云', '裴新韦', '高二敏', '程纪余', '郝宝玲', '马楠','翁金林','赵秋雪', '覃玉连', '陈慧丽', '汪佳洁', '张晓梅', '周晶晶', '李彩娟', '郝婧萱', '周忠玺', '方亚文', '王修华', '张建春', '段永生', '刘光碧', '王玉亭', '秦小龙', '查乙丁', '王观池']
# namelist = ['包小兰', '郑佩', '崔薇', '包花善', '柳玉梅', '王燕', '包天白', '魏儒嘉', '包爱军', '杨东梅', '包小兰2', '张英', '张金全', '苏玉霞', '李玉梅', '柳玉梅2', '吕萍', '于秀琴', '邹心明']
aa = Quanmi()
aa.main(namelist,handler)