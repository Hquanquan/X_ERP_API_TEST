#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 10:48
# @File : loginAPI.py
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : 登录认证接口api

from pprint import pprint
import requests

from configs.api_env import HOST
from logs.logger import Logger
from utils.base64加密 import myBase64
from utils.time_tools import get_timeString

logger = Logger(logger="LoginAPI").getlog()
class LoginAPI:
    """
    登录认证接口api
    """

    def __init__(self):
        self.HOST = HOST
        self.headers = {"Content-Type": "application/json;charset=UTF-8"}

    def login001(self, userName, passWord):
        """
        登录：分别输入用户名，密码登录系统
        :param userName: 用户名
        :param passWord: 密码
        :return:
        """
        # http://192.168.1.25:8380/uc-api/auth?tenantId=
        # {"username":"QY000341","password":"MTIzNDU2"}
        # Content-Type: application/json;charset=UTF-8
        # 请求头
        header = {
            "Content-Type": "application/json;charset=UTF-8",
            "Referer": f"{HOST}/fuve/login"
        }
        # 请求URL
        url = f"{HOST}/uc-api/auth?tenantId="
        # 请求体
        inData = {"username": userName, "password": passWord}
        payload = inData
        # post 请求方法
        resp = requests.post(url, headers=header, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    def login(self, inDate):
        """
        登录:直接以字典的形式传递所有的参数
        :param inDate: 字典类型的参数，如：{"username": username, "password": password}
        :return:
        """
        # 请求URL
        url = f"{HOST}/uc-api/auth?tenantId="
        logger.info(f"{get_timeString()} url is {url}")
        logger.info(f"{get_timeString()} Request headers is {self.headers}")
        password = inDate["password"]
        inDate["password"] = myBase64(password)
        payload = inDate
        logger.info(f"{get_timeString()} Request payload is {payload}")
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    def getToken(self, inDate):
        """
        获取用户登录后的token
        :param inDate:
        :return:
        """
        resp = self.login(inDate)
        return resp["token"]

    def sigout(self, token):
        """
        退出登录
        :return:
        """
        self.headers["Authorization"] = "Bearer " + token
        url = f"{HOST}/uc-api/signout"
        logger.info(f"{get_timeString()} url is {url}")
        logger.info(f"{get_timeString()} Request headers is {self.headers}")
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}


if __name__ == '__main__':
    login = LoginAPI()
    # # resp = login.login001("QY000341","MTIzNDU2")
    indata = {"username": "QY000341", "password": "123456"}
    resp = login.login(indata)
    # token = login.getToken(indata)
    # print(token)
    # resp = login.sigout(token)
    # print(type(resp))
    pprint(resp)
    # # resp.replace("true", "True").replace("false", "False")
    # pprint(resp)
