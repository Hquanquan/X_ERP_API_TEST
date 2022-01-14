#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 9:16
# @File : test.py.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import base64
from pprint import pprint

from pylib.APILib.loginAPI import LoginAPI
from pylib.APILib.客户管理.clueAPI import ClueAPI

if __name__ == '__main__':
    # login = LoginAPI()
    # indata = {"username": "QY000311", "password": "MTIzNDU2"}
    # token = login.getToken(indata)
    # clueAPI = ClueAPI(token)
    # # ================ 获取我的线索 ==================
    # resp = clueAPI.get_myself_clue(pageBean={'page': 100, 'pageSize': 1})
    #
    # # indata = {"pageBean": {"page": 1, "pageSize": 50},
    # #           "params": {"clueTag": "", "clueState": "", "followOrg": "", "followBy": ""}}
    # # resp = clueAPI.get_myself_clue(indata)
    #
    # # querys = [{"property": "person", "value": "联系人", "group": "quick", "relation": "OR", "operation": "LIKE"}]
    # # resp = clueAPI.get_myself_clue(querys=querys)
    #
    # # =================== 保存线索 ================
    # # resp = clueAPI.save_clue(phone=get_phone_num())
    # # phone = get_phone_num()
    # # resp = clueAPI.save_clue(person=f"联系人{phone}", phone=phone)
    #
    # pprint(resp)

    # import datetime  # 导入日期时间模块
    # # today = datetime.date.today()  # 获得今天的日期
    # today = datetime.datetime.now()
    # dt = datetime.datetime.now()
    # current_time = dt.strftime(time_formate)
    # yesterday = today - datetime.timedelta(days=1)  # 用今天日期减掉时间差，参数为1天，获得昨天的日期
    #
    # tomorrow = today + datetime.timedelta(days=1)  # 用今天日期加上时间差，参数为1天，获得明天的日期
    #
    # print(yesterday)
    # print(tomorrow)
    """
        # 想将字符串转编码成base64,要先将字符串转换成二进制数据
        url = "https://www.cnblogs.com/songzhixue/"
        bytes_url = url.encode("utf-8")
        str_url = base64.b64encode(bytes_url)  # 被编码的参数必须是二进制数据
        print(str_url.decode())
        str_1 = base64.b64encode(url.encode()).decode()
    
        # b'aHR0cHM6Ly93d3cuY25ibG9ncy5jb20vc29uZ3poaXh1ZS8='
    """
    # 将base64解码成字符串
    # import base64
    #
    # url = "aHR0cHM6Ly93d3cuY25ibG9ncy5jb20vc29uZ3poaXh1ZS8="
    # str_url = base64.b64decode(url).decode("utf-8")
    # print(str_url)
    #
    # str_1 = base64.b64encode(str_url.encode()).decode()
    # print(str_1)
    # # 'https://www.cnblogs.com/songzhixue/'

    a = ["11"]
    b = []
    print(len(b) == 0)


