#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 17:03
# @File : base64加密.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None

import base64

def myBase64(data):
    """
    base64加密，用于加密密码
    :param data:
    :return:
    """
    data1 = base64.encodebytes(data.encode("utf8"))
    return data1.decode()

if __name__ == '__main__':
    print(myBase64("123456"))
