# -*- coding: utf-8 -*-
"""
通过gddriver.GenericOperator更方便地使用gddriver:

直接使用StorageDriver:
   -> 根据 provider 初始化driver
   -> 使用driver初始化connection
   -> 调用driver的方法时，将connection作为参数

使用generic operator则无需关注繁琐的初始化过程：

operator = gddriver.GenericOperator(
    provider=_get_provider(),  # 'ftp' or 'oss'
    credential=_get_credential(),
    host=host,
    port=port,
    **_get_extra_params()
)

Tips: 动态地提供 provider、credential、extra_params等信息，可以使程序无需关注背后实际的存储介质
"""

import gddriver
import gddriver.models as models


class StorageInfo(object):

    def get_provider(self):
        """
        provider name
        :rtype: str
        """
        raise NotImplementedError

    def get_container(self):
        """
        获取容器名称（bucket）或ftp目录
        :rtype: str
        """
        raise NotImplementedError

    def get_host(self):
        """
        :return: host, port
        """
        raise NotImplementedError

    def get_credential(self):
        """
        :rtype: gddriver.models.Credential
        """
        raise NotImplementedError

    def get_extra_params(self):
        """
        :return open ssl、pasv、timeout等额外的初始化参数
        :rtype: dict
        """
        raise NotImplementedError


class OSSStorageInfo(StorageInfo):

    def get_container(self):
        return "data-bucket"

    def get_provider(self):
        return gddriver.Provider.OSS

    def get_host(self):
        return " oss-cn-shenzhen.aliyuncs.com", None

    def get_credential(self):
        return models.Credential(
            access_key_id=None,
            access_key_secret=None,
            access_key_token=None
        )

    def get_extra_params(self):
        return {}


class FTPStorageInfo(StorageInfo):

    def get_container(self):
        return "/"

    def get_provider(self):
        return gddriver.Provider.FTP

    def get_host(self):
        return '192.168.1.111', 21

    def get_credential(self):
        return models.Credential(
            user='bio',
            password='bio123'
        )

    def get_extra_params(self):
        return dict(
            ssl=True,
            anonymous=False,
            pasv=False,
            timeout=None
        )


# storage_info = OSSStorageInfo()
storage_info = FTPStorageInfo()


host, port = storage_info.get_host()

operator = gddriver.GenericOperator(
    provider=storage_info.get_provider(),
    credential=storage_info.get_credential(),
    host=host,
    port=port,
    **storage_info.get_extra_params()
)

"""operator 支持使用with的上下文，在每次使用之后释放资源"""
with operator:
    obj_list, next_marker = operator.list_container_objects(container_name=storage_info.get_container())
    for i in obj_list:
        print(i)
