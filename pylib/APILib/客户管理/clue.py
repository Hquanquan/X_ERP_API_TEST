#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 14:28
# @File : clue.py
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : 线索管理API

from pprint import pprint

from pylib.APILib.baseAPI import BaseAPI
import requests

from pylib.APILib.commonAPI import CommonAPI
from pylib.APILib.loginAPI import LoginAPI


class ClueAPI(BaseAPI):
    """
    线索管理API
    """

    # 获取我的线索列表
    def get_myself(self, inDate):
        """
        获取我的线索
        :param inDate:
        {
            "pageBean":{"page":1,"pageSize":50,"total":1},
            "querys":[{"property":"person","value":"苏玉炎","group":"quick","relation":"OR","operation":"LIKE"},
                    {"property":"phone","value":"苏玉炎","group":"quick","relation":"OR","operation":"LIKE"},
                    {"property":"telephone","value":"苏玉炎","group":"quick","relation":"OR","operation":"LIKE"},
                    {"property":"wx","value":"苏玉炎","group":"quick","relation":"OR","operation":"LIKE"},
                    {"property":"qq","value":"苏玉炎","group":"quick","relation":"OR","operation":"LIKE"},
                    {"property":"email","value":"苏玉炎","group":"quick","relation":"OR","operation":"LIKE"}],
            "params":{"clueTag":"","clueState":"","followOrg":"","followBy":""}}
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/myself"
        payload = inDate
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 创建我的线索
    def save_clue(self, inDate):
        """
        创建线索,
        clueType=00:我的线索
        clueType=01:推广线索
        :param inDate:
        {
            "person":"联系人",
            "phone":"15623656985",
            "telephone":"88888888",
            "wx":"wx987654",
            "qq":"98765423",
            "email":"98765423@qq.com",
            "source":"tyc",     # 线索来源字段，创建我的线索填写
            "sourceChannel":"",    # 推广渠道，创建推广线索填写
            "intentionLevel":"",    #
            obtainTime: "2021-11-29",    # 获取线索时间，创建推广线索填写
            sourceAccount: "00"         # 推广线索来源户，创建推广线索填写
            "demandType":"",
            "demandRemark":"",
            "remark":"这是备注",
            "consultQua":"咨询资质",
            "clueType":"00",
            "province":"110000",
            "city":"110100",
            "areas":"110101"
        }
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/save"
        payload = inDate
        resp = requests.post(url, headers=self.headers, json=payload)
        if resp.status_code == 200 or resp.status_code == 500:
            return resp.json()
        else:
            return {"state": 9999, "message": "接口请求失败，未知服务错误！"}

    # 转移线索
    def transfer_clue(self, inDate):
        """
        转移线索,
        :param inDate: {clueNos: "XS2472631", transferTo: "1407876697361092608"}
            clueNos:线索id,   有多个线索id则用逗号分隔，如："XS2472631,XS2472632"
            transferTo:接收者id
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/transfer"
        payload = inDate
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 移入公海线索
    def move_to_noMaster(self, inData):
        """
        移入公海线索
        :param inData: {clueNos: "XS2471253"}
         clueNos:线索id,   有多个线索id则用逗号分隔，如："XS2472631,XS2472632"
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/moveto/noMaster"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 移入无效线索
    def move_to_invalid(self, inData):
        """
        移入无效线索
        :param inData:{clueNos: "XS2471241", remark: "无效的联系方式"}
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/moveto/invalid"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 导出线索
    def exportClues(self, inData):
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

        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/exportClues"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        with open("../../../data/我的线索.xls", "wb") as code:
            code.write(resp.content)
            return "OK"

    # 获取我的线索详情基本信息
    def getClueByAuth(self, inData):
        """
        获取我的线索详情基本信息
        :param inData: {
            "clueNo": clueNo,
            "type": "myself"
        }
        clueNo：线索id
        type:线索类型，myself：我的线索； extension：推广线索
        :return:
        """
        # http://192.168.1.25:8380/crm-api/crm/clue/v1/getClueByAuth?clueNo=1464132832069816320&type=myself
        url = f"{self.HOST}/crm-api/crm/clue/v1/getClueByAuth?"
        payload = inData
        resp = requests.get(url, headers=self.headers, params=payload)
        return resp.json()

    # 跟进记录
    def get_followup_record(self, fkId, inData):
        """
        跟进记录
        :param inData:
            {
             "params":{"fkId":"1464132832069816320","type":1},
             "pageBean":{"page":1,"pageSize":10}
             }

             {
             "params":{"fkId":"1464132832069816320","type":1},
             "pageBean":{"page":1,"pageSize":10}
             }

        :param fkId:  线索id
        :param inData:
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/tTaskFllow/v1/querysBusi"
        inData["params"] = {"fkId": fkId, "type": 1}
        payload = inData
        print(payload)
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # (线索)操作记录
    def get_operation_record(self, fkId, inData):
        """
        获取线索操作记录
        :param fkId: 线索id
        :param inData:
        {"pageBean":{"page":1,"pageSize":50}}
        :return:
        """
        url = f"{self.HOST}/file-api/common/tOperationLog/v1/list/{fkId}"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # （线索）写跟进
    def create_FollowUp(self, fkId, inData):
        """
        写跟进
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
        inData["fkId"] = fkId
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 加入我的线索
    def move_to_myself(self, inData):
        """
        加入我的线索
        :param inData: {clueNos: "1432606797323177984,1431440053799882752"}
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/moveto/myself"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 公海线索列表
    def get_noMaster(self, inData):
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
        "params":{"clueTag":"","province":"340000","city":"","areas":""}
        }
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/noMaster"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 无效线索列表
    def get_invalid(self, inData):
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
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 推广线索列表
    def get_extension(self, inData):
        """
        推广线索列表
        :param inData:
        {"pageBean": {"page": 1, "pageSize": 50}, "querys": [
        {"property": "person", "value": "15698656235", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "phone", "value": "15698656235", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "telephone", "value": "15698656235", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "wx", "value": "15698656235", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "qq", "value": "15698656235", "group": "quick", "relation": "OR", "operation": "LIKE"},
        {"property": "email", "value": "15698656235", "group": "quick", "relation": "OR", "operation": "LIKE"}],
         "params": {"clueTag": "", "clueState": "", "followOrg": "", "followCompany": "",
                    "province": "", "city": "", "areas": "", "followBy": ""}}
        :return:
        """
        url = f"{self.HOST}/crm-api/crm/clue/v1/list/extension"
        payload = inData
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

    # 推广线索分配到分公司
    def allot_clue(self, allotTo, clueNos):
        """

        :param allotTo: 分公司id
        :param clueNos: 线索id
        :return:
        """
        inData = {"clueNos": clueNos, "allotTo": allotTo}
        payload = inData
        url = f"{self.HOST}/crm-api/crm/clue/v1/allot/org"
        resp = requests.post(url, headers=self.headers, json=payload)
        return resp.json()

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
        Content_ype = self.headers.pop("Content-Type")
        url = f"{self.HOST}/crm-api/crm/clue/v1/import"
        resp = requests.post(url, files=files, headers=self.headers)
        # 恢复为原来的格式
        self.headers["Content-Type"] = Content_ype
        if resp.status_code == 200:
            # resp.json()["state"]=False 就意味着导入有失败的
            if not resp.json()["state"]:
                fileId = resp.json()["value"]
                self.clue_downloadFile(fileId)
                return "线索导入异常！详情查看【线索导入异常情况.xls】文件"
            return resp.json()
        elif resp.status_code == 502:
            return {"status_code":502,"msg":"服务重启中！稍后再试"}
        elif resp.status_code == 500:
            return {"status_code":500,"msg":"服务器发生不可预测的错误"}
        else:
            return {"status_code":9999,"msg":"请求失败！接口返回未知错误"}

    # 线索导入异常时，下载异常文件
    def clue_downloadFile(self, filedId):
        """
        线索导入异常时，下载异常文件
        :param filedId:
        :return:
        """
        url = f"{self.HOST}/portal-api/system/file/v1/downloadFile?fileId={filedId}"
        resp = requests.get(url, headers=self.headers)
        with open("../../../data/线索导入异常情况.xls", "wb") as code:
            code.write(resp.content)
            return "OK"


if __name__ == '__main__':
    login = LoginAPI()
    # # resp = login.login001("QY000341","MTIzNDU2")
    indata = {"username": "QY000215", "password": "MTIzNDU2"}
    # resp = login.login(indata)
    token = login.getToken(indata)
    common = CommonAPI(token)
    clue = ClueAPI(token)

    # 获取我的线索列表
    indata = {"pageBean": {"page": 0, "pageSize": 50},
              "params": {"clueTag": "", "clueState": "", "followOrg": "", "followBy": ""}}

    """
    # 创建我的线索
    indata = {
        "person": "联系人002",
        "phone": "15623656950",
        "telephone": "88888880",
        "wx": "wx987650",
        "qq": "98765420",
        "email": "98765420@qq.com",
        "source": "tyc",
        "sourceChannel": "",
        "intentionLevel": "",
        "demandType": "",
        "demandRemark": "",
        "remark": "这是备注0",
        "consultQua": "咨询资质0",
        "clueType": "00",
        "province": "110000",
        "city": "110100",
        "areas": "110101"
    }
    resp = clue.save_clue(indata)
    """
    # 获取第一条线索id
    clueNo = clue.get_myself(indata)["value"]["rows"][0]["clueNo"]
    # ============转移线索==========
    # 获取接收者id
    # transferId = common.querySubUser("杜连杰")["rows"][0]["id"]
    # indata = {"clueNos": clueNo, "transferTo": transferId}
    # resp = clue.transfer_clue(indata)
    # ============移入公海线索==============
    # indata = {"clueNos": clueNo}
    # resp = clue.move_to_noMaster(indata)
    # ============移入无效线索===============
    # indata = {"clueNos": clueNo, "remark": "无效的联系方式"}
    # resp = clue.move_to_invalid(indata)
    # ===============导出线索================
    # indata = {
    #     "params": {
    #         "isSensitive": "true",
    #         "clueNos": clueNo
    #     }
    # }
    # resp = clue.exportClues(indata)
    # indata = {"clueNo": clueNo, "type": "myself"}
    # resp = clue.getClueByAuth(indata)

    # 获取线索跟进记录
    # indata = {
    #     "pageBean": {"page": 1, "pageSize": 10}
    # }
    # resp = clue.get_followup_record(clueNo, indata)
    # =============== 线索跟进 ===========
    # indata = {
    #     "type": "1",
    #     "nextFollowTime": "2021-11-28 00:00:00",
    #     "remark": "这是跟进内容1",
    #     "nextRemark": "这是下次跟进备注1",
    #     "clueTag": ["20"],
    #     "isMeet": "true",
    #     "taskType": 1,
    #     "fkId": "1464132832069816320",
    #     "taskTitle": "线索跟进"
    # }
    # resp = clue.create_FollowUp(clueNo, indata)

    # indata = {"pageBean": {"page": 1, "pageSize": 50, "total": 0},
    #           "params": {"clueTag": ""}
    #           }

    # resp = clue.get_noMaster(indata)
    # resp = clue.get_invalid(indata)
    # indata = {"pageBean": {"page": 1, "pageSize": 10}}
    # # resp = clue.get_operation_record(clueNo, indata)
    #
    # resp = clue.get_extension(indata)
    # =============导入推广线索====================
    # filePath = r"../../../data/线索导入模板.xls"
    # resp = clue.import_extension(filePath)
    # pprint(resp)
