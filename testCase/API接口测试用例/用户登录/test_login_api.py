#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/1 21:27
# @File : test_login_api.py
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : loginAPI登录接口测试
import allure
import pytest

from utils.excel_tools import get_ExcelDataByCaseName


@allure.epic("X-ERP系统接口测试")
@allure.feature("登录模块接口测试")
class TestLoginAPI:

    @allure.story("登录功能测试")
    @pytest.mark.login
    @pytest.mark.parametrize("inData,expectedData,title", get_ExcelDataByCaseName("登录模块", "Login"))
    def test_login(self, inData, expectedData, title, init_loginApi):
        """
        登录接口测试
        :param inData:
        :param expectedData:
        :param title:
        :param init_loginApi:
        :return:
        """
        allure.dynamic.title(f"{title}")
        allure.dynamic.description(f"接口登录测试:{title}")
        resp = init_loginApi.login(inData)
        if "loginStatus" in resp.keys():
            assert resp["loginStatus"] == expectedData["loginStatus"] and resp["userId"] is not None
        elif "state" in resp.keys():
            assert resp["message"] == expectedData["message"]
        else:
            assert resp["status_code"] == 9999 or resp["status_code"] == 502

    @allure.story("退出登录功能")
    @allure.title("退出登录")
    @pytest.mark.sigout
    def test_sigout(self, get_token, init_loginApi):
        loginApi = init_loginApi
        token = get_token[0]
        resp = loginApi.sigout(token)
        assert resp["message"] == "退出成功"

