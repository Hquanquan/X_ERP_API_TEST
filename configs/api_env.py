#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 10:45
# @File : api_env.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : 接口测试的环境配置

# 1、接口测试的URL地址
# 测试环境
HOST = "http://192.168.1.25:8380"
# 6080环境
# HOST = "http://192.168.1.26:6080"


# 2、接口测试用例的相对路径
TestCaseFilePath = r"./data/X-ERP系统接口测试用例.xls"

# 3、登录用户账号QY000311  MTIzNDU2

userinfo = {"username": "QY000311", "password": "123456"}

# 4、测试推广线索相关功能的账号
userInfo1 = {"username": "QY000215", "password": "123456"}

