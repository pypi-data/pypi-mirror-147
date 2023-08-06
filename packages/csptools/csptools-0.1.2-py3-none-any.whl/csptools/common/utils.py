#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/29 15:22
# @Author  : xgy
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @python version: 3.7.4
"""

import subprocess
import shlex
import time
import traceback
import gitlab

import os
import sys
import yaml


parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
resource_config = os.path.join(parent_path, "common/config", "resources.yaml")
resource_config_deafult = os.path.join(parent_path, "common/config", "default.yaml")

yaml_l = [resource_config]

class ConfigureParser():
    """
    配置类，通过读取配置文件实例化
    """

    parent_path = os.path.dirname(os.path.split(os.path.realpath(__file__))[0])
    resource_config = os.path.join(parent_path, "common/config", "resources.yaml")

    def __init__(self, yaml_path=None):
        self.config_path = yaml_path

    @property
    def data(self):
        # self.check_config(yaml_l=yaml_l)
        if os.path.exists(self.config_path):
            with open(self.config_path, "r", encoding="utf-8") as fr:
                config_dict = yaml.load(fr, Loader=yaml.FullLoader)

                return config_dict

    def updata_config(self, ouput=None):
        congfig_new = self.data
        resource_config = self.resource_config if not ouput else ouput
        with open(resource_config, "w", encoding="utf-8") as fw:
            yaml.dump(congfig_new, fw, allow_unicode=True, encoding="utf-8")
            print("Configuration succeeded")

    @staticmethod
    def check_config(yaml_l=yaml_l):
        for item in yaml_l:
            flag = os.path.exists(item)
            if not flag:
                raise RuntimeError("There is no configuration. Pleace run config command first.'CSP config -h' for help")


class RunSys:
    """
    执行 shell 命令
    """

    def __init__(self, command: str = None):
        self.command = command
        self.output = None

    def run_cli(self):
        cmd = shlex.split(self.command)
        try:
            # output = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
            subprocess.check_call(cmd, stderr=subprocess.STDOUT)
            # self.output = output.decode()
        except subprocess.CalledProcessError as e:
            print(traceback.print_exc())


# gitlab API 整合，获取项目信息
class GitlabAPI(object):
    """
    获取工具集 gitlab 工程列表
    """

    def __init__(self, url, private_token):
        # self.gl = gitlab.Gitlab()
        self.private_token = private_token
        self.url = url
        self.gl = gitlab.Gitlab(url=self.url, private_token=self.private_token, timeout=3)
        self.groups = []
        self.projects = []

    def get_all_projects(self):
        projects = self.gl.projects.list(all=True)
        result_list = []
        for project in projects:
            result_list.append(project.http_url_to_repo)
            self.projects.append(project)
        return result_list

    def get_group(self):
        group_list = []
        items = self.gl.groups.list(as_list=False)
        for item in items:
            group_list.append(item.attributes)
            self.groups.append(item)
        return group_list

    def get_group_projects(self, *args):
        group_projects = []
        _ = self.get_group()
        for item in self.groups:
            if args:
                if item.name in args:
                    projects = item.projects.list(all=True)
                    for project in projects:
                        # group_projects.append(project.http_url_to_repo)
                        # group_projects.append(project.attributes)
                        group_projects.append([project.http_url_to_repo, project.namespace["name"], project.description])
            else:
                projects = item.projects.list()
                for project in projects:
                    # group_projects.append(project.attributes)
                    group_projects.append([project.http_url_to_repo, project.namespace["name"], project.description])
        return group_projects










if __name__ == '__main__':
    print("start")

    __test_private_token__ = 'FyvDzBm8EmYLfiUxxb2q'
    __gitlab_url__ = 'http://192.168.55.37:12001/'

    # gitlb API
    # user_name ='xgy'
    # groupname = ["人工智能", "safetyctrl"]
    # git = GitlabAPI(url=__gitlab_url__, private_token=__test_private_token__)
    # pro_all = git.get_all_projects()
    # group_list = git.get_group()
    # group_pro_l = git.get_group_projects(*groupname)
    test = 'd:\\document\\pycharmpro\\csptools\\src\\csptools\\common\\config\\resources.yaml'
    with open(test, "r", encoding="utf-8") as fr:
        config_dict = yaml.load(fr, Loader=yaml.FullLoader)
