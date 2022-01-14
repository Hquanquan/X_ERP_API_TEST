#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/12/4 16:24
# @File : yaml_tools.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None

import yaml
def read_yaml(filePath):
    """
    读取yaml文件数据，并以字典格式返回
    :param filePath: yaml文件路径
    :return:
    """
    # 打开filePath路径的文件
    with open(filePath, encoding="utf-8") as f:
        # 读取yaml文件的内容，赋值到content
        content = f.read()
        # 把content转化为字典
        data = yaml.safe_load(content)
        # 返回数据
        return data

