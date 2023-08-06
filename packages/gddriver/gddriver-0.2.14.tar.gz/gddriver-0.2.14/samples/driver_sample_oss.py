#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import gddriver.models as models
import gddriver.transmission as transmission
from gddriver import Provider
from gddriver import get_driver


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        sys.stdout.write('\r{0}% '.format(rate))
        sys.stdout.flush()


oss_access_id = "YOUR OSS ACCESS KEY ID"
oss_access_key = "YOUR OSS ACCESS KEY SECRET"
oss_endpoint = "ENDPOINT: oss-cn-beijing.aliyuncs.com"
container_name = "YOUR BUCKET NAME"

# 1. 获取driver
driver = get_driver(Provider.OSS)

# 2. 初始化 connection
credential = models.Credential(
    access_key_id=oss_access_id,
    access_key_secret=oss_access_key
)

_connection = driver.create_connection_manager(
    store_host=oss_endpoint,
    store_port=None,
    credential=credential
)


# -----------------------
# 获取Object的meta信息
def test_get_object():
    print("\nGet objects")
    obj = driver.get_object_meta(
        connection=_connection,
        container_name=container_name,
        object_name='5a053411bac80d00365c5b3b/test'
    )
    print(obj)


# -----------------------
# 列出Bucket中的内容
def test_list_container():
    print("\nList container")
    ls, next_mark = driver.list_container_objects(
        connection=_connection,
        container_name=container_name,
        max_objects=1
    )
    name_list = [x.name for x in ls]
    print("name list: {}, next marker: {}".format(name_list, next_mark))


# -----------------------
# 流式下载
def test_download_as_stream():
    print("\nDownload as stream")
    with open("/Users/rao-mengnan/test-download-1.obj", "wb") as f:
        request = models.StreamDownloadRequest(
            container_name=container_name,
            object_name='5a053411bac80d00365c5b3b/test'
        )
        stream = driver.download_object_as_stream(
            connection=_connection,
            request=request
        )
        for data in stream:
            f.write(data)
        print("download result - server checksum: {}, checksum type: {}".format(stream.server_checksum,
                                                                                stream.checksum_type))


# -----------------------
# 普通下载
def test_download():
    # OSS 服务端不提供下载时返回文件的MD5
    print("\nDownload")

    request = models.OSSDownloadRequest(
        container_name=container_name,
        file_path="/Users/rao-mengnan/tmp/test-download.obj2",
        object_name='5a053411bac80d00365c5b3b/test-4'
    )
    request.threads_count = 4
    request.progress_callback = percentage
    res = driver.download_file(
        connection=_connection,
        request=request
    )
    print("result1, threshold less than file size: {}".format(res))

    request.object_name = '5a053411bac80d00365c5b3b/test-4',
    request.file_path = "/Users/rao-mengnan/tmp/test-download.obj2",
    res = driver.download_file(
        connection=_connection,
        request=request
    )
    print("result2, threshold (default) great than file size: {}".format(res))


# -----------------------
# 流式上传
def test_upload():
    print("\nUpload via stream")

    def upload_via_stream():
        # 10MB
        file_path = '/Users/rao-mengnan/Test/genedock-sdk-tool.jar'
        data_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            request = models.OSSStreamUploadRequest(
                container_name=container_name,
                stream=f,
                object_name="5a053411bac80d00365c5b3b/SDK-TOOL"
            )
            request.progress_callback = percentage
            request.data_size = data_size

            res = driver.upload_object_via_stream(
                connection=_connection,
                request=request
            )
            print("upload via stream result - {}".format(res))

    def upload_via_stream_with_multi_mode():
        # 1.7GB
        file_path = '/Users/rao-mengnan/Test/CL100006359_L01_2_1.fq.gz'
        data_size = os.path.getsize(file_path)

        # 上传大文件流时需要控制文件流每一块的大小
        def iterator_generator():
            with open(file_path, "rb") as f:
                while True:
                    chunk = f.read(1 << 23)
                    if not chunk:
                        break
                    yield chunk

        generator = iterator_generator()

        request = models.OSSStreamUploadRequest(
            container_name=container_name,
            stream=generator,
            object_name="5a053411bac80d00365c5b3b/CL-1"
        )
        request.multi = True
        request.progress_callback = percentage
        request.data_size = data_size
        res = driver.upload_object_via_stream(
            connection=_connection,
            request=request
        )
        print('upload big stream - {}'.format(res))

    upload_via_stream()
    upload_via_stream_with_multi_mode()


# -----------------------
# 多线程上传
def test_multipart_upload():
    file_path = '/Users/rao-mengnan/Test/CL100006359_L01_2_1.fq.gz'
    print("\nUpload")

    request = models.OSSUploadRequest(
        container_name=container_name,
        file_path=file_path,
        object_name="5a053411bac80d00365c5b3b/CL-2"
    )
    request.threads_count = 5
    request.part_size = 1 << 20
    request.progress_callback = percentage

    res = driver.upload_file(
        connection=_connection,
        request=request
    )

    print("upload result - {}".format(res))


# -----------------------
# 追加上传
def test_append_object():
    print("Append upload")
    file_path = '/Users/rao-mengnan/Test/genedock-sdk-tool.jar'
    obj_name = "5a053411bac80d00365c5b3b/test-append"
    data_size = os.path.getsize(file_path)
    with open(file_path, 'rb') as f:
        position = transmission.get_object_append_position(
            connection=_connection,
            driver=driver,
            object_name=obj_name,
            container_name=container_name
        )
        request = models.AppendRequest(
            container_name=container_name,
            stream=f,
            object_name=obj_name,
            position=position
        )
        request.progress_callback = percentage
        request.data_size = data_size
        res = driver.append_object(
            connection=_connection,
            request=request
        )
        print("append result - {}".format(res))


# -----------------------
# 删除
def test_delete():
    print("delete")
    driver.delete_object(
        connection=_connection,
        object_name="5a053411bac80d00365c5b3b/test-append",
        container_name=container_name
    )


# -----------------------
# 拷贝
def test_copy():
    print("copy")
    dst_container_name = container_name
    request = models.OSSCopyRequest(
        container_name=container_name,
        object_name="5a053411bac80d00365c5b3b/CL-1",
        dst_container_name=dst_container_name,
        dst_object_name="5a053411bac80d00365c5b3b/test-copy",
    )
    request.multi_threshold = 1
    driver.copy_object(
        connection=_connection,
        request=request
    )


def test_archive():
    print("mock archive")
    archive_container_name = container_name
    driver.archive_object(
        connection=_connection,
        src_object_name='5a053411bac80d00365c5b3b/test-copy',
        src_container_name=container_name,
        archive_container_name=archive_container_name,
        archive_object_name='5a053411bac80d00365c5b3b/test-archived'
    )


def test_restore():
    print("mock restore")
    driver.restore_object(
        connection=_connection,
        src_container_name=container_name,
        src_object_name='5a053411bac80d00365c5b3b/test-archived')


if __name__ == '__main__':
    test_get_object()
    test_list_container()

    test_download_as_stream()
    test_download()

    test_upload()
    test_multipart_upload()
    test_append_object()

    test_copy()
    test_archive()
    test_restore()
