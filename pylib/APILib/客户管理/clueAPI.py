#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/4 16:37
# @File : clueAPI.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import json
from pprint import pprint

import requests
import copy

from pylib.APILib.baseAPI import BaseAPI
from pylib.APILib.loginAPI import LoginAPI


class ClueAPI(BaseAPI):

    # 获取我的线索列表
    def get_myself_clue(self, inData=None, **kwargs):
        """
        获取我的线索
        :param inData:
        :param kwargs: 以key-value的形式传参
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/myself"
        # 如果直接传递参数inData,则不使用模板进行创建，两个都传inData生效
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中get_myself_clue的内容
            # 使用深拷贝，避免data与self.conf["get_myself_clue"]共用内存地址
            data = copy.deepcopy(self.conf["get_myself_clue"])
            # 判断data字典是否为空，不为空则执行下面的语句，为空则跳过
            if bool(data):
                # 直接update更新字典里的数据
                # data.update(kwargs)
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data["params"].keys()]
                # 逐个核对key-value是否对应，对应则更新到字典data里
                if "value" in kwargs:
                    for one in data["querys"]:
                        one["value"] = kwargs["value"]
                # 直接对比，是否有传递page和pageSize参数，有就赋值，没有就使用默认值
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
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

    # 保存线索
    def save_clue(self, inData=None, **kwargs):
        """
        保存线索，包括创建线索，更新修改线索
        :param kwargs:
        :param inData:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/save"
        # 如果直接传递参数inData,则不使用模板进行创建，两个都传inData生效
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中save_clue的内容
            # 使用深拷贝，避免data与self.conf["save_clue"]共用内存地址
            data = copy.deepcopy(self.conf["save_clue"])
            # 判断data字典是否为空，不为空则执行下面的语句，为空则跳过
            if bool(data):
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data.keys()]
                # 把字典类型的参数更新到data中
                # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
                for onekey in params_keyslist:
                    if onekey in kwargs.keys():
                        data[onekey] = kwargs[onekey]
            # 如果kwargs中没有clueNo参数，则为创建线索，不需要传递clueNo参数，故从字典移除clueNo
            if "clueNo" not in kwargs.keys():
                data.pop("clueNo")
            # 如果kwargs中没有clueTab,则不传递clueTab字段
            if "clueTab" not in kwargs.keys():
                data.pop("clueTab")
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 转移线索
    def transfer_clue(self, inDate=None, **kwargs):
        """
        转移线索,
        :param inDate: {clueNos: "XS2472631", transferTo: "1407876697361092608"}
            clueNos:线索id,   有多个线索id则用逗号分隔，如："XS2472631,XS2472632"
            transferTo:接收者id
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/transfer"
        if inDate:
            payload = inDate
        else:
            # 读取接口配置模板文件中transfer_clue的内容
            # 使用深拷贝，避免data与self.conf["transfer_clue"]共用内存
            data = copy.deepcopy(self.conf["transfer_clue"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data.update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 移入公海线索
    def move_to_noMaster(self, inData=None, **kwargs):
        """
        移入公海线索
        :param inData: {clueNos: "XS2471253"}
         clueNos:线索id,   有多个线索id则用逗号分隔，如："XS2472631,XS2472632"
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/moveto/noMaster"
        if bool(inData):
            payload = inData
        else:
            # 读取接口配置模板文件中move_to_noMaster的内容
            # 使用深拷贝，避免data与self.conf["move_to_noMaster"]共用内存
            data = copy.deepcopy(self.conf["move_to_noMaster"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data.update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 移入无效线索
    def move_to_invalid(self, inData=None, **kwargs):
        """
        移入无效线索
        :param inData:{clueNos: "XS2471241", remark: "无效的联系方式"}
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/moveto/invalid"
        if bool(inData):
            payload = inData
        else:
            # 读取接口配置模板文件中move_to_invalid的内容
            # 使用深拷贝，避免data与self.conf["move_to_invalid"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["move_to_invalid"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data.update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 导出线索
    def exportClues(self, inData=None, **kwargs):
        """
        导出线索,保存成Excel文件
        :param inData:
            {"params":{
                    "isSensitive":true,
                    "clueNos":"XS2471395,XS2471247"
                    }
            }
            isSensitive: ture 脱敏导出; false 正常导出
            clueNos：没有这个参数字段为全部导出，有参数并且有值就是导出指定值的
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/exportClues"
        if bool(inData):
            payload = inData
        else:
            # 读取接口配置模板文件中self.conf["exportClues"]的内容
            # 使用深拷贝，避免data与self.conf["exportClues"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["exportClues"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data["params"].update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200:
            with open("../../../data/我的线索.xls", "wb") as code:
                code.write(resp.content)
                return {"state_code": 200, "state": True, "message": "OK,导出成功"}
        elif resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 获取我的线索详情基本信息
    def getClueByAuth(self, inData=None, **kwargs):
        """
        获取我的线索详情基本信息
        :param inData: {
            "clueNo": clueNo,
            "type": "myself"
        }
        clueNo：线索id
        type:线索类型，myself：我的线索； extension：推广线索
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/getClueByAuth?"
        if bool(inData):
            payload = inData
        else:
            # 读取接口配置模板文件中getClueByAuth的内容
            # 使用深拷贝，避免data与self.conf["getClueByAuth"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["getClueByAuth"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data
                data.update(kwargs)
            payload = data
        resp = requests.get(url, headers=self.headers, params=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # (线索)跟进记录
    def get_followup_record(self, fkId, inData=None, **kwargs):
        """
        跟进记录
        :param inData:
            {
             "params":{"fkId":"1464132832069816320","type":1},
             "pageBean":{"page":1,"pageSize":10}
             }
        :param fkId:  线索id
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tTaskFllow/v1/querysBusi"
        if inData:
            inData["params"] = {"fkId": fkId, "type": 1}
            payload = inData
        else:
            # 读取接口配置模板文件中get_followup_record的内容
            # 使用深拷贝，避免data与self.conf["get_followup_record"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["get_followup_record"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data["pageBean"].update(kwargs)
            # 把fkId赋值到模板里的fkId中
            data["params"]["fkId"] = fkId
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # (线索)操作记录
    def get_operation_record(self, fkId, inData=None, **kwargs):
        """
        获取线索操作记录
        :param fkId: 线索id
        :param inData: {"pageBean":{"page":1,"pageSize":50}}
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/file-api/common/tOperationLog/v1/list/{fkId}"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_operation_record的内容
            # 使用深拷贝，避免data与self.conf["get_operation_record"]共用内存地址导致更改数据
            data = copy.deepcopy(self.conf["get_operation_record"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data["pageBean"].update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # （线索）写跟进
    def create_FollowUp(self, fkId, remark, nextFollowTime, inData=None, **kwargs):
        """
        写跟进
        :param nextFollowTime:
        :param remark:
        :param fkId:
        :param inData:
            {
            "type":"1",
            "nextFollowTime":"2021-11-27 00:00:00",
            "remark":"这是跟进内容",
            "nextRemark":"这是下次跟进备注",
            "clueTag":["20"],
            "isMeet":true,
            "taskType":1,
            "fkId":"1464132832069816320",
            "taskTitle":"线索跟进"
            }
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tTaskFllow/v1/create"
        if inData:
            inData["fkId"] = fkId
            inData["remark"] = remark
            inData["nextFollowTime"] = nextFollowTime
            payload = inData
        else:
            data = copy.deepcopy(self.conf["create_FollowUp"])
            if bool(data):
                data.update(kwargs)
            data["fkId"] = fkId
            data["remark"] = remark
            data["nextFollowTime"] = nextFollowTime
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 加入我的线索
    def move_to_myself(self, inData=None, **kwargs):
        """
        加入我的线索
        :param inData:  {clueNos: "1432606797323177984,1431440053799882752"}
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/moveto/myself"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中move_to_myself的内容
            # 使用深拷贝，避免data与self.conf["move_to_myself"]共用内存
            data = copy.deepcopy(self.conf["move_to_myself"])
            if bool(data):
                # 把字典类型的参数kwargs更新到data中
                data.update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 公海线索列表
    def get_noMaster(self, inData=None, **kwargs):
        """
        公海线索列表
        :param inData:
        {
        "pageBean":{"page":1,"pageSize":50},
        "querys":[
            {"property":"person","value":"刘连玲","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"phone","value":"刘连玲","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"telephone","value":"刘连玲","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"wx","value":"刘连玲","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"qq","value":"刘连玲","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"email","value":"刘连玲","group":"quick","relation":"OR","operation":"LIKE"}],
        "params":{"clueType":"","clueTag":"","province":"","city":"","areas":""}
        }
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/noMaster"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_noMaster的内容
            # 使用深拷贝，避免data与self.conf["get_noMaster"]共用内存
            data = copy.deepcopy(self.conf["get_noMaster"])
            if bool(data):
                if "value" in kwargs:
                    for one in data["querys"]:
                        one["value"] = kwargs["value"]
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
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 无效线索列表
    def get_invalid(self, inData=None, **kwargs):
        """
        无效线索列表
        :param inData:
        {
        "pageBean":{"page":1,"pageSize":50},
        "querys":[
            {"property":"person","value":"赵福茹","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"phone","value":"赵福茹","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"telephone","value":"赵福茹","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"wx","value":"赵福茹","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"qq","value":"赵福茹","group":"quick","relation":"OR","operation":"LIKE"},
            {"property":"email","value":"赵福茹","group":"quick","relation":"OR","operation":"LIKE"}],
        "params":{"clueTag":"","province":"340000","city":"","areas":""}
        }
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/invalid"
        if inData:
            payload = inData
        else:
            # 读取接口配置模板文件中get_invalid的内容
            # 使用深拷贝，避免data与self.conf["get_invalid"]共用内存
            data = copy.deepcopy(self.conf["get_invalid"])
            if bool(data):
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data["params"].keys()]
                if "value" in kwargs:
                    for one in data["querys"]:
                        one["value"] = kwargs["value"]
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
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

    # 推广线索列表
    def get_extension(self, inData=None, **kwargs):
        """
        推广线索列表
        :param inData:
        {"pageBean": {"page": 1, "pageSize": 50}, "querys": [
        {"property": "person", "value": "", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "phone", "value": "", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "telephone", "value": "", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "wx", "value": "", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "qq", "value": "", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "email", "value": "", "group": "quick", "relation": "OR", "operation": "LIKE"}],
         "params": {"clueTag": "", "clueState": "", "followOrg": "", "followCompany": "",
                    "province": "", "city": "", "areas": "", "followBy": ""}}
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/extension"
        # 如果直接传递参数inData,则不使用模板进行创建，两个都传inData生效
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中get_extension的内容
            # 使用深拷贝，避免data与self.conf["get_extension"]共用内存地址
            data = copy.deepcopy(self.conf["get_extension"])
            # 判断data字典是否为空，不为空则执行下面的语句，为空则跳过
            if bool(data):
                # 使用列表生成式，把接口模板配置文件中的某些key获取出来
                params_keyslist = [onekey for onekey in data["params"].keys()]
                # 逐个核对key-value是否对应，对应则更新到字典data里
                if "value" in kwargs.keys():
                    for one in data["querys"]:
                        one["value"] = kwargs["value"]
                # 直接对比，是否有传递page和pageSize参数，有就赋值，没有就使用默认值
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
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

    # 推广线索分配到分公司
    def allot_clue(self, inData=None, **kwargs):
        """
        推广线索分配到分公司
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/allot/org"
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中allot_clue的内容
            # 使用深拷贝，避免data与self.conf["allot_clue"]共用内存地址
            data = copy.deepcopy(self.conf["allot_clue"])
            if bool(data):
                data.update(kwargs)
                # if "clueNos" in kwargs.keys():
                #     data["clueNos"] = kwargs["clueNos"]
                # if "allotTo" in kwargs.keys():
                #     data["allotTo"] = kwargs["allotTo"]
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 推广线索分配到人
    def allot_clue_to_user(self, inData=None, **kwargs):
        """
        推广线索分配到用户
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/allot/user"
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中allot_clue_to_user的内容
            # 使用深拷贝，避免data与self.conf["allot_clue_to_user"]共用内存地址
            data = copy.deepcopy(self.conf["allot_clue_to_user"])
            if bool(data):
                data.update(kwargs)
            payload = data
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 批量导入推广线索
    def import_extension(self, filePath):
        """
        批量导入推广线索
        :param filePath: 文件路径
        :return:
        """
        files = {
            "file": open(filePath, "rb"),
            # 'Content-Disposition': 'form-data',
            # "Content-Type": "application/vnd.ms-excel",
            # "filename": "线索导入模板.xls"
        }
        # 注意：切记header头信息中不要添加Content-Type：xxxxxxx 这个字段，
        # 添加之后在发起请求的时候有可能找不到文件，所以暂时去掉这个字段，
        # 请求完成后再加回来
        Content_Type = self.headers.pop("Content-Type")
        url = f"{self.HOST}/crm-api/crm/clue/v1/import"
        resp = requests.post(url, files=files, headers=self.headers)
        # 恢复为原来的格式
        self.headers["Content-Type"] = Content_Type
        if resp.status_code == 200:
            # resp.json()["state"]=False 就意味着导入有失败的,取反
            if not resp.json()["state"]:
                fileId = resp.json()["value"]
                self.clue_downloadFile(fileId)
                return {"retcode": 9998, "message": "线索导入异常！详情查看【线索导入异常情况.xls】文件"}
            return resp.json()
        elif resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}

    # 线索导入异常时，下载异常文件
    def clue_downloadFile(self, filedId):
        """
        1、线索导入异常时，下载异常文件
        2、下载线索导入模板
        :param filedId:
        :return:
        """
        url = f"{self.HOST}/portal-api/system/file/v1/downloadFile?fileId={filedId}"
        resp = requests.get(url, headers=self.headers)
        # with open("../../../data/线索导入异常情况.xls", "wb") as code:
        with open("data/线索导入异常情况.xls", "wb") as code:
            code.write(resp.content)
            return {"OK"}

    # 线索审核列表
    def clue_review(self, inData=None, **kwargs):
        """
        线索审核列表
        :param inData:
        :param kwargs:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/queryExamine"
        # 如果直接传递indata,则不使用模板进行查询，两个都传递，则inData生效
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中clue_review的内容
            # 使用深拷贝，避免data与self.conf["clue_review"]共用内存
            data = copy.deepcopy(self.conf["clue_review"])
            # 判断data字段是否为空，不为空则执行下面的语句，为空则跳过
            if bool(data):
                if "page" in kwargs.keys():
                    data["pageBean"]["page"] = kwargs["page"]
                if "pageSize" in kwargs.keys():
                    data["pageBean"]["pageSize"] = kwargs["pageSize"]
                if "value" in kwargs.keys():
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

    # 线索审核
    def examine_clue(self, inData=None, **kwargs):
        """
        线索审核为有效或者无效
        # :param cule_id: 线索id
        # :param status: 线索状态：01 有效；02 无效
        :param inData:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/examineClue?"
        if inData:
            payload = inData
        else:
            # 读取接口模板配置文件中examine_clue的内容
            # 使用深拷贝，避免data与self.conf["examine_clue"]共用内存
            data = copy.deepcopy(self.conf["examine_clue"])
            # 判断data字段是否为空，不为空则执行下面的语句，为空则跳过
            if bool(data):
                # 直接把kwargs更新到data字典中，后果是所有传递的键值对都会被传递到请求中
                data.update(kwargs)
            payload = data
        resp = requests.get(url, headers=self.headers, params=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"retcode": 9999, "message": "接口报错！"}






if __name__ == '__main__':
    login = LoginAPI()
    indata = {"username": "QY000311", "password": "MTIzNDU2"}
    token = login.getToken(indata)
    clueAPI = ClueAPI(token)
    # ================ 获取我的线索 ==================
    pageBean = {'page': 1, 'pageSize': 1}
    resp = clueAPI.get_myself_clue()
    print(resp)
    # indata = {"pageBean": {"page": 1, "pageSize": 50},
    #           "params": {"clueTag": "", "clueState": "", "followOrg": "", "followBy": ""}}
    # resp = clueAPI.get_myself_clue(indata)

    # querys = [{"property": "person", "value": "联系人", "group": "quick", "relation": "OR", "operation": "LIKE"}]
    # resp = clueAPI.get_myself_clue(querys=querys)

    # =================== 保存线索 ================
    # resp = clueAPI.save_clue(phone=get_phone_num())
    # phone = get_phone_num()
    # resp = clueAPI.save_clue(person=f"联系人{phone}", phone=phone)

    # =================转移线索====================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 100, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.transfer_clue(clueNos=clueNo)
    # ===================移入公海线索==================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.move_to_noMaster(clueNos=clueNo)
    # ==================移入无效线索=======================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.move_to_invalid(clueNos=clueNo)
    # ===================导出我的线索==================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.exportClues(clueNos=clueNo, isSensitive=True)
    # =====================查看我的线索详情====================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.getClueByAuth(clueNo=clueNo)
    # =====================查看线索跟进记录======================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.get_followup_record(clueNo)
    # ======================查看我的线索操作记录=========================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.get_operation_record(clueNo, page=1, pageSize=1)
    # ======================(线索)写跟进=========================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.create_FollowUp(clueNo, "这是跟进备注", "2021-12-27 00:00:00")

    # ====================加入我的线索==================
    # clueNo = clueAPI.get_myself_clue(pageBean={'page': 1, 'pageSize': 1})["value"]["rows"][0]["clueNo"]
    # resp = clueAPI.move_to_myself()
    # ============== 获取公海线索 ===================
    # resp = clueAPI.get_noMaster(page=1, pageSize=5)
    # ============== 获取无效线索 ===================
    # resp = clueAPI.get_invalid(page=1, pageSize=5)

    # # ============== 获取推广线索列表 ===================
    # resp = clueAPI.get_extension(page=1, pageSize=5)
    # pprint(resp)

    # ==================== 获取线索审核列表 ===========
    # clue_id = clueAPI.clue_review()["value"]["rows"][0]["id"]
    # # clue_id = "31959ebf15d74fb8a5c9c86904cef08d"
    # # print(clue_id)
    # resp = clueAPI.examine_clue(id=clue_id)
    # pprint(resp)

