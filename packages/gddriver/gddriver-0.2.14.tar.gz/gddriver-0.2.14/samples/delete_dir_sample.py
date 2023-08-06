# -*- coding: utf-8 -*-

"""ftp driver中需要递归删除目录时，可以通过operator直接调用该属性"""

from gddriver import Provider
from gddriver import transmission
from gddriver import models

host = 'host'
port = 21  # port
user_name = 'ftp user name'
password = 'ftp password'
ssl = False  # default false
pasv = False  # default false

credential = models.Credential(
    user=user_name,
    password=password
)

operator = transmission.GenericOperator(
    host=host,
    port=port,
    credential=credential,
    provider=Provider.FTP,
    ssl=ssl
)

with operator:
    object_name = "/path/to/delete"
    operator.delete_dir(container_name=None, dir_name=object_name)


