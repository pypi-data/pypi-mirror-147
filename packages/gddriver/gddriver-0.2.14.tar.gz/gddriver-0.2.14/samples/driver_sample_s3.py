#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import threading

import gddriver.models as models
import gddriver.transmission as transmission
from gddriver import Provider
from gddriver import get_driver


class ProgressPercentage(object):
    def __init__(self, filename=None, object_size=None):
        self._filename = filename
        self._seen_so_far = 0
        self._lock = threading.Lock()
        if filename:
            self._size = float(os.path.getsize(filename))
        elif object_size:
            self._size = object_size
        else:
            raise Exception('filename or object_size must have one is not null')

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)" % (self._filename, self._seen_so_far,
                                             self._size, percentage))
            sys.stdout.flush()


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        sys.stdout.write('\r{0}% '.format(rate))
        sys.stdout.flush()


s3_access_id = "YOUR S3 ACCESS KEY ID"
s3_access_key = "YOUR S3 ACCESS KEY SECRET"
s3_endpoint = "ENDPOINT: s3.bj.bcebos.com"
container_name = "YOUR BUCKET NAME"

# 1.获取driver
driver = get_driver(Provider.S3)

# 2.初始化 connection
credential = models.Credential(
    access_key_id=s3_access_id,
    access_key_secret=s3_access_key
)

_connection = driver.create_connection_manager(
    store_host=s3_endpoint,
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
    with open("/Users/admin/tmp/test-download-1.obj", "wb") as f:
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
    print("\nDownload")

    def _get_object_size(connection, object_name, container_name):
        return driver.get_object_meta(
            connection=_connection,
            object_name=object_name,
            container_name=container_name
        ).size

    request = models.S3DownloadRequest(
        container_name=container_name,
        file_path="/Users/admin/tmp/test-download.obj2",
        object_name='5a053411bac80d00365c5b3b/test'
    )
    request.threads_count = 4
    object_size = _get_object_size(_connection, '5a053411bac80d00365c5b3b/test', container_name)
    request.progress_callback = ProgressPercentage(object_size=object_size)
    res = driver.download_file(
        connection=_connection,
        request=request
    )
    print("result1, threshold less than file size: {}".format(res))

    request.object_name = '5a053411bac80d00365c5b3b/test-4'
    request.file_path = "/Users/admin/tmp/test-download.obj3"
    object_size = _get_object_size(_connection, '5a053411bac80d00365c5b3b/test-4', container_name)
    request.progress_callback = ProgressPercentage(object_size=object_size)
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
        # 15MB
        file_path = '/Users/admin/Desktop/test/cache.tar.gz'
        data_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            request = models.S3StreamUploadRequest(
                container_name=container_name,
                stream=f,
                object_name="5a053411bac80d00365c5b3b/up-1"
            )
            request.progress_callback = percentage
            request.data_size = data_size

            res = driver.upload_object_via_stream(
                connection=_connection,
                request=request
            )
            print("upload via stream result - {}".format(res))

    def upload_via_stream_with_multi_mode():
        # 1.0 GB
        file_path = '/Users/admin/Desktop/test/test.tar.gz'
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

        request = models.S3StreamUploadRequest(
            container_name=container_name,
            stream=generator,
            object_name="5a053411bac80d00365c5b3b/up-2"
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
    file_path = '/Users/admin/Desktop/test/test.tar.gz'
    print("\nUpload")

    request = models.S3UploadRequest(
        container_name=container_name,
        file_path=file_path,
        object_name="5a053411bac80d00365c5b3b/up-3"
    )
    request.threads_count = 5
    request.part_size = 5 * 1 << 20
    request.progress_callback = ProgressPercentage(filename='/Users/admin/Desktop/test/test.tar.gz')

    res = driver.upload_file(
        connection=_connection,
        request=request
    )

    print("upload result - {}".format(res))


# -----------------------
# 删除
def test_delete():
    print("delete")
    driver.delete_object(
        connection=_connection,
        object_name="5a053411bac80d00365c5b3b/up-1",
        container_name=container_name
    )


# -----------------------
# 拷贝
def test_copy():
    print("copy")
    dst_container_name = container_name
    request = models.S3CopyRequest(
        container_name=container_name,
        object_name="5a053411bac80d00365c5b3b/test",
        dst_container_name=dst_container_name,
        dst_object_name="5a053411bac80d00365c5b3b/test-copy",
    )
    request.multi_threshold = 1
    driver.copy_object(
        connection=_connection,
        request=request
    )


# -----------------------
# 归档
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


# -----------------------
# 恢复
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

    test_delete()
    test_copy()

    test_archive()
    test_restore()
