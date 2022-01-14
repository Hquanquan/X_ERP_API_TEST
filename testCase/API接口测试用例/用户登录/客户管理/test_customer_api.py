#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2022/1/13 13:34
# @File : test_customer_api.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import pytest
import allure

from utils.excel_tools import get_ExcelDataByCaseName
from utils.string_tools import create_customerInfo_dict, get_phone_num
from utils.time_tools import get_timeString


@allure.epic("X-ERP系统接口测试")
@allure.feature("客户管理-CustomerAPI客户管理接口测试")
class TestCustomerAPI:

    @allure.story("客户管理-我的客户列表")
    @allure.title("{title}")
    @pytest.mark.customer_list
    # inData 请求体参数  expectedData 预期结果数据（不准确，暂时不使用） title 用例标题
    @pytest.mark.parametrize("inData,expectedData,title", get_ExcelDataByCaseName("客户管理", "customer_list"))
    def test_customer_list(self, inData, expectedData, title, initCustomerAPI):
        # 动态生成描述
        allure.dynamic.description(f"我的客户列表：{title}")
        customerApi = initCustomerAPI[0]
        resp = customerApi.customer_list(inData)
        # 客户数据在列表中，列表不为0，则断言通过
        assert len(resp["value"]["rows"]) != 0

    @pytest.fixture()
    def before_test_customer_moveTo_noMaster(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]

    @allure.story("客户管理-我的客户列表-客户移入公海")
    @allure.title("单个客户移入公海")
    @pytest.mark.customer_moveTo_noMaster
    def test_customer_moveTo_noMaster(self, before_test_customer_moveTo_noMaster):
        custNos = self.resp["value"]
        resp = self.customerApi.customer_moveTo_noMaster(custNos=custNos)
        assert resp["message"] == f"{custNos}操作成功\n"

    @pytest.fixture()
    def before_test_transfer_customer(self, init_customer):
        self.customerApi = init_customer[0]
        self.commomApi = init_customer[1]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-我的客户列表-转移客户")
    @allure.title("单个客户转移")
    @pytest.mark.transfer_customer
    def test_transfer_customer(self, before_test_transfer_customer):
        """
        单个客户转移
        :param before_test_transfer_customer:
        :return:
        """
        custNos = self.resp["value"]
        userID = self.commomApi.querySubUser("张迪")["rows"][0]["id"]
        resp = self.customerApi.transfer_customer(custNos, userID)
        assert resp["value"] == f"{custNos}:操作成功\n"

    @pytest.fixture()
    def before_test_write_customer_follow_up(self, init_customer):
        self.customerApi = init_customer[0]
        self.commomApi = init_customer[1]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-我的客户列表-写跟进")
    @allure.title("写跟进")
    @pytest.mark.write_customer_follow_up
    def test_write_customer_follow_up(self, before_test_write_customer_follow_up):
        custNos = self.resp["value"]
        resp = self.customerApi.write_customer_follow_up(
            custNos,
            nextFollowTime=get_timeString(tomorrow=True))
        assert resp["state"] is True

    @pytest.fixture()
    def after_test_create_customer(self, initCustomerAPI):
        self.customerApi = initCustomerAPI[0]
        self.commomApi = initCustomerAPI[1]
        self.userId = initCustomerAPI[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-我的客户列表-创建客户")
    @allure.title("创建客户")
    @pytest.mark.create_customer
    def test_create_customer(self, after_test_create_customer):
        # 获取企业工商信息
        enterprise_info = self.commomApi.get_enterprise_info("91110000710921189P")["value"][0]
        # 获取当前账号所在分公司编号
        followCompany = self.commomApi.getOrgByUserId(self.userId)['value'][0]['id']
        # 获取线索编号
        # clueApi = ClueAPI(get_token[0])
        # clueNo = clueApi.get_myself_clue()["value"]["rows"][0]["clueNo"]
        # 使用函数生成客户参数字段信息
        customerInfo = create_customerInfo_dict(enterprise_info, followCompany=followCompany)
        self.resp = self.customerApi.create_customer(customerInfo)
        assert self.resp["message"] == "操作成功" and self.resp["value"] is not None

    @pytest.fixture()
    def before_test_customer_details(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("客户详情-基础信息")
    @pytest.mark.customer_details
    def test_customer_details(self, before_test_customer_details):
        custNos = self.resp["value"]
        resp = self.customerApi.customer_details(custNos)
        assert resp["value"]["custNo"] == custNos and resp["value"]["person"] is not None

    @pytest.fixture()
    def before_test_edit_customer(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("编辑客户基础信息")
    @pytest.mark.edit_customer
    def test_edit_customer(self, before_test_edit_customer):
        # 客户编号
        custNos = self.resp["value"]
        # 获取查询到的客户基础信息
        customerValue = self.customerApi.customer_details(custNos)["value"]
        resp = self.customerApi.edit_customer(custNos, customerValue,
                                              remark=f"这是短短的备注信息{custNos}",
                                              intentionToGrade="B")
        assert resp["message"] == "操作成功" and resp["value"] == custNos

    @pytest.fixture()
    def before_test_add_contacts(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("添加联系人")
    @pytest.mark.add_contacts
    def test_add_contacts(self, before_test_add_contacts):
        # 客户编号
        custNos = self.resp["value"]
        # 这里就只添加联系人名称和手机号码
        # 使用工具随机生成手机号,phones是列表类型的
        phones = [get_phone_num()]
        person = f"联系人{phones[0]}"
        resp = self.customerApi.add_contacts(custNos,
                                             phones=phones,
                                             person=person)
        assert resp["message"] == "操作成功"

    @pytest.fixture()
    def before_test_customer_contact_info(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("获取联系人信息")
    @pytest.mark.customer_contact_info
    def test_customer_contact_info(self, before_test_customer_contact_info):
        # 客户编号
        custNos = self.resp["value"]
        resp = self.customerApi.customer_contact_info(custNos)
        assert resp["value"][0]["person"] is not None

    @pytest.fixture()
    def before_test_set_primary_contact(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("设为主联系人")
    @pytest.mark.set_primary_contact
    def test_set_primary_contact(self, before_test_set_primary_contact):
        # 客户编号
        custNos = self.resp["value"]
        # 联系人信息编号
        contactNum = self.customerApi.customer_contact_info(custNos)["value"][0]["contactNum"]
        resp = self.customerApi.set_primary_contact(contactNum)
        assert resp["message"] == "操作成功"

    @pytest.fixture()
    def before_test_delete_contact(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        # 客户编号
        custNos = self.resp["value"]
        # 这里就只添加联系人名称和手机号码
        # 使用工具随机生成手机号,phones是列表类型的
        phones = [get_phone_num()]
        person = f"联系人{phones[0]}"
        # 添加一个新的联系人
        self.customerApi.add_contacts(custNos,
                                      phones=phones,
                                      person=person)
        yield
        # 测试完成把客户数据移入公海
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("删除联系人")
    @pytest.mark.delete_contact
    def test_delete_contact(self, before_test_delete_contact):
        # 客户编号
        custNos = self.resp["value"]
        # 联系人编号
        contactNum = self.customerApi.customer_contact_info(custNos)["value"][0]["contactNum"]
        resp = self.customerApi.delete_contact(contactNum)
        assert resp["message"] == "操作成功"

    @pytest.fixture()
    def before_test_get_customer_followup_record(self, init_customer):
        self.customerApi = init_customer[0]
        self.commomApi = init_customer[1]
        self.resp = init_customer[2]
        self.custNos = self.resp["value"]
        self.customerApi.write_customer_follow_up(
            self.custNos,
            nextFollowTime=get_timeString(tomorrow=True))
        yield
        # 测试完成把客户数据移入公海
        self.customerApi.customer_moveTo_noMaster(custNos=self.custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("跟进记录")
    @pytest.mark.get_customer_followup_record
    def test_get_customer_followup_record(self, before_test_get_customer_followup_record):
        resp = self.customerApi.get_customer_followup_record(self.custNos)
        # 判断列表有数据返回，不为空，则列表长度不为0
        assert len(resp["value"]["rows"]) != 0 and resp["value"]["total"] != 0

    @pytest.fixture()
    def before_test_get_enterprise_info_02(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("企业资料")
    @pytest.mark.get_enterprise_info
    def test_get_enterprise_info_02(self, before_test_get_enterprise_info_02):
        # 客户编号
        custNos = self.resp["value"]
        # 02 代表获取的是企业资料
        resp = self.customerApi.get_enterprise_info(custNos, "02")
        assert resp["message"] == "操作成功"

    @pytest.fixture()
    def before_test_get_enterprise_info_01(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        # 正常的前置条件是应该要上传资料的，但是为了方便就不上传了
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("客户资料")
    @pytest.mark.get_enterprise_info
    def test_get_enterprise_info_01(self, before_test_get_enterprise_info_01):
        # 客户编号
        custNos = self.resp["value"]
        # 01 代表获取的是客户资料
        resp = self.customerApi.get_enterprise_info(custNos, "01")
        assert resp["message"] == "操作成功"

    @pytest.fixture()
    def before_test_get_opportunity_manager(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        # 正常的前置条件是应该要创建一个商机的，但是为了方便就不创建了
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("商机管理")
    @pytest.mark.get_opportunity_manager
    def test_get_opportunity_manager(self, before_test_get_opportunity_manager):
        # 客户编号
        custNos = self.resp["value"]
        resp = self.customerApi.get_opportunity_manager(custNos)
        assert resp["message"] == "获取成功"

    @pytest.fixture()
    def before_test_get_orders(self, init_customer):
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        # 正常的前置条件是应该要创建一个订单的，但是为了方便就不创建了
        yield
        # 测试完成把客户数据移入公海
        custNos = self.resp["value"]
        self.customerApi.customer_moveTo_noMaster(custNos=custNos)

    @allure.story("客户管理-客户详情页")
    @allure.title("获取订单列表")
    @pytest.mark.get_orders
    def test_get_get_orders(self, before_test_get_orders):
        # 客户编号
        custNos = self.resp["value"]
        resp = self.customerApi.get_orders(custNos)
        assert resp["message"] == "获取成功"

    @pytest.fixture()
    def before_test_to_do_tasks(self, init_customer):
        # 前置条件，创建一个客户，创建一个客户跟进类型的任务
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        custNo = self.resp["value"]
        self.customerApi.create_task([custNo])
        yield
        # 测试完成把客户数据移入公海
        self.customerApi.customer_moveTo_noMaster(custNos=custNo)

    @allure.story("客户管理-客户详情页")
    @allure.title("待办任务")
    @pytest.mark.to_do_tasks
    def test_get_to_do_tasks(self, before_test_to_do_tasks):
        # 客户编号
        custNos = self.resp["value"]
        resp = self.customerApi.to_do_tasks(custNos)
        assert resp["state"] is True and resp["value"]["total"] != 0

    @pytest.fixture()
    def before_test_customer_noMaster_list(self, init_customer):
        """
        公海客户列表前置条件：创建一个客户，再把这个客户移入公海
        :param init_customer:
        :return:
        """
        self.customerApi = init_customer[0]
        self.resp = init_customer[2]
        self.custNo = self.resp["value"]
        # 把创建的客户移入公海
        self.customerApi.customer_moveTo_noMaster(self.custNo)

    @allure.story("客户管理-公海客户列表")
    @allure.title("公海客户列表")
    @pytest.mark.customer_noMaster_list
    def test_customer_noMaster_list(self, before_test_customer_noMaster_list):
        resp = self.customerApi.customer_noMaster_list()
        assert len(resp["value"]["rows"]) != 0 and resp["message"] == "操作成功"

    @pytest.fixture()
    def before_test_reassign_customer(self, init_customer):
        """
        公海客户列表前置条件：创建一个客户，再把这个客户移入公海
        :param init_customer:
        :return:
        """
        self.customerApi = init_customer[0]
        self.commonApi = init_customer[1]
        self.resp = init_customer[2]
        self.custNo = self.resp["value"]
        # 把创建的客户移入公海
        self.customerApi.customer_moveTo_noMaster(self.custNo)

    @allure.story("客户管理-公海客户")
    @allure.title("重新指派（客户）")
    @pytest.mark.reassign_customer
    def test_reassign_customer(self, before_test_reassign_customer):
        userID = self.commonApi.querySubUser("李振辉")["rows"][0]["id"]
        resp = self.customerApi.reassign_customer(self.custNo, userID)
        assert resp["value"] == f"{self.custNo}:操作成功\n"
