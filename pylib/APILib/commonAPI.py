#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 12:53
# @File : commonAPI.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import copy
import json
from pprint import pprint

from pylib.APILib.baseAPI import BaseAPI
import requests

from pylib.APILib.loginAPI import LoginAPI


class CommonAPI(BaseAPI):
    """
    公共调用的接口
    """

    # 获取用户角色
    def getRolesByUser(self, username):
        """
        获取用户角色
        :param username: 用户名 QY000341
        :return:
        """
        url = f"{self.HOST}/uc-api/api/role/v1/role/getRolesByUser?account={username}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    def getDetailByAccountOrId(self, username):
        """
        根据用户名获取详细的用户信息
        :param username:
        :return:
        """
        url = f"{self.HOST}/uc-api/api/user/v1/user/getDetailByAccountOrId?"
        inData = {"account": username}
        payload = inData
        resp = requests.get(url, headers=self.headers, params=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取当前用户的前端菜单
    def getCurrentUserMenu(self, inData=None, **kwargs):
        """
        获取当前用户的前端菜单
        :param inData: { menuAlias: front_menu }
        :return:
        """
        url = f"{self.HOST}/portal-api/sys/sysMenu/v1/getCurrentUserMenu?"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中getCurrentUserMenu的内容
            # 使用深拷贝，避免data与self.conf["getCurrentUserMenu"]共用内存
            data = copy.deepcopy(self.conf["getCurrentUserMenu"])
            if bool(data):
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data.keys()]
                # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
                for onekey in params_keyslist:
                    if onekey in kwargs.keys():
                        data[onekey] = kwargs[onekey]
        resp = requests.get(url, headers=self.headers, params=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取当前用户方法身份验证
    def getCurrentUserMethodAuth(self):
        """
        获取当前用户方法身份验证
        :return:
        """
        url = f"{self.HOST}/portal-api/sys/sysMenu/v1/getCurrentUserMethodAuth"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取字典选项（多层级展示）
    def getFormatDics(self, inData=None, **kwargs):
        """
        获取字典选项（多层级展示）
        :param inData:
        {"nodeKey": "visit_type"}      获取根据方式
        {"nodeKey":"new_timeout"}
        {"nodeKey":"intention_to_grade"}    获取意向等级
        {"nodeKey":"area_manage", "isFormat":1}  获取地区
        {"nodeKey": "extend_clue_source"}   获取推广线索来源
        {"nodeKey": "my_clue_source"}       获取我的线索来源
        {"nodeKey": "clue_intention_level"}     获取我的线索意向等级
        {"nodeKey": "clue_demand_type"}         获取我的线索需求分类
        {"nodeKey": "my_clue_state"}            获取我的线索状态
        {"nodeKey": "clue_type"}            获取线索分类
        {"nodeKey": "clue_tag", "isFormat":1}   获取线索标签
        {"nodeKey": "clue_state"}       获取线索状态
        :return:
        """
        url = f"{self.HOST}/portal-api/api/common/v1/getFormatDics?"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中getFormatDics的内容
            # 使用深拷贝，避免data与self.conf["getFormatDics"]共用内存
            data = copy.deepcopy(self.conf["getFormatDics"])
            if bool(data):
                data.update(kwargs)
            payload = data
        resp = requests.get(url, headers=self.headers, params=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 查询用户：按用户名查询
    def querySubUser(self, userName):
        """
        查询用户：按用户名查询
        :param userName:
        {"querys":[
        {"group":"main","operation":"LIKE","property":"FULLNAME_","relation":"OR","value":"李振辉"},
        {"group":"main","operation":"LIKE","property":"EMAIL_","relation":"OR","value":"李振辉"}
        ]}
        :return:
            {   'page': 1,
                'pageSize': 10,
                'rows': [{'email': 'lizhenhui@xzjt.cn',
                        'fullname': '李振辉',
                        'id': '1407876697361092608',
                        'pathName': '【/携众集团/朱炜杰总经理/朱炜杰副总经理（兼）/山东、
                        安徽、重庆运营中心/山东青岛分公司】,【/携众集团/朱炜杰总经理/朱炜
                        杰副总经理（兼）/山东、安徽、重庆运营中心/青岛携众筑业企业管理咨询有限公司】'}],
                'total': 1}
        """
        url = f"{self.HOST}/uc-api/api/user/v1/users/querySubUser/precise"
        # 读取接口配置模板文件中querySubUser的内容
        # 使用深拷贝，避免data与self.conf["querySubUser"]共用内存
        data = copy.deepcopy(self.conf["querySubUser"])
        params_keyslist = data["querys"]
        # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
        for onekey in params_keyslist:
            onekey["value"] = userName
        payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取新闻公告菜单
    def getNewsTree(self):
        """
        获取新闻公告菜单
        :return:
        """
        url = f"{self.HOST}/portal-api/portalNewsNoticePlus/v1/getNewsTree"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 通过新闻公告菜单id获取新闻公告里的新闻
    def getNewsByClassfyId(self, classifyId):
        """
        通过新闻公告菜单id获取新闻公告里的新闻
        :param classifyId:
        :return:
        """
        url = f"{self.HOST}/portal-api/portalNewsNoticePlus/v1/getNewsByClassfyId?"
        inData = {"classifyId": classifyId}
        payload = inData
        resp = requests.get(url, headers=self.headers, params=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    def getMyOftenFlow(self):
        """

        :return:
        """
        url = f"{self.HOST}/runtime-api/runtime/instance/v1/getMyOftenFlow"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取当前登录人的组织
    def orgTree(self):
        """
        获取当前登录人的组织
        :return:
        """
        url = f"{self.HOST}/fund-api/fund/home/v1/orgTree"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取当前已过去的年月，包括当月
    def get_date(self):
        """
        获取当前已过去的年月，包括当月
        :return:
        """
        url = f"{self.HOST}/fund-api/fund/home/v1/date"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    def get_enterprise_info(self, keyWord):
        """
        获取企业信息
        :param keyWord:  企业名称，或者 企业信用代码
        :return:
        """
        url = f"{self.HOST}/product-api/tQua/v1/getEnterprise?keyWord={keyWord}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    def getOrgByUserId(self, uerId):
        """
        根据用户id,查询其所在分公司信息
        :param uerId:
        :return:
        """
        url = f"{self.HOST}/order-api/tOrderBusinessMainConfig/v1/getOrgByUserId?userId={uerId}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}


if __name__ == '__main__':
    login = LoginAPI()
    indata = {"username": "QY000341", "password": "123456"}
    userInfo = login.login(indata)

    userId = userInfo["userId"]
    token = userInfo["token"]
    
    common = CommonAPI(token)

    # resp = common.getRolesByUser("QY000341")
    # resp = common.getDetailByAccountOrId("QY000341")
    # print(resp)

    # resp = common.getCurrentUserMethodAuth()
    # nodeKey = visit_type

    # 查询字典
    # indata = {
    #     # "nodeKey": "new_timeout"
    #     "nodeKey": "visit_type"
    # }
    # resp = common.getFormatDics(indata)

    # resp = common.querySubUser("李儿啊")
    # indata = {"menuAlias": "front_menu"}
    # resp = common.getCurrentUserMenu(indata)

    # 获取新闻公告菜单
    # resps = common.getNewsTree()
    # # 获取新闻公告菜单里具体菜单的新闻
    # classId = resps[0]["id"]
    # resp = common.getNewsByClassfyId(classId)

    # resp = common.getMyOftenFlow()

    # resp = common.get_date()

    # 创建客户时获取企业信息
    # resp = common.get_enterprise_info("91110000710921189P")
    #
    # pprint(resp)
    # 获取用户userId
    resp = common.getOrgByUserId(userId)
    print(resp)
