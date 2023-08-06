#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/30 17:06
# @Author  : xgy
# @Site    : 
# @File    : allTools.py
# @Software: PyCharm
# @python version: 3.7.4
"""


# import yaml
import os
import requests
import json
from csptools.common.utils import GitlabAPI, RunSys, ConfigureParser, resource_config


# def resources_list(*args, url, token):
def resources_list():
    config = ConfigureParser(yaml_path=resource_config)
    config.check_config()
    data = config.data

    # 资源包括gitlab工程、resources部署包
    resources_all = []
    for key, value in data.items():
        if key in ["gitlab_in", "gitlab_out"]:
            try:
                git = GitlabAPI(url=value['url'], private_token=value['token'])
                groups = value["groups"]
                group_pro_l = git.get_group_projects(*groups)
                for item in group_pro_l:
                    item.append(key)
                    resources_all.append(item)
            except Exception:
                print("can not connetion to {}".format(key))

        elif key == "nexus" and os.path.exists(resource_config):
            from csptools.common.nexus_config import NexusResources
            resource_info = NexusResources()
            resource_search_url = resource_info.url + ":" + str(resource_info.port) + "/" + "service/rest/v1/search"
            for group in resource_info.groups:
                params = {"repository": resource_info.repository, "format": resource_info.format, "group": group}

                res = requests.get(resource_search_url, params=params)
                res_dict = json.loads(res.text)
                for item in res_dict["items"]:
                    item_name = item["name"].split("/")[-1]
                    item_group = item["group"]
                    item_url = item["assets"][0]["downloadUrl"]
                    item_info = [item_url, item_group, item_name, key]
                    resources_all.append(item_info)
        else:
            raise KeyError('the resources should be from gitlab or nexus')

    print("url", "\t", "groups", "\t", "description", "\t", "local")
    for item in resources_all:
        print(item[0], "\t", item[1], "\t", item[2], "\t", item[3])
        print("\n")
    # return resources_all


def resources_download(url, folder):
    if folder:
        cmd_line = "git clone " + url + " " + folder
    else:
        cmd_line = "git clone " + url

    command = RunSys(cmd_line)
    command.run_cli()


# 测试用
# def nexus_resources_list():
#     """
#     从nexus获取部署包列表
#     :return:
#     """
#     if os.path.exists(resource_config):
#         from csptools.common.nexus_config import NexusResources
#         resource_info = NexusResources()
#         resource_search_url = resource_info.url + ":" + resource_info.port + "/" + "service/rest/v1/search"
#         for group in resource_info.groups:
#             # print(resource_info.groups)
#             params = {"repository": resource_info.repository, "format": resource_info.format, "group": group}
#
#             res = requests.get(resource_search_url, params=params)
#             res_dict = json.loads(res.text)
#
#     return res, res_dict

if __name__ == '__main__':
    print("start")

    # h_res, nex_res = nexus_resources_list()
    # __test_private_token__ = 'rDYfmk1ZkEQ4phz8RxUa'
    # __gitlab_url__ = 'http://192.168.55.37:12001/'
    res = resources_list()
