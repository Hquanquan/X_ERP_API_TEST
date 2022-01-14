#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/1 21:48
# @File : excel_tools.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : Excel表格工具
import json

import xlrd

from configs.api_env import TestCaseFilePath


def get_ExcelDataByCaseName(sheetName, caseName, filePath=TestCaseFilePath):
    """
    读取Excel表格里的接口测试用例
    :param sheetName: Excel表里的sheet子表名字
    :param caseName: 测试用例第一列的caseName前缀字母
    :param filePath: Excel表的文件路径
    :return:
    """
    # 1、声明一个列表resList用来存储读取到的测试用例数据
    resList = []
    # 2、打开Excel表格,formatting_info=True保持原样式打开
    workBook = xlrd.open_workbook(filePath, formatting_info=True)
    # 3、根据sheetName获取sheet子表
    workSheet = workBook.sheet_by_name(sheetName)
    # 4、以列表的形式返回sheet子表第一行的所有数据
    col_values = workSheet.col_values(0)
    idx = 0  # 开始的下标
    # 5、遍历循环，比较第一列的内容是否包含caseName
    for oneValue in col_values:
        # 6、包含caseName，则该行数据为测试数据
        if caseName in oneValue:
            # 7、读取请求体参数
            reqBodyData = workSheet.cell(idx, 9).value
            # 8、读取预期响应结果数据
            respData = workSheet.cell(idx, 11).value
            # 9、读取测试用例标题title
            test_Title = workSheet.cell(idx, 4).value
            # 10、列表里嵌套元组，元组保存读取到的测试用例数据
            resList.append((json.loads(reqBodyData), json.loads(respData), test_Title))
        idx += 1
    return resList



if __name__ == '__main__':
    respdata = get_ExcelDataByCaseName("线索管理", "list_myself_clue", r".././data/X-ERP系统接口测试用例.xls")
    print(respdata[0][1])
    # a = '{"token": "eyJhbGciOiJIUzUxMiJ9.eyJzdWIiOiJRWTAwMDM0MSIsInRlbmFudElkIjoiLTEiLCJleHAiOjE2Mzg0NTcwMzQsImlhdCI6MTYzODM3MDYzNH0.whrPtsY_bLSHU3KwBz8tgDjkwxFFjgVT4M6NlSUeYXjNDdg2BGP0RRUh0UXt-o64CgN6CvuMSV700Q6OSAeISA",' \
    #     '"username": "张迪", "account": "QY000341",' \
    #     '"userId": "1407876689714876416","expiration": 86400,' \
    #     '"loginStatus": true,"userAttrs": {"tenantId": "-1"}}'
    # print(type(a))
    # b = json.loads(a)
    # print(type(b))
    # print(type(b['loginStatus']))
