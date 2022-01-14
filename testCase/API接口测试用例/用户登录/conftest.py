#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/1 21:24
# @File : conftest.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import allure
import pytest

from configs.api_env import userinfo
from pylib.APILib.loginAPI import LoginAPI


@pytest.fixture(scope="session")
def get_token():
    """
    获取登录账号的token
    :return:
    """
    loginApi = LoginAPI()
    indate = userinfo
    userInfo = loginApi.login(indate)
    token = userInfo["token"]
    ueserId = userInfo["userId"]
    yield token, ueserId


@pytest.fixture(scope="session")
def init_loginApi():
    """
    初始化一个LoginAPI实例对象
    :return:
    """
    loginApi = LoginAPI()
    yield loginApi
