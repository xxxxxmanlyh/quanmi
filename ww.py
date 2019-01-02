from pymongo import MongoClient
client = MongoClient()

db = client.BTC
ziliao = db.ziliao
cursor = ziliao.find()

memberlist = db.member#最新表单
cur = memberlist.find()

counts = db.countnum
aa = counts.find()


countnum = db.countw
countcur = countnum.find()

# print(counts.find_one({'name': '包小兰2', 'handler': '包小兰'}))

# counts.update_one({'name':'刘勇豪','handler':'刘勇豪'},{'$set': {'countnum':0}})
# counts.update_one({'name':'廖菊','handler':'刘勇豪'},{'$set': {'handler':'徐莉媛'}})
# axa = counts.find_one({'name': '刘勇豪', 'handler': '刘勇豪'})['comm']
for i in cur:

    print(i)
# for i in cur:
#     data = {
#         'name':i['name'],
#         'account':i['account'],
#         'countnum':0,
#         'comm':0,
#         're':0,
#         'datetime':'',
#         'cash':0,
#         'text':'',
#         'handler':i['handler']
#
#     }
#     counts.insert_one(data)


# for i in countcur:
#     # if i['name'] in ['包小兰', '郑佩', '崔薇', '包花善', '柳玉梅', '王燕', '包天白', '魏儒嘉', '包爱军']:
#     #     countnum.update({'name': i['name']}, {'$set': {'handler': '包小兰'}})
#     # #增
#     # data = {
#     #     'name':i['name'],
#     #     'account':i['account'],
#     #     'countnum':0,
#     #     'handler':i['handler']
#     #
#     # }
#     # countnum.insert_one(data)
#     x = 0
#     if i['handler'] == '刘勇豪':
#         # countnum.update({'name': i['name']}, {'$set': {'countnum': 0}})
#         print(i)

# for i in countcur:
#     data = {
#         'name':i['name'],
#         'account':i['account'],
#         'countnum':0,
#         'comm':0,
#         're':0,
#         'datetime':'',
#         'cash':0,
#         'text':'',
#         'handler':i['handler']
#
#     }
#     counts.insert_one(data)



#删
# counts.remove({'name':'信妍'})
# counts.remove({'name':'刘萍'})
#
# data = {
#     'name':'信妍',
#     'account':'bjxyan',
#     'countnum':0,
#     'comm':0,
#     're':0,
#     'datetime':'',
#     'cash':0,
#     'text':'',
#     'handler':'王晓英'
#
# }
# counts.insert_one(data)
#
# data = {
#     'name':'周美君',
#     'account':'bjzmj',
#     'countnum':0,
#     'comm':0,
#     're':0,
#     'datetime':'',
#     'cash':0,
#     'text':'',
#     'handler':'刘玉芬'
#
# }
# counts.insert_one(data)


# for i in countcur:

    # data = {
    #     'name':'信妍',
    #     'account':'bjxyan',
    #     'countnum':7,
    #     'handler':'王晓英'
    #
    # }
    #countnum.insert_one(data)
    # countnum.update({'account':'bjwtt'},{'$set':{'countnum':22}})
    # if i['handler'] == '刘勇豪':
    #     print(i['name'])
    #     countnum.update({'name': i['name']}, {'$set': {'countnum': 0}})

#print(memberlist.find_one({'name':'朱'}))
# 增
# data = {
#     'name':'姜陈威',
#     'account':'bjjcwei',
#     'acc_number':3,
#     'pw':'jcw654321',
#     'Email':'13587986612@163.com',
#     'Emailpw':'jcw654321',
#     'handler':'王少博'
#
# }
# memberlist.insert_one(data)

# data = {
#     'name':'周美君',
#     'account':'bjzmj',
#     'acc_number':3,
#     'pw':'zmj654321',
#     'Email':'15801399866@163.com',
#     'Emailpw':'afan-801218.',
#     'handler':'刘玉芬',
#         }
# memberlist.insert_one(data)

#删
# memberlist.remove({'name':'王玲3'})
# 改
# memberlist.update({'name':'张树枝', 'handler':'刘勇豪'},{'$set':{'Emailpw':'zsz54321'}})
# memberlist.update({'name':'周志鹏', 'handler':'刘玉芬'},{'$set':{'Emailpw':'rcf654321'}})
#ziliao.remove(spec_or_id={"_id":ObjectId('5050457a1308122ec272d24c')},safe=True)w
#查
#print(ziliao.find_one({'name':'郑珮'}))

#遍历数据
# a = ['李秀敏','裴艳丽','杨印梅','郭小立','李英俊','朱晓光',
#      '卢小娟','刘玉杰','宋建英','项丽清','张丽媛']
# x = 0
# b = [ '王艺霏', '金花', '张丽阁','刘勇豪','江国华','胡治国', '张建国','徐恒春', '曹戈冲', '毛占伟', '张宏杰', '张晓希','赵海娅','张朋玲','李磊','邬美丽','王彬','张云云','乔凤民','程垒','朱义国','张桂芬','张欣','张小飞','孙莹',
#      '王晓英','范为','李想','靳桂兰','王志英','张小杰','王晓燕','赵保玉','文平','白鹤鸣','朱莹莹','张婷','吴建君','奚巧燕','王敏燕','冯亚芳','金亚娣','葛云莲','储彩球',
#      '赵士超', '王若泰','朱晓光','卢小娟','杨倪','陈柱','申艳华','施优琴','庄红娟','杨政','华小英', '王爱华', '陈明双', '朱云华', '杨印梅', '黄海凇', '李英俊','郭一辰','罗春辉','刘玉芬', '冯明强','吴庆军',
#       '胡刚禄', '吴玉玲', '徐燕宇', '刘玉杰', '应鹰', '王培珍','张燕', '李娟娟', '张彩云', '孙炳权', '崔淑玲', '武凯鹏', '高晓瑞','韩春丽','陆雪芬','']
# n = 1
# for i in cursor:
#     x = i['acc_number'] + x
#     a.append(i['name'])
#     print(i)
# print(a)
# print(x)

# for i in cur:
#
#     if i['name'] in ['包小兰', '郑佩', '崔薇', '包花善', '柳玉梅', '王燕', '包天白', '魏儒嘉', '包爱军']:
#
#         # data = {
#         #     'name':i['name'],
#         #     'account':i['account'],
#         #     'acc_number':i['acc_number'],
#         #     'pw':i['pw'],
#         #     'Email':i['Email'],
#         #     'Emailpw':i['Emailpw'],
#         #     'handler':'江国华'
#         #
#         # }
#         # memberlist.insert_one(data)
#         memberlist.update({'name': i['name']}, {'$set': {'handler': '包小兰'}})


#增
# data = {
#     'name':'柳玉梅2',
#     'account':'sdlym',
#     'acc_number':3,
#     'pw':'zyh654321',
#     'Email':'myr6161278@163.com',
#     'Emailpw':'zyh1212',
#     'handler':'郭一辰'
#
# }
# memberlist.insert_one(data)
# memberlist.update({'name':'张晓梅','handler': '刘勇豪'},{'$set':{'Emailpw':'xm6767'}})
#memberlist.remove({'name':'乔晓曦'})
# zll=[]
# lyh=[]
# clp=[]
# wl=[]
# wsb=[]
# wxy=[]
# for i in aa:
# #     if i['handler'] == '周丽丽':
# #        zll.append(i['name'])
#        #  print('姓名：'+i['name'])
#        #  print('账号：{0}001-00{1}'.format(i['account'],i['acc_number']))
#        #  print('密码：'+i['pw'])
#        #  print('邮箱：' + str(i['Email']))
#        #  print('邮箱密码：'+ str(i['Emailpw']))
#        #  print('\n')
#     if i['handler'] == '刘勇豪':
#         lyh.append(i['name'])
#     if i['handler'] == '徐莉媛':
#         clp.append(i['name'])
#     if i['handler'] == '李秀敏':
#         wl.append(i['name'])
#     if i['handler'] == '包小兰':
#         # print(i['acc_number'])
#         print(i)
#         wsb.append(i['name'])
#     if i['handler'] == '周义霞':
#         wxy.append(i['name'])
#     print(i)
#
# print(zll)
# print(lyh)
# print(clp)
# print(wl)
# print(wsb)
# print(wxy)