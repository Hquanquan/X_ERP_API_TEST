#!/usr/bin/python3.8
# -*- coding: utf-8 -*-
# @Time    : 2021/11/24 9:16
# @File : main.py 
# @Author  : 黄权权
# @Software: PyCharm
# @Desc    : None
import os

import pytest

def run():
    """
    运行测试
    :return:
    """
    for one in os.listdir('report/tmp'):  # 列出对应文件夹的数据
        if 'json' in one:
            os.remove(f'report/tmp/{one}')
    pytest.main(['testcase/API接口测试用例', '-s', '--alluredir=report/tmp'])
    # pytest.main(['-m add_myselfClue', '-s', '--alluredir=report/tmp'])
    # pytest.main(['-k test_login_api.py', '-s', '--alluredir=report/tmp'])
    os.system('allure serve report/tmp')

if __name__ == '__main__':
    # pytest.main(["-s", "-k test_login_api.py"])
    # pytest.main(["-s", "-m", "reassign_customer"])
    run()
