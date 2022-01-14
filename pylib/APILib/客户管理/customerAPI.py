#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/18 15:16
# @File : customerAPI.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : customerAPI 客户管理接口
import copy
from pprint import pprint

import requests

from pylib.APILib.baseAPI import BaseAPI
from pylib.APILib.commonAPI import CommonAPI
from pylib.APILib.loginAPI import LoginAPI
from pylib.APILib.客户管理.clueAPI import ClueAPI
from utils.string_tools import get_phone_num, create_customerInfo_dict


class CustomerAPI(BaseAPI):

    # 我的客户列表
    def customer_list(self, inData=None, **kwargs):
        """
        我的客户列表
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/list/myself"
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中customer_list的内容
            # 使用深拷贝，避免data与self.conf["customer_list"]共用内存地址
            data = copy.deepcopy(self.conf["customer_list"])
            if bool(data):
                # 直接对比，是否有传递page和pageSize参数，有就赋值，没有就使用默认值
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                # 按照指定字段进行排序，没传递参数时会报错，故没传递参数则移除排序参数
                if "property" in kwargs.keys() and "direction" in kwargs.keys():
                    data["sorter"][0]["property"] = kwargs["property"]
                    data["sorter"][0]["direction"] = kwargs["direction"]
                else:
                    data.pop("sorter")
                # 逐个核对key-value是否对应，对应则更新到字典data里
                if "value" in kwargs:
                    for one in data["querys"]:
                        one["value"] = kwargs["value"]
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data["params"].keys()]
                # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
                for onekey in params_keyslist:
                    if onekey in kwargs.keys():
                        data["params"][onekey] = kwargs[onekey]
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 客户移入公海
    def customer_moveTo_noMaster(self, custNos, inData=None, **kwargs):
        """
        我的客户移入公海
        :param custNos: 客户编号
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/moveto/noMaster"
        if bool(inData):
            payload = inData
        else:
            # 读取接口配置模板文件中customer_moveTo_noMaster的内容
            # 使用深拷贝，避免data与self.conf["customer_moveTo_noMaster"]共用内存
            data = copy.deepcopy(self.conf["customer_moveTo_noMaster"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data.update(kwargs)
            data["custNos"] = custNos
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 转移客户
    def transfer_customer(self, custNos, handover, inData=None, **kwargs):
        """
        转移客户
        :param custNos:  # 客户编号
        :param handover:  # 接收主体id
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/transfer"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中transfer_customer的内容
            # 使用深拷贝，避免data与self.conf["transfer_customer"]共用内存
            data = copy.deepcopy(self.conf["transfer_customer"])
            # 使用列表生成式，把接口模板配置文件中的某些key获取出来
            params_keyslist = [onekey for onekey in data.keys()]
            # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
            for onekey in params_keyslist:
                if onekey in kwargs.keys():
                    data[onekey] = kwargs[onekey]
            data["custNos"] = custNos
            data["handover"] = handover
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 写(客户)跟进
    def write_customer_follow_up(self, fkId, inData=None, **kwargs):
        """
        客户写跟进
        :param fkId: 客户编号
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/custFollowUp"
        if inData:
            inData["fkId"] = fkId
            payload = inData
        else:
            # 读取接口配置模板文件中write_customer_follow_up的内容
            # 使用深拷贝，避免data与self.conf["write_customer_follow_up"]共用内存
            data = copy.deepcopy(self.conf["write_customer_follow_up"])
            # 使用列表生成式，把接口模板配置文件中的某些key获取出来
            params_keyslist = [onekey for onekey in data.keys()]
            # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
            for onekey in params_keyslist:
                if onekey in kwargs.keys():
                    data[onekey] = kwargs[onekey]
            data["fkId"] = fkId
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 创建客户
    def create_customer(self, inData=None, **kwargs):
        """
        创建客户
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/save/normal"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中create_cystomer的内容
            # 使用深拷贝，避免data与self.conf["create_cystomer"]共用内存
            data = copy.deepcopy(self.conf["create_cystomer"])
            # 使用列表生成式，把接口模板配置文件中的某些key获取出来
            params_keyslist = [onekey for onekey in data.keys()]
            # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
            for onekey in params_keyslist:
                if onekey in kwargs.keys():
                    data[onekey] = kwargs[onekey]
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 编辑客户
    def edit_customer(self, custNo, customerValue, inData=None, **kwargs):
        """
        编辑客户,不改客户来源。先获取原来的客户信息，用来替换模板中的数据，kwargs传递需要更新的参数
        :param custNo:          客户编号
        :param customerValue:    客户原来的信息
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/save/enterprise"
        # 读取接口配置模板文件中edit_customer的内容
        # 使用深拷贝，避免data与self.conf["edit_customer"]共用内存
        data = copy.deepcopy(self.conf["edit_customer"])
        # 遍历对比原来的客户信息，替换模板上的字段信息
        for onekey in data.keys():
            if onekey in customerValue.keys():
                if customerValue[onekey] != "" or customerValue[onekey] is not None:
                    data[onekey] = customerValue[onekey]
        # 如果参数以inData方式传入，则直接使用inData参数
        if inData:
            inData["custNo"] = custNo
            payload = inData
        # 否则使用模板数据
        else:
            # 使用列表生成式，把data字典中的key获取出来
            params_keyslist = [onekey for onekey in data.keys()]
            # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
            for onekey in params_keyslist:
                if onekey in kwargs.keys():
                    data[onekey] = kwargs[onekey]
            data["custNo"] = custNo
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 导出我的客户
    def export_customers(self, isSensitive=False, custNos=None, inData=None, **kwargs):
        """
        导出我的客户
        :param isSensitive: 是否脱敏导出，False不脱敏，True 脱敏
        :param custNos: 客户编号，多个时用逗号分隔，不传则导出全部
        :param inData: 如果传入inData，则优先使用inData参数
        :param kwargs: 如果传入kwargs，不传inDate,则优先使用inData参数
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/exportCusts"
        # inData 如果有传递参数，则使用该参数请求接口
        if inData:
            payload = inData
        # kwargs 如果有传递参数，则把参数更新
        else:
            # 读取接口配置模板文件中export_customers的内容
            # 使用深拷贝，避免data与self.conf["export_customers"]共用内存
            data = copy.deepcopy(self.conf["export_customers"])
            params_keyslist = [onekey for onekey in data["params"].keys()]
            # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
            for onekey in params_keyslist:
                if onekey in kwargs.keys():
                    data["params"][onekey] = kwargs[onekey]

            # custNos 有数据，则传递该参数。没有则不传递
            if custNos:
                data["params"]["isSensitive"] = isSensitive
                data["params"]["custNos"] = custNos
            else:
                data["params"]["isSensitive"] = isSensitive
                data["params"].pop("custNos")
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            # 导出数据到指定文件
            with open("../../../data/我的客户.xls", "wb") as code:
                code.write(resp.content)
                return {"state_code": 200, "state": True, "message": "OK,导出成功"}
        elif resp.status_code in [500, 403]:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 客户详情-基本信息
    def customer_details(self, custNo):
        """
        客户详情-基本信息
        :param custNo:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/getCustByAuth?custNo={custNo}&type=myself"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 客户联系人信息
    def customer_contact_info(self, custNo):
        """
         获取客户联系人信息
        :param custNo:  客户编号
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tContact/v1/getByCustNo/{custNo}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 添加联系人
    def add_contacts(self, customerNo, inData=None, **kwargs):
        """
        添加联系人/编辑联系人，kwargs中有id和contactNum这两个字段才是编辑联系人
        :param customerNo: 客户编号
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tContact/v1/saveByCust/{customerNo}"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中add_contacts的内容
            # 使用深拷贝，避免data与self.conf["add_contacts"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["add_contacts"])[0]
            if bool(data):
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data.keys()]
                # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
                for onekey in params_keyslist:
                    if onekey in kwargs.keys():
                        data[onekey] = kwargs[onekey]
                # kwargs中没有这两个参数,则为添加新的联系人，从字典中移除
                if "id" not in kwargs.keys() and "contactNum" not in kwargs.keys():
                    data.pop("id")
                    data.pop("contactNum")
                # # 判断此时的phone字段内容是否为列表：是则不处理，否则嵌套到列表中
                # if not isinstance(data["phones"], list):
                #     data["phones"] = [data["phones"]]
            # 传递的参数为列表，故需要把字典添加到列表中
            payload = [data]
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code in [200, 500, 403]:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 设置为主联系人
    def set_primary_contact(self, contactNum):
        """
        设置为主联系人
        :param contactNum:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tContact/v1/converMajor/{contactNum}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code in [200, 500, 403]:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 删除联系人
    def delete_contact(self, contactNum):
        """
        删除联系人
        :param contactNum:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tContact/v1/delete/{contactNum}"
        resp = requests.get(url, headers=self.headers)
        if resp.status_code in [200, 500, 403]:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 客户跟进记录
    def get_customer_followup_record(self, fkId, inData=None, **kwargs):
        """
        跟进记录
        :param inData:
            {
             "params":{"fkId":"1464132832069816320","type":2},
             "pageBean":{"page":1,"pageSize":10}
             }
        :param fkId:
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tTaskFllow/v1/querysBusi"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_customer_followup_record的内容
            # 使用深拷贝，避免data与self.conf["get_customer_followup_record"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["get_customer_followup_record"])
            if bool(data):
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                data["params"]["fkId"] = fkId
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取企业资料/客户资料
    def get_enterprise_info(self, businessId, businessCategory="01", inData=None):
        """
        获取企业资料、客户资料
        :param businessId:  # 客户id
        :param businessCategory:   # 01 客户资料；02企业资料
        :param inData:
        :return:
        """
        url = f"{self.HOST}/file-api/common/tFileBusiness/v1/getBusiFile"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_enterprise_info的内容
            # 使用深拷贝，避免data与self.conf["get_enterprise_info"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["get_enterprise_info"])
            data["businessId"] = businessId
            data["businessCategory"] = businessCategory
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取商机管理
    def get_opportunity_manager(self, customerNo, inData=None, **kwargs):
        """
        获取商机管理
        :param customerNo:  客户编号
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/tQuotedPrice/v1/queryList"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_opportunity_manager的内容
            # 使用深拷贝，避免data与self.conf["get_opportunity_manager"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["get_opportunity_manager"])
            if bool(data):
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                data["params"]["customerNo"] = customerNo
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取订单
    def get_orders(self, customerNo, inData=None, **kwargs):
        """
        获取订单
        :param customerNo:  客户编号
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/order-api/tOrder/v1/queryVo"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_orders的内容
            # 使用深拷贝，避免data与self.conf["get_orders"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["get_orders"])
            if bool(data):
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                data["params"]["customerNo"] = customerNo
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 待办任务
    def to_do_tasks(self, objectId, inData=None, **kwargs):
        """
        待办任务
        :param objectId:
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/tTaskCenter/v1/query"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中to_do_tasks的内容
            # 使用深拷贝，避免data与self.conf["to_do_tasks"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["to_do_tasks"])
            if bool(data):
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data["params"].keys()]
                # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
                for onekey in params_keyslist:
                    if onekey in kwargs.keys():
                        data["params"][onekey] = kwargs[onekey]
                data["params"]["objectId"] = objectId
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        # if resp.status_code == 200 or resp.status_code == 500 or resp.status_code == 403:
        if resp.status_code in [200, 500, 403]:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 创建（客户跟进）任务
    def create_task(self, custNosList, inData=None, **kwargs):
        """
        创建（客户跟进）任务
        :param custNosList: 列表类型数据,如["id1","id2"]
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/tTaskCenter/v1/saveOrUpdate"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中create_task的内容
            # 使用深拷贝，避免data与self.conf["create_task"]共用内存
            data = copy.deepcopy(self.conf["create_task"])
            params_keyslist = [onekey for onekey in data.keys()]
            # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
            for onekey in params_keyslist:
                if onekey in kwargs.keys():
                    data[onekey] = kwargs[onekey]
            data["ids"] = custNosList
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 公海客户列表
    def customer_noMaster_list(self, inData=None, **kwargs):
        """
        公海线索列表
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/list/noMaster"
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中customer_noMaster_list的内容
            # 使用深拷贝，避免data与self.conf["customer_noMaster_list"]共用内存地址
            data = copy.deepcopy(self.conf["customer_noMaster_list"])
            if bool(data):
                # 直接对比，是否有传递page和pageSize参数，有就赋值，没有就使用默认值
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                # 逐个核对key-value是否对应，对应则更新到字典data里
                if "value" in kwargs:
                    for one in data["querys"]:
                        one["value"] = kwargs["value"]
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data["params"].keys()]
                # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
                for onekey in params_keyslist:
                    if onekey in kwargs.keys():
                        data["params"][onekey] = kwargs[onekey]
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 公海客户列表-重新指派(客户)
    def reassign_customer(self, custNos, handover, inData=None):
        """
        公海客户列表-重新指派(客户)
        :param custNos:  客户编号，多个时："id1,id2"
        :param handover: 接受者id
        :param inData:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tCustomer/v1/transfer"
        if inData:
            payload = inData
        else:
            data = {"custNos": custNos, "handover": handover}
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}




if __name__ == '__main__':
    login = LoginAPI()
    indata = {"username": "QY000311", "password": "123456"}
    userInfo = login.login(indata)
    userId = userInfo["userId"]
    token = userInfo["token"]
    customerApi = CustomerAPI(token)
    # =====================我的客户列表===================
    # indata = {
    #     "pageBean": {"page": 1, "pageSize": 50, "total": 150},
    #     "params": {
    #         "followOrg": "", "dealState": "", "intentionToGrade": "", "custType": "",
    #         "handover": {"id": "", "value": ""}, "followUp": ""}}

    # resp = customerApi.customer_list(inData=indata)
    # resp = customerApi.customer_list(direction="DESC", property="lastFollowTime")
    # ===================客户移入公海===============
    # custNo = customerApi.customer_list(pageSize=2)["value"]["rows"][0]["custNo"]
    # # resp1 = customerApi.customer_moveTo_noMaster(custNos=custNo)
    # # ======================转移客户====================
    # commonApi = CommonAPI(token)
    # userID = commonApi.querySubUser("李振辉")["rows"][0]["id"]
    # resp1 = customerApi.transfer_customer(custNos=custNo, handover=userID)
    # pprint(resp1)
    # ==================创建客户 ================================
    commom = CommonAPI(token)
    enterprise_info = commom.get_enterprise_info("91110000710921189P")["value"][0]
    phone = get_phone_num()
    followCompany = commom.getOrgByUserId(userId)['value'][0]['id']

    clueApi = ClueAPI(token)
    clueNo = clueApi.get_myself_clue()["value"]["rows"][0]["clueNo"]

    customerInfo = create_customerInfo_dict(clueNo=clueNo, followCompany=followCompany)
    resp = customerApi.create_customer(customerInfo)
    pprint(resp)
    # # ============= 导出我的客户 ===================
    # resp = customerApi.export_customers(True)
    # print(resp)

    # ============ 查看客户详情-基本信息=====
    lists = customerApi.customer_list()
    custNo = lists["value"]["rows"][0]["custNo"]
    # print(custNo)
    customerInfo = customerApi.customer_details(custNo)

    customerValue = customerInfo["value"]
    pprint(customerValue)
    resp = customerApi.edit_customer(custNo, customerValue,
                                     remark="这是短短的备注信息1",
                                     intentionToGrade="B")
    pprint(resp)

    # # =========获取客户详情-添加联系人=========
    # lists = customerApi.customer_list()
    # custNo = lists["value"]["rows"][0]["custNo"]
    # # print(custNo)
    # customerInfo = customerApi.add_contacts(custNo, pageSize=20)
    # pprint(customerInfo)

    # # ============ 查看客户详情-客户联系人=====
    # lists = customerApi.customer_list()
    # custNo = lists["value"]["rows"][0]["custNo"]
    # # print(custNo)
    # customerInfo = customerApi.customer_contact_info(custNo)
    # pprint(f'联系人个数：{len(customerInfo["value"])}')
    # contactNum = customerInfo["value"][0]["contactNum"]
    # # print(contactNum)

    # # 设为主联系人
    # info = customerApi.set_primary_contact(contactNum)
    # print(info)

    # # 删除联系人
    # info = customerApi.delete_contact(contactNum)
    # print(info)

    # # ============ 查看客户详情-跟进记录=====
    # lists = customerApi.customer_list()
    # custNo = lists["value"]["rows"][0]["custNo"]
    # # print(custNo)
    # customerInfo = customerApi.get_followup_record(custNo)
    # pprint(customerInfo)

    # # ============ 查看客户详情-企业资料=====
    # lists = customerApi.customer_list()
    # custNo = lists["value"]["rows"][0]["custNo"]
    # print(custNo)
    # customerInfo = customerApi.get_enterprise_info(custNo, "02")
    # pprint(customerInfo)

    # # ============ 查看客户详情-商机管理=====
    # lists = customerApi.customer_list()
    # custNo = lists["value"]["rows"][0]["custNo"]
    # # print(custNo)
    # customerInfo = customerApi.get_opportunity_manager(custNo, pageSize=20)
    # pprint(customerInfo)

    #   ============ 查看客户详情-商机管理=====

    # # =========获取客户详情-订单=========
    # lists = customerApi.customer_list()
    # custNo = lists["value"]["rows"][0]["custNo"]
    # # print(custNo)
    # customerInfo = customerApi.get_orders(custNo, pageSize=20)
    # pprint(customerInfo)

    # # =========获取客户详情-待办任务=========
    #     lists = customerApi.customer_list()
    #     custNo = lists["value"]["rows"][0]["custNo"]
    #     # print(custNo)
    #     customerInfo = customerApi.to_do_tasks(custNo, pageSize=20)
    #     pprint(customerInfo)
