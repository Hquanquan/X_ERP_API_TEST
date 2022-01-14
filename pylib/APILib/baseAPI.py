#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 12:57
# @File : baseAPI.py
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
from configs.api_env import HOST
from logs.logger import Logger
from utils.yaml_tools import read_yaml

logger = Logger(logger="BaseAPI").getlog()
class BaseAPI:
    """
    基类
    """
    def __init__(self, token):
        # 测试接口的URL地址
        self.HOST = HOST
        # 当前账号的token
        self.token = token
        # 请求头
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Authorization": f"Bearer {self.token}"
        }
        # 接口数据模板文件的相对路径
        # path = "configs/api_conf.yaml"
        # path = "../../../configs/api_conf.yaml"
        # 接口数据模板文件的绝对路径
        path = r"E:\Git_Repository\X_ERP_API_TEST\configs\api_conf.yaml"
        # 读取yaml接口数据模板文件数据
        api_template = read_yaml(path)
        # 获取当前类的类名，便于根据类名读取yaml文件里的模板数据
        current_className = self.__class__.__name__
        # 根据当前类名获取yaml文件接口数据模板
        self.conf = api_template[current_className]




