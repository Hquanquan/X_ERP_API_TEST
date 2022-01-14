#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/4 9:13
# @File : string_tools.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import random
from pprint import pprint

from utils.time_tools import get_timeString


def get_phone_num():
    """
    生成一个随机的手机号码
    要获取一个手机号，我们首先需要了解手机号码的组成规律，我们简单的认为存在以下规律：
    ①手机号码一共有11位
    ②第1位目前都是1
    ③第2位in[3、4、5、7、8] 取值
    ④第3位比较复杂一些，根据第2位的数字，对应运营商的生成规律
    ⑤后8位是随机生成的8个数字
    :return:
    """
    second_spot = random.choice([3, 4, 5, 7, 8])
    third_spot = {
        3: random.randint(0, 9),
        4: random.choice([5, 7, 9]),
        5: random.choice([i for i in range(10) if i != 4]),
        7: random.choice([i for i in range(10) if i not in [4, 9]]),
        8: random.randint(0, 9), }[second_spot]

    remain_spot = random.randint(9999999, 100000000)
    phone_num = "1{}{}{}".format(second_spot, third_spot, remain_spot)
    return phone_num

def get_QQ_num():
    """随机生成8-10位的qq号"""
    QQ = random.randint(10000000, 9999999999)
    return QQ

def get_random_Num(starNumber=1000000, endNumber=99999999):
    """
    随机生成数字,默认生成7-8位的数字
    :param starNumber:
    :param endNumber:
    :return:
    """
    if endNumber >= starNumber:
        number = random.randint(starNumber, endNumber)
        return number

def create_clueInfo_dict(isExtensionClue=False):
    """
    创建线索的字典信息
    :param isExtensionClue:
    :return:
    """
    # 生成一个随机的手机号码
    phone = get_phone_num()
    # 生成一个随机的QQ号
    qq = get_QQ_num()
    # 随机生成7-8位的数字当做固话号码
    telephone = get_random_Num()
    # 获取当前时间
    obtainTime = get_timeString()
    # isExtensionClue=True 就是创建推广线索的客户信息
    if isExtensionClue:
        clueInfo = {
            "person": f"联系人{phone}",
            "phone": phone,
            "telephone": f"020-{telephone}",
            "wx": f"wx{phone}",
            "qq": qq,
            "email": f"{qq}@qq.com",
            "sourceChannel": "tg_bdss",    # 推广渠道，创建推广线索填写 tg_bdss
            "obtainTime": obtainTime,  # 获取线索时间，创建推广线索填写
            "sourceAccount": "00",  # 推广线索来源户，创建推广线索填写 00
            "remark": f"这是创建推广线索的备注{phone}",
            "consultQua": f"咨询资质{phone}",
            "clueType": "01",    # 推广线索
            "province": "110000",
            "city": "110100",
            "areas": "110101"
        }
    else:
        clueInfo = {
            "person": f"联系人{phone}",
            "phone": phone,
            "telephone": f"020-{telephone}",
            "wx": f"wx{phone}",
            "qq": qq,
            "email": f"{qq}@qq.com",
            "source": "tyc",  # 线索来源：天眼查
            "sourceChannel": "",
            "intentionLevel": "C",
            "demandType": "03",
            "demandRemark": "这个是需求分类备注",
            "remark": f"这是备注{phone}",
            "consultQua": f"咨询资质{phone}",
            "clueType": "00",
            "province": "110000",
            "city": "110100",
            "areas": "110101"
        }
    return clueInfo

def create_customerInfo_dict(enterprise_info=None, clueNo=None, **kwargs):
    """
    生成创建客户的字段字典
    :param clueNo: 线索编号，传递准确的线索编号，则该线索与生成的客户关联
    :param enterprise_info: 企业信息,不传这个参数就是生成个人客户信息
    :param kwargs:
    :return:
    """
    # 生成一个随机的手机号码
    phone = get_phone_num()
    # 生成一个随机的QQ号
    qq = get_QQ_num()
    # 随机生成7-8位的数字当做固话号码
    telephone = get_random_Num()
    customerInfo = {
        "person": f"客户联系人{phone}",  # 联系人 （非共工商信息）
        "custType": "01",  # 客户类型：01 个人客户，02企业客户  （非共工商信息）
        "followCompany": "1442323703668019200",  # 客户归属公司    （非共工商信息）
        "phone": phone,  # 手机号            （非共工商信息）
        "intentionToGrade": "A",  # 意向等级 A,B,C    （非共工商信息）
        "clueNo": "",  # 线索编号 （非共工商信息）
        "qq": qq,  # qq号 （非共工商信息）
        "wx": f"wx{phone}",  # 微信号 （非共工商信息）
        "email": f"{qq}@qq.com",  # 邮箱 （非共工商信息）
        "province": "110000",  # 省 （非共工商信息）
        "city": "110100",  # 市 （非共工商信息）
        "areas": "110101",  # 区 （非共工商信息）
        "address": f"客户详细地址{phone}",  # 客户详细地址 （非共工商信息）
        "source": "tyc",  # 客户来源（非共工商信息）
        "sourceChannel": "",  # 推广渠道，推广线索转换为客户才需要填写（非共工商信息）
        "telephone": f"020-{telephone}",  # 固话（非共工商信息）
        "remark": f"测试备注{phone}",  # 备注（非共工商信息）
        "clueType": "00",  # 线索分类：00 普通线索，01 推广线索（非共工商信息）

        "linkNumber": "",
        "linkType": "",
        "type": "",
        "idNo": ""
    }
    # 更新字典值
    params_keyslist = [onekey for onekey in customerInfo.keys()]
    # 循环对比，kwargs中的key是否有符合的，有则把value赋值到字典中
    for onekey in params_keyslist:
        if onekey in kwargs.keys():
            customerInfo[onekey] = kwargs[onekey]
    # 是否有传递企业信息，有则把企业信息添加到字典
    if enterprise_info:
        customerInfo["nameCn"] = enterprise_info["nameCn"]
        customerInfo["socialCreditCode"] = enterprise_info["socialCreditCode"]
        customerInfo["legalPerson"] = enterprise_info["legalPerson"]
        customerInfo["registAddress"] = enterprise_info["registAddress"]
        customerInfo["registeredCapital"] = enterprise_info["registeredCapital"]
        # 先判断是否有营业开始时间，有则把营业时间传入
        # 再传入营业结束时间，若失败则给自定义的时间
        if "licenseStartDate" in enterprise_info.keys():
            customerInfo["licenseStartDate"] = enterprise_info["licenseStartDate"]
            try:
                customerInfo["licenseEndDate"] = enterprise_info["licenseEndDate"]
            except KeyError as e:
                customerInfo["licenseEndDate"] = "9999-01-01 00:00:00"
        # 没有营业开始时间，则营业期限为空
        else:
            customerInfo["licenseEndDate"] = ""
            customerInfo["licenseEndDate"] = ""

        customerInfo["foundDate"] = enterprise_info["foundDate"]
        customerInfo["issueDate"] = enterprise_info["issueDate"]
        customerInfo["businessScope"] = enterprise_info["businessScope"]
        customerInfo["transformerName"] = enterprise_info["transformerName"]
        if "有限责任公司" in enterprise_info["type"]:
            customerInfo["enterType"] = "04"
        elif "有限责任公司" in enterprise_info["type"]:
            customerInfo["enterType"] = "05"
        else:
            customerInfo["enterType"] = ""
        # 客户类型改成02企业客户
        customerInfo["custType"] = "02"
    if clueNo:
        customerInfo["clueNo"] = clueNo
    return customerInfo









if __name__ == '__main__':
    pprint(create_customerInfo_dict())
