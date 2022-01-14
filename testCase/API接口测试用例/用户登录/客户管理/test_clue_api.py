#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/2 16:48
# @File : test_clue_api.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : ClueAPI线索管理接口测试
import allure
import pytest

from utils.excel_tools import get_ExcelDataByCaseName
from utils.string_tools import create_clueInfo_dict
from utils.time_tools import get_timeString


@allure.epic("X-ERP系统接口测试")
@allure.feature("客户管理-ClueAPI线索管理接口测试")
class TestClueAPI:

    # @pytest.mark.skip("暂不运行")
    @allure.story("线索管理-我的线索列表")
    @allure.title("{title}")
    @pytest.mark.list_myself
    # inData 请求体参数  expectedData 预期结果数据（不准确，暂时不使用） title 用例标题
    @pytest.mark.parametrize("inData,expectedData,title", get_ExcelDataByCaseName("线索管理", "list_myself_clue"))
    def test_get_myself_clue(self, inData, expectedData, title, initClueApi):
        allure.dynamic.description(f"我的线索列表：{title}")
        clueApi = initClueApi
        resp = clueApi.get_myself_clue(inData)
        # 线索数据在列表中，列表不为0，则断言通过
        assert len(resp["value"]["rows"]) != 0

    @pytest.mark.add_myselfClue
    @allure.story("线索管理-我的线索列表")
    @allure.title("创建我的线索")
    def test_add_myself_clue(self, initClueApi):
        clueApi = initClueApi
        clueInfo = create_clueInfo_dict()
        resp = clueApi.save_clue(clueInfo)
        assert resp['message'] == "操作成功"

    @pytest.fixture()
    def before_test_find_myself_clue(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        yield
        self.clueAPI.move_to_noMaster(clueNos=self.resp["value"])

    @allure.story("线索管理-我的线索列表")
    @allure.title("按联系人名字查询我的线索")
    @pytest.mark.find_myself_clue
    def test_find_myself_clue(self, before_test_find_myself_clue):
        resp = self.clueAPI.get_myself_clue(value=self.clueInfo["person"])
        assert resp["value"]["rows"][0]["person"] == self.clueInfo["person"]

    @allure.story("线索管理-我的线索列表")
    @allure.title("单个线索移入公海")
    @pytest.mark.move_to_noMaster
    def test_move_myself_clue_to_noMaster(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        # 把我的线索移入公海
        resp1 = self.clueAPI.move_to_noMaster(clueNos=self.resp["value"])
        resp2 = self.clueAPI.get_noMaster(value=self.clueInfo["person"])
        assert "操作成功" in resp1["message"] and resp2["value"]["rows"][0]["person"] == self.clueInfo["person"]

    @allure.story("线索管理-我的线索列表")
    @allure.title("单个线索移入无效")
    @pytest.mark.move_to_invalid
    def test_move_myself_clue_to_invalid(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        # 把我的线索移入无效
        resp1 = self.clueAPI.move_to_invalid(clueNos=self.resp["value"])
        resp2 = self.clueAPI.get_invalid(value=self.clueInfo["person"])
        assert "操作成功" in resp1["message"] and resp2["value"]["rows"][0]["person"] == self.clueInfo["person"]

    @pytest.fixture()
    def before_test_create_FollowUp(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        yield
        # 把我的线索移入无效
        resp = self.clueAPI.move_to_invalid(clueNos=self.resp["value"])

    @allure.story("线索管理-我的线索列表")
    @allure.title("(线索)写跟进")
    @pytest.mark.create_FollowUp
    def test_create_FollowUp(self, before_test_create_FollowUp):
        fkid = self.resp["value"]
        resp1 = self.clueAPI.create_FollowUp(fkid, "这是跟进线索内容", get_timeString(tomorrow=True))
        resp2 = self.clueAPI.get_followup_record(fkid)
        assert resp1["state"] is True and resp2["value"]["rows"][0]["remark"] == "这是跟进线索内容"

    @pytest.fixture()
    def before_test_getClueByAuth(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        self.clueNos = self.resp["value"]
        yield
        # 把我的线索移入无效
        resp = self.clueAPI.move_to_invalid(clueNos=self.clueNos)

    @allure.story("线索管理-线索详情页")
    @allure.title("线索详情基本信息")
    @pytest.mark.getClueByAuth
    def test_getClueByAuth(self, before_test_getClueByAuth):
        resp = self.clueAPI.getClueByAuth(clueNo=self.clueNos, )
        assert resp["message"] == "操作成功" and resp["value"]["clueNo"]

    @pytest.fixture()
    def before_test_get_followup_record(self, init_clue):
        """
        获取线索详情页-跟进记录的前置条件：创建线索，并写跟进
        :param init_clue:
        :return:
        """
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        self.clueNos = self.resp["value"]
        # (线索)写跟进
        self.clueAPI.create_FollowUp(
            self.clueNos,
            "这是跟进线索内容",
            get_timeString(tomorrow=True))
        yield
        # 把我的线索移入无效
        self.clueAPI.move_to_invalid(clueNos=self.clueNos)

    @allure.story("线索管理-线索详情页")
    @allure.title("跟进记录")
    @pytest.mark.get_followup_record
    def test_get_followup_record(self, before_test_get_followup_record):
        resp = self.clueAPI.get_followup_record(self.clueNos)
        assert len(resp["value"]["rows"]) != 0 and resp["value"]["total"] != 0

    @pytest.fixture()
    def before_test_get_operation_record(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        yield
        # 把我的线索移入无效
        resp = self.clueAPI.move_to_invalid(clueNos=self.resp["value"])

    @allure.story("线索管理-线索详情页")
    @allure.title("获取(线索)操作记录")
    @pytest.mark.get_operation_record
    def test_get_operation_record(self, before_test_get_operation_record):
        fkid = self.resp["value"]
        resp = self.clueAPI.get_operation_record(fkid)
        assert resp["value"]["rows"] != []

    @pytest.fixture()
    def before_test_move_to_myself(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        # 把我的线索移入无效
        self.clueAPI.move_to_invalid(clueNos=self.resp["value"])
        yield
        # 把我的线索移入无效
        resp = self.clueAPI.move_to_invalid(clueNos=self.resp["value"])

    @allure.story("线索管理-无效线索列表/公海线索列表")
    @allure.title("加入我的线索")
    @pytest.mark.move_to_myself
    def test_move_to_myself(self, before_test_move_to_myself):
        fkid = self.resp["value"]
        phone = self.clueInfo["phone"]
        resp1 = self.clueAPI.move_to_myself(clueNos=fkid)
        resp2 = self.clueAPI.get_myself_clue(value=phone)
        assert "操作成功" in resp2['message'] and resp2["value"]["rows"][0]["phone"] == phone

    @pytest.fixture()
    def before_test_get_noMaster(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        # 把我的线索移入公海
        self.clueAPI.move_to_noMaster(clueNos=self.resp["value"])
        yield

    @allure.story("线索管理-公海线索列表")
    @allure.title("获取公海线索列表")
    @pytest.mark.get_noMaster
    def test_get_noMaster(self, before_test_get_noMaster):
        resp = self.clueAPI.get_noMaster()
        assert resp["value"]["rows"] != []

    @pytest.fixture()
    def before_test_get_invalid(self, init_clue):
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        # 把我的线索移入无效
        self.clueAPI.move_to_invalid(clueNos=self.resp["value"])
        yield

    @allure.story("线索管理-无效线索列表")
    @allure.title("获取无效线索列表")
    @pytest.mark.get_invalid
    def test_get_invalid(self, before_test_get_invalid):
        resp = self.clueAPI.get_invalid()
        assert resp["value"]["rows"] != []

    @pytest.fixture()
    def before_test_get_extension(self, init_extension_clue):
        self.clueAPI = init_extension_clue[0]
        self.resp = init_extension_clue[1]
        self.clueInfo = init_extension_clue[2]
        yield

    @allure.story("线索管理-推广线索列表")
    @allure.title("获取推广线索列表")
    @pytest.mark.get_extension
    def test_get_extension(self, before_test_get_extension):
        resp = self.clueAPI.get_extension()
        resp2 = self.clueAPI.get_extension(value=self.clueInfo["phone"])
        assert resp["value"]["rows"] != [] and resp2['value']['rows'][0]['phone'] == self.clueInfo["phone"]

    @pytest.fixture()
    def before_test_create_extension_clue(self, init_extension_clue):
        self.clueAPI = init_extension_clue[0]
        yield

    @allure.story("线索管理-推广线索列表")
    @allure.title("创建推广线索")
    @pytest.mark.create_extension_clue
    def test_create_extension_clue(self, before_test_create_extension_clue):
        clueInfo = create_clueInfo_dict(isExtensionClue=True)
        resp1 = self.clueAPI.save_clue(clueInfo)
        resp2 = self.clueAPI.get_extension(value=clueInfo["phone"])
        assert resp1["message"] == "操作成功" and resp2['value']['rows'][0]['phone'] == clueInfo["phone"]

    @pytest.fixture()
    def before_test_allot_clue(self, init_extension_clue):
        self.clueAPI = init_extension_clue[0]
        self.resp = init_extension_clue[1]
        yield

    @allure.story("线索管理-推广线索列表")
    @allure.title("单个推广线索分配到分公司")
    @pytest.mark.allot_clue
    def test_allot_clue(self, before_test_allot_clue):
        clueNos = self.resp["value"]
        resp = self.clueAPI.allot_clue(clueNos=clueNos)
        assert resp["message"] == f"{clueNos}:操作成功\n"

    @pytest.fixture()
    def before_allot_clue_to_user(self, init_extension_clue):
        self.clueAPI = init_extension_clue[0]
        self.resp = init_extension_clue[1]
        yield

    @allure.story("线索管理-推广线索列表")
    @allure.title("单个推广线索分配到人")
    @pytest.mark.allot_clue_to_user
    def test_allot_clue_to_user(self, before_allot_clue_to_user):
        clueNos = self.resp["value"]
        resp = self.clueAPI.allot_clue_to_user(clueNos=clueNos)
        assert resp["message"] == f"{clueNos}:操作成功\n"

    @pytest.fixture()
    def before_test_import_extension(self, getClueAPI):
        self.clueAPI = getClueAPI

    @pytest.mark.skip("暂不运行")
    @allure.story("线索管理-推广线索列表")
    @allure.title("导入推广线索")
    @pytest.mark.import_extension
    def test_import_extension(self, before_test_import_extension):
        filePath = "data/线索导入模板.xls"
        resp = self.clueAPI.import_extension(filePath)
        assert resp["message"] == "线索导入成功"
        # if "state" in resp.keys():
        #     assert resp["message"] == "线索导入成功"
        # elif "retcode" in resp.keys():
        #     if resp["retcode"] == 9998:
        #         assert resp["message"] == "线索导入异常！详情查看【线索导入异常情况.xls】文件"

    @pytest.fixture()
    def before_test_clue_review(self, init_clue):
        # 这里只实现了创建线索，没有用代码去设置组织参数，需手动去后台设置
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        yield

    @allure.story("线索管理-线索审核列表")
    @allure.title("获取线索审核列表")
    @pytest.mark.clue_review
    def test_clue_review(self, before_test_clue_review):
        """
        测试-获取线索审核列表
        测试该功能时的前置条件:
        1、该测试账号所在分公司，需要在后台设置组织参数【是否需要审核线索】：【是】
        2、创建一条线索
        :param before_test_clue_review:
        :return:
        """
        resp = self.clueAPI.clue_review()
        assert resp["value"]["rows"] != []

    @pytest.fixture()
    def before_test_examine_clue(self, init_clue):
        # 这里只实现了创建线索，没有用代码去设置组织参数，需手动去后台设置
        self.clueAPI = init_clue[0]
        self.resp = init_clue[1]
        self.clueInfo = init_clue[2]
        yield

    @allure.story("线索管理-线索审核列表")
    @allure.title("线索审核")
    @pytest.mark.examine_clue
    def test_examine_clue(self, before_test_examine_clue):
        """
        测试-审核线索
        测试该功能时的前置条件:
        1、该测试账号所在分公司，需要在后台设置组织参数【是否需要审核线索】：【是】
        2、创建一条线索
        :param before_test_examine_clue:
        :return:
        """
        clue_id = self.clueAPI.clue_review()["value"]["rows"][0]["id"]
        resp = self.clueAPI.examine_clue(id=clue_id)
        assert resp["message"] == "操作成功"
