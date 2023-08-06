#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/28 9:45
# @Author  : xgy
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import requests
import os
from csptools.common.utils import ConfigureParser

parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
resource_config_deafult = os.path.join(parent_path, "common/config", "default.yaml")


def login(username, password):
    pass


def resources_config(config_file):
    if config_file:
        # todo 传入的配置文件写入
        # 直接复制？
        resources_config = ConfigureParser(yaml_path=config_file)
        resources_config.updata_config()
    else:
        resources_config = ConfigureParser(yaml_path=resource_config_deafult)
        resources_config.updata_config()




if __name__ == '__main__':
    print("start")
    # test_file = 'd:\\document\\pycharmpro\\csptools\\temporary\\resources_test.yaml'
    # resources_config(test_file)
    resources_config(config_file=None)
