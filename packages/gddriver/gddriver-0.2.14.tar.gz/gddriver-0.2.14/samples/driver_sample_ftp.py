#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import gddriver.models as models
import gddriver.transmission as transmission
import gddriver.utils.io as ioutil
from gddriver import Provider
from gddriver import get_driver


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        sys.stdout.write('\r{0}% '.format(rate))
        sys.stdout.flush()


FTP_HOST = '192.168.1.111'
FTP_PORT = 21
FTP_USER = 'bio'
FTP_PASSWORD = 'bio123'

CONTAINER_ROOT = 'ftp'

# 1. 获取driver
driver = get_driver(Provider.FTP)

# 2. 初始化 connection
credential = models.Credential(
    user=FTP_USER,
    password=FTP_PASSWORD
)
connection = driver.create_connection_manager(
    store_host=FTP_HOST,
    store_port=FTP_PORT,
    credential=credential
)


def get_object():
    print('\nGet object')
    obj = driver.get_object_meta(
        connection=connection,
        object_name='test/bin-file-1',
        container_name=CONTAINER_ROOT
    )
    print(obj)


def list_container():
    print('\nList')
    objects, _ = driver.list_container_objects(
        connection=connection,
        container_name=CONTAINER_ROOT,
        prefix='test/'
    )
    for i in objects:
        print(i)


def delete_object():
    print("\nDelete object")
    driver.delete_object(
        connection=connection,
        object_name='test/test',
        container_name=CONTAINER_ROOT
    )


def download_as_stream():
    print("\nDownload as stream")
    request = models.FTPStreamDownloadRequest(
        container_name=CONTAINER_ROOT,
        object_name='test/bin-file-1'
    )
    request.buffer_size = 1024
    request.progress_callback = percentage
    stream = driver.download_object_as_stream(
        connection=connection,
        request=request
    )
    adapter = ioutil.make_checksum_adapter(
        data=stream,
        checksum_type='md5'
    )
    with open('/Users/rao-mengnan/test-ftp-download.obj', 'wb') as f:
        for data in adapter:
            f.write(data)
    print(adapter.checksum)


def download_to_file():
    print("\nDownload to file")
    # 文件大小小于threshold时，会使用流式下载，FTP的threads参数影响的是缓冲区大小
    request = models.FTPDownloadRequest(
        container_name=CONTAINER_ROOT,
        file_path="/Users/rao-mengnan/tmp/test-download.obj",
        object_name='test/bin-file-1'
    )
    request.threads_count = 4
    request.checksum_type = 'md5'
    request.progress_callback = percentage

    res = driver.download_file(
        connection=connection,
        request=request
    )
    print(res)


def upload_file():
    print("\nUpload file")

    file_path = '/Users/rao-mengnan/Test/small-binary-file'
    request = models.FTPUploadRequest(
        container_name=CONTAINER_ROOT,
        file_path=file_path,
        object_name="test/bin-file-1"
    )
    request.threads_count = 5,
    request.checksum_type = 'md5'
    request.progress_callback = percentage
    res = driver.upload_file(
        connection=connection,
        request=request
    )
    print(res)


def upload_via_stream():
    print("\nUpload via stream")
    with open('/Users/rao-mengnan/Test/CL100006359_L01_2_1.fq.gz', 'rb') as f:
        request = models.OSSStreamUploadRequest(
            container_name=CONTAINER_ROOT,
            stream=f,
            object_name='test/bin-file-2'
        )
        request.checksum_type = 'md5'
        request.progress_callback = percentage
        res = driver.upload_object_via_stream(
            connection=connection,
            request=request
        )
        print(res)


def append_via_stream():
    print("\nAppend via stream")
    object_name = 'test/test-append'

    with open('/Users/rao-mengnan/Test/small-binary-file', 'rb') as f:
        position = transmission.get_object_append_position(
            connection=connection,
            driver=driver,
            object_name=object_name,
            container_name=CONTAINER_ROOT
        )
        request = models.AppendRequest(
            container_name=CONTAINER_ROOT,
            stream=f,
            object_name=object_name,
            position=position
        )

        res = driver.append_object(
            connection=connection,
            request=request
        )
        print(res)


def copy():
    print("\nCopy object")
    request = models.CopyRequest(
        container_name=CONTAINER_ROOT,
        object_name='test/bin-file-1',
        dst_container_name=CONTAINER_ROOT,
        dst_object_name='test/bin-file-1-copy'
    )
    driver.copy_object(
        connection=connection,
        request=request
    )


if __name__ == '__main__':
    try:
        get_object()
        list_container()

        append_via_stream()
        upload_file()
        upload_via_stream()

        download_as_stream()
        download_to_file()

        copy()

    finally:
        connection.close()
