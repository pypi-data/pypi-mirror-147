#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2022/3/29 10:20
# @Author  : xgy
# @Site    : 
# @File    : nexus_config.py
# @Software: PyCharm
# @python version: 3.7.4
"""
from dataclasses import dataclass, field
from csptools.common.utils import ConfigureParser, resource_config


congfig_dict = ConfigureParser(yaml_path=resource_config).data

# nexus 私服信息配置
@dataclass
class NexusConfig:
    url: str = congfig_dict["nexus"]["url"]
    port: str = "18081"      # 查询API端口均为18081，docker镜像上传、下载端口为28081
    repository: str = None
    format: str = None
    name: str = None


# nexus 私服，docker镜像查询配置
@dataclass
class NexusDocker(NexusConfig):
    repository: str = "docker"
    format: str = "docker"
    name: str = None


# nexus 私服，docker镜像下载配置
@dataclass
class NexusDockerDownload(NexusConfig):
    port: str = congfig_dict["nexus"]["docker_port"]
    images: str = None
    tag: str = None


# nexus 私服，resources资源查询配置
@dataclass
class NexusResources(NexusConfig):
    port: str = congfig_dict["nexus"]["resources_port"]
    repository: str = "resources"
    format: str = "raw"
    groups: list = field(default_factory=lambda: congfig_dict["nexus"]["resources_groups"])


if __name__ == '__main__':
    print("start")
