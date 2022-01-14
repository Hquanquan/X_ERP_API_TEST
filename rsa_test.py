#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 18:49
# @File : rsa_test.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import rsa


def rsaEncrypt(str1):
    """
    rsa加密
    :param str1:
    :return:
    """
    # 生成公钥私钥
    (pubkey, privkey) = rsa.newkeys(512)
    # print(pubkey)
    # print(privkey)
    # 编码为utf-8格式
    content1 = str1.encode("utf-8")
    # 使用公钥加密
    crypto = rsa.encrypt(content1, pubkey)
    # 返回加密后的数据和私钥
    return crypto, privkey


def rsaDecrypt(str1, pk):
    """
    私钥解密
    :param str1:
    :param pk:
    :return:
    """
    # 使用私钥对数据进行解密
    content = rsa.decrypt(str1, pk)
    # 编码为utf-8格式
    con = content.decode("utf-8")
    return con


if __name__ == '__main__':
    str1, pk = rsaEncrypt("hello")
    print(str1)

    content = rsaDecrypt(str1, pk)
    print(content)
