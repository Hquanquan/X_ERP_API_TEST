#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/3 9:27
# @File : conftest.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import pytest

from configs.api_env import userInfo1
from pylib.APILib.commonAPI import CommonAPI
from pylib.APILib.loginAPI import LoginAPI
from pylib.APILib.客户管理.clueAPI import ClueAPI
from pylib.APILib.客户管理.customerAPI import CustomerAPI
from utils.string_tools import create_clueInfo_dict, get_phone_num, create_customerInfo_dict

@pytest.fixture(scope="package")
def initClueApi(get_token):
    """
    初始化ClueAPI对象
    :param get_token:
    :return:
    """
    clueApi = ClueAPI(get_token[0])
    yield clueApi

@pytest.fixture()
def init_clue(initClueApi):
    """
    初始化：创建线索
    :param initClueApi:
    :return:
    """
    clueApi = initClueApi
    clueInfo = create_clueInfo_dict()
    resp = clueApi.save_clue(clueInfo)
    yield clueApi, resp, clueInfo

@pytest.fixture()
def init_extension_clue(getClueAPI):
    """
    初始化创建推广线索
    :return:
    """
    clueApi = getClueAPI
    clueInfo = create_clueInfo_dict(isExtensionClue=True)
    resp = clueApi.save_clue(clueInfo)
    yield clueApi, resp, clueInfo

@pytest.fixture(scope="package")
def getClueAPI():
    loginApi = LoginAPI()
    indate = userInfo1
    token = loginApi.getToken(indate)
    clueApi = ClueAPI(token)
    yield clueApi

@pytest.fixture(scope="package")
def initCustomerAPI(get_token):
    """
    初始化CustomerAPI对象
    :param get_token:
    :return:
    """
    customerApi = CustomerAPI(get_token[0])
    commomApi = CommonAPI(get_token[0])
    userId = get_token[1]
    yield customerApi, commomApi, userId

@pytest.fixture()
def init_customer(get_token):
    """
    创建客户
    :param get_token:
    :return:
    """
    customerApi = CustomerAPI(get_token[0])
    commomApi = CommonAPI(get_token[0])
    # 获取企业工商信息
    enterprise_info = commomApi.get_enterprise_info("91110000710921189P")["value"][0]
    # 获取当前登录人部门信息
    userId = get_token[1]
    # 获取当前账号所在分公司编号
    followCompany = commomApi.getOrgByUserId(userId)['value'][0]['id']
    # 获取线索编号
    # clueApi = ClueAPI(get_token[0])
    # clueNo = clueApi.get_myself_clue()["value"]["rows"][0]["clueNo"]
    # 使用函数生成客户参数字段信息
    customerInfo = create_customerInfo_dict(enterprise_info, followCompany=followCompany)
    resp = customerApi.create_customer(customerInfo)
    yield customerApi, commomApi, resp, customerInfo

