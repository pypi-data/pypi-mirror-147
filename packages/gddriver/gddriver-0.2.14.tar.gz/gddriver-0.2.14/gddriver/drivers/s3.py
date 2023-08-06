# -*- coding: utf-8 -*-

"""
S3StorageDriver：
    * 列出Bucket中的Object
    * 获取Object的meta信息
    * 文件上传
    * 流式上传
    * 下载到本地文件
    * 流式下载
    * 复制
    * 删除
    * 批量删除
    * 归档
    * 恢复
    * 获取下载链接
统一使用md5进行校验，不支持在request中自定义的``checksum_type``

"""
import datetime
import functools
import math
import os
import sys
import threading

import boto3
import botocore.exceptions as boto_exc
import baidubce.exception as bos_exc
from boto3.s3.transfer import TransferConfig
from botocore.config import Config
from concurrent.futures import ThreadPoolExecutor, as_completed
from s3transfer import ReadFileChunk

import gddriver.base as base
import gddriver.config as config
import gddriver.errors as err
import gddriver.models as models
import gddriver.utils.io as ioutil
import gddriver.utils.time as timeutil

DEFAULT_DOWNLOAD_BUFFER_SIZE = 1 << 14  # 16MB 默认下载时的缓冲大小
DEFAULT_SIZE_PER_PART = 5 * (1 << 20)  # 5MB 默认每块分片的字节大小
DEFAULT_MULTIPART_TRANSFER_THRESHOLD = 1 << 26  # 64MB 默认分片传输的阈值
DEFAULT_URL_EXPIRES = 3600 * 12  # 12小时  下载链接默认过期时间
DEFAULT_LIST_OBJECTS = 100  # 默认遍历时的max_object
LIST_DATA_MAX_OBJECTS = 1000  # list_container_objects 时最大可获取的object数量
S3_MAX_PART_NUM = 10000  # 分片上传最大分片数
PUT_DATA_MAX_SIZE = 5 * (1 << 30)  # 5GB  调用PutData api最大允许的文件大小
DEFAULT_STORAGE_CLASS = 'STANDARD'
DEFAULT_S3_SIGN_VERSION = 's3v4'

_DEFAULT_LOGGER_NAME = __name__


class BaseStorageClass(object):
    STANDARD = 'STANDARD'  # 标准存储
    STANDARD_IA = 'STANDARD_IA'  # 低频存储


class S3StorageClass(BaseStorageClass):
    """
    s3 storage_class的类型有：'STANDARD','REDUCED_REDUNDANCY','STANDARD_IA','ONEZONE_IA', 'INTELLIGENT_TIERING','GLACIER','DEEP_ARCHIVE','OUTPOSTS'
    """
    REDUCED_REDUNDANCY = 'REDUCED_REDUNDANCY'
    ONEZONE_IA = 'ONEZONE_IA'
    INTELLIGENT_TIERING = 'INTELLIGENT_TIERING'
    GLACIER = 'GLACIER'  # 归档存储
    DEEP_ARCHIVE = 'DEEP_ARCHIVE'  # 深度归档存储
    OUTPOSTS = 'OUTPOSTS'


class BceStorageClass(BaseStorageClass):
    """
    百度云 storage_class的类型有：STANDARD, STANDARD_IA, MAZ_STANDARD, MAZ_STANDARD_IA, COLD, ARCHIVE
    """
    MAZ_STANDARD = 'MAZ_STANDARD'
    MAZ_STANDARD_IA = 'MAZ_STANDARD_IA'
    COLD = 'COLD'  # 对应归档存储，相当于GLACIER
    ARCHIVE = 'ARCHIVE'  # 对应深度归档存储，相当于DEEP_ARCHIVE


S3_ARCHIVE_CLASS_LIST = [S3StorageClass.GLACIER, S3StorageClass.DEEP_ARCHIVE, BceStorageClass.COLD,
                         BceStorageClass.ARCHIVE]


def exception_handler(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = config.get_logger(_DEFAULT_LOGGER_NAME)

        try:
            return func(*args, **kwargs)
        except boto_exc.ClientError as e:
            status_code = e.response.get('ResponseMetadata').get('HTTPStatusCode')
            details = e.response.get('Error')
            code = details.get('Code')
            message = details.get('Message')
            if status_code == 404:
                logger.debug("s3 not found error", exc_info=1)
                if code == 'NoSuchBucket':
                    raise err.NoSuchContainer(details.get('BucketName'), **details)
                elif code == 'NoSuchKey':
                    raise err.NoSuchObject(details.get('Key'), **details)
                else:
                    raise err.NotFound(message, **details)
            elif status_code == 403:
                logger.debug('s3 server error', exc_info=1)
                raise err.Forbidden(message, **details)
            elif status_code == 400:
                logger.debug('s3 request error', exc_info=1)
                raise err.BadRequest(message, **details)
            else:
                raise err.DriverServerException(message, status_code, code=code, **details)
        except (boto_exc.BotoCoreError, bos_exc.BceError) as e:
            logger.debug('s3 error', exc_info=1)
            raise err.StorageDriverException('unknown s3 error: {}'.format(e))

    return wrapper


class S3Connection(base.Connection):
    def __init__(self, host, port, credential, region_name=None, s3_sign_vers=None, **kwargs):
        super(S3Connection, self).__init__(
            host=host,
            port=port,
            credential=credential
        )
        self.service_name = 's3'
        self._client = None
        self.s3_sign_vers = s3_sign_vers or DEFAULT_S3_SIGN_VERSION
        self.region_name = region_name

    def clone(self):
        return S3Connection(
            host=self.host,
            port=self.port,
            credential=self.credential,
            region_name=self.region_name,
            s3_sign_vers=self.s3_sign_vers
        )

    def get_client(self, container_name):
        """
        获取S3客户端（S3 client instance),可调用 boto api
        :param container_name: 对应bucket_name
        :return: 返回client
        :rtype: :class:`botocore.client.S3`
        """
        if not self._client:
            access_key_token = self.credential.access_key_token
            access_key_id = self.credential.access_key_id
            access_key_secret = self.credential.access_key_secret
            config = Config(signature_version=self.s3_sign_vers)

            if not access_key_token:
                self._client = boto3.client(self.service_name,
                                            region_name=self.region_name,
                                            aws_access_key_id=access_key_id,
                                            aws_secret_access_key=access_key_secret,
                                            config=config,
                                            endpoint_url=self.host)
            else:
                self._client = boto3.client(self.service_name,
                                            region_name=self.region_name,
                                            aws_access_key_id=access_key_id,
                                            aws_secret_access_key=access_key_secret,
                                            aws_session_token=access_key_token,
                                            config=config,
                                            endpoint_url=self.host)
        return self._client

    def close(self):
        self._client = None


class S3StorageDriver(base.StorageDriver):
    connection_class = S3Connection
    checksum_type = 'md5'

    def __init__(self):
        super(S3StorageDriver, self).__init__()

    @exception_handler
    def get_object_meta(self, connection, object_name, container_name):
        """
        获取object的详细信息
           *  name
           *  size
           *  extra
                * last_modified:    最后修改时间，ISO 8601格式
                * etag：            s3附带的etag信息
                * storage_class:    对象的存储类型： 'STANDARD','GLACIER','DEEP_ARCHIVE'...
                * restore_status:   '' / restoring / restored
                * expiry_date:      归档文件恢复的过期时间，ISO 8601格式

        :param connection: `S3Connection` instance
        :type  connection: :class:`S3Connection`

        :param object_name: 对象名称
        :type  object_name: `str`

        :param container_name: bucket name
        :type  container_name: :class:`str`

        :return: 返回Object meta信息
        :rtype: :class:``gddriver.models.Object``
        """
        s3_client = connection.get_client(container_name)
        meta = s3_client.head_object(Bucket=container_name, Key=object_name)
        storage_class, restore_status, expiry_date = self.get_restore_status(meta)
        last_modified = meta.get('LastModified')
        extra = {
            "etag": meta.get('ETag'),
            "last_modified": last_modified,
            "storage_class": storage_class,
            "restore_status": restore_status,
            "expiry_date": expiry_date
        }
        content_length = meta.get('ContentLength')
        return models.Object(object_name, content_length, **extra)

    @exception_handler
    def list_container_objects(self, connection, container_name, prefix=None,
                               marker='', max_objects=DEFAULT_LIST_OBJECTS):
        """
        列出容器中的object

        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param container_name: bucket name
        :type  container_name: :class:`str`

        :param prefix: 文件的前缀（S3中没有真正的目录的概念）
        :type  prefix: :class:`str`

        :param marker:  上一次遍历的标记，若marker不为None，则继续上一次标记遍历
        :type  marker: :class:`str`

        :param max_objects: 每次list返回的Object数目限制，最大可设置为1000
        :type  max_objects:  :class:`int`

        :return: object-meta列表, 下一次继续遍历的标记.
        :rtype: ``list`` of :class:`Object` | ``str``
        """
        _max_objects = max_objects if max_objects < LIST_DATA_MAX_OBJECTS else LIST_DATA_MAX_OBJECTS
        prefix = prefix or ''
        s3_client = connection.get_client(container_name)
        result = s3_client.list_objects(
            Bucket=container_name,
            Prefix=prefix,
            Marker=marker,
            MaxKeys=_max_objects,
        )
        is_truncated = result.get('IsTruncated')
        next_marker = None

        objects = []
        for meta in result.get('Contents', []):
            last_modified = meta.get('LastModified')
            extra = {
                "etag": meta.get('ETag'),
                "last_modified": last_modified,
                "storage_class": meta.get('StorageClass')
            }
            objects.append(models.Object(meta.get('Key'), meta.get('Size'), **extra))

        if is_truncated:
            next_marker = objects[-1].name
        return objects, next_marker

    @exception_handler
    def download_object_as_stream(self, connection, request):
        """
        流式下载，获取一个可读的文件流
        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param request: 流式下载请求
        :type  request: gddriver.models.S3StreamDownloadRequest

        :return: 返回的StreamDownloadResult是一个流，属性中默认包含从server端获取的md5
        :rtype: :class:``StreamDownloadResult``
        """
        logger = self.logger
        buffer_size = request.buffer_size
        container_name = request.container_name
        object_name = request.object_name
        progress_callback = request.progress_callback

        byte_range = request.byte_range if hasattr(request, 'byte_range') else None

        buffer_size = buffer_size or DEFAULT_DOWNLOAD_BUFFER_SIZE
        object_meta = self.get_object_meta(connection, object_name, container_name)
        object_size = object_meta.size
        if not byte_range:
            byte_range = (0, object_size - 1)
        data_size = get_range_size(object_size, byte_range)
        range_str = _make_range_string(byte_range)

        s3_client = connection.get_client(container_name)
        result = s3_client.get_object(Bucket=container_name,
                                      Key=object_name,
                                      Range=range_str)

        server_checksum = result.get('ETag')
        stream = result.get('Body')
        msg_template = ("download object as stream, bucket={}, object-key={}, "
                        "object-size={}, server-md5={}, buffer-size={}")
        msg = msg_template.format(container_name, object_name, object_size, server_checksum, buffer_size)
        logger.debug(msg)

        stopwatch = timeutil.Stopwatch()
        stopwatch.start()

        def generator():
            while True:
                chunk = stream.read(buffer_size)
                if not chunk:
                    break
                yield chunk
            logger.debug("%s, elapsed=%s, download finished", msg, stopwatch.elapsed())

        checksum_type = 'md5'
        stream_generator = generator()
        wrapped_stream = ioutil.make_progress_adapter(stream_generator, progress_callback, data_size)
        checksum_wrapped_stream = ioutil.make_checksum_adapter(wrapped_stream, checksum_type)
        result = models.StreamDownloadResult(
            iterator=checksum_wrapped_stream,
            length=data_size,
            server_checksum=server_checksum,
            checksum_type=checksum_type
        )
        return result

    @exception_handler
    def download_file(self, connection, request):
        """
        下载文件到指定的路径中

        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param request: 流式下载请求
        :type  request: gddriver.models.S3DownloadRequest

        """
        container_name = request.container_name
        object_name = request.object_name
        local_file_path = request.file_path
        threads_count = request.threads_count
        progress_callback = request.progress_callback

        msg_template = ("multipart download, bucket={container_name}, object-key={object_name}, "
                        "dst-path={file_path}, threads_count={threads_count}")
        msg = msg_template.format(
            container_name=container_name,
            object_name=object_name,
            file_path=local_file_path,
            threads_count=threads_count
        )
        self.logger.debug(msg)

        stopwatch = timeutil.Stopwatch()
        stopwatch.start()

        s3_client = connection.get_client(container_name)
        config = TransferConfig(
            max_concurrency=threads_count,
            num_download_attempts=2,
        )
        s3_client.download_file(
            Bucket=container_name,
            Key=object_name,
            Filename=local_file_path,
            Callback=progress_callback,
            Config=config
        )
        self.logger.info("%s, elapsed=%s, download finished", msg, stopwatch.elapsed())

    @exception_handler
    def upload_object_via_stream(self, connection, request):
        """
        流式上传，可以上传网络流、文件流、字符串、bytes等可迭代的对象。
        分片上传时，每个分片至少5Mb,否则会报错:
        e.g 400 Your proposed upload is smaller than the minimum allowed size  details

        :param connection: `S3Connection` 实例
        :type  connection: :class:`S3Connection`

        :param request:
        :type  request: `gddriver.models.S3StreamUploadRequest`

        :rtype: :class:``gddriver.models.UploadResult``
        """

        container_name = request.container_name
        object_name = request.object_name
        stream = request.stream
        progress_callback = request.progress_callback

        data_size = request.data_size
        # 这是因为流式上传时，无法感知这个流的实际大小，默认会使用常规的put_object
        # 上传，但这种方式最大只能上传5GB文件，超过5GB必须使用分片上传，所以用户在知道
        # 文件流较大时，可以使用multi参数通知driver使用分片上传
        multi = request.multi if hasattr(request, 'multi') else False

        logger = self.logger
        msg_template = ("upload via stream, bucket={container_name}, object-key={object_name}, "
                        "checksum-type={checksum_type}, data-size={data_size}, multi={multi}")
        msg = msg_template.format(
            container_name=container_name,
            object_name=object_name,
            checksum_type=self.checksum_type,
            data_size=data_size,
            multi=multi
        )
        stopwatch = timeutil.Stopwatch()
        stopwatch.start()

        logger.debug(msg)

        wrapped_stream = ioutil.make_progress_adapter(stream, progress_callback, data_size)

        s3_client = connection.get_client(container_name)
        if not multi:
            if not hasattr(wrapped_stream, 'read'):
                body = next(wrapped_stream)
            else:
                body = wrapped_stream
            s3_result = s3_client.put_object(
                Key=object_name,
                Body=body,
                Bucket=container_name,
            )
            try:
                next(wrapped_stream)
            except Exception as e:
                pass
        else:
            # 分片上传
            logger.debug("%s, via multipart mode", msg)
            upload_id = s3_client.create_multipart_upload(Bucket=container_name, Key=object_name).get('UploadId')
            # parts = self._upload_parts(
            #     upload_id,
            #     wrapped_stream,
            #     container_name,
            #     object_name,
            #     s3_client
            # )
            parts = []
            part_num = 0
            for chunk in wrapped_stream:
                part_num += 1
                response = s3_client.upload_part(
                    Body=chunk,
                    Bucket=container_name,
                    Key=object_name,
                    UploadId=upload_id,
                    PartNumber=part_num
                )
                etag = response['ETag']
                parts.append({'ETag': etag, 'PartNumber': part_num})
            s3_result = s3_client.complete_multipart_upload(
                    Bucket=container_name,
                    Key=object_name,
                    UploadId=upload_id,
                    MultipartUpload={"Parts": parts}
                )
        logger.debug(s3_result)
        # s3上传成功后没有显式返回数据的md5或者crc校验值，这里使用etag作为校验
        # put_object的etag为内容的md5值，分片上传方式是将没块分片的md5值以字节形式相加之和计算md5值
        # 并以'-'拼接分片数量 e.g '3e2c20a209064f33d1760456fc0b5423-4'，s3存储返回的etag
        # -98f2c5eb21f7bafed7c355d07c59d1b8   百度云存储返回的etag
        server_checksum = s3_result.get('ETag')
        extra = self.__get_extra_info(s3_result)
        # extra添加multi信息,区分put_object校验还是multipart_upload校验
        extra['multi'] = multi
        result = models.UploadResult(
            checksum=server_checksum,
            checksum_type=self.checksum_type,
            **extra
        )
        logger.info('%s, checksum=%s, elapsed=%s, upload finished',
                    msg, result.checksum, stopwatch.elapsed())
        return result

    @exception_handler
    def upload_file(self, connection, request):
        """
        分片多线程上传一个文件

        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param request:
        :type  request: `gddriver.models.S3UploadRequest`

        :return:
        :rtype `UploadResult`
        """
        container_name = request.container_name
        file_path = request.file_path
        object_name = request.object_name
        threads_count = request.threads_count
        progress_callback = request.progress_callback

        part_size = request.part_size if hasattr(request, 'part_size') else None
        logger = self.logger
        msg_template = ("multipart upload, file={file_path}, bucket={container_name}, object-key={object_name}, "
                        "threads_count={threads_count}, part-size={part_size}, checksum-type={checksum_type}")
        msg = msg_template.format(
            file_path=file_path,
            container_name=container_name,
            object_name=object_name,
            threads_count=threads_count,
            part_size=part_size,
            checksum_type=self.checksum_type
        )
        logger.debug(msg)

        stopwatch = timeutil.Stopwatch()
        stopwatch.start()

        s3_client = connection.get_client(container_name)
        config = TransferConfig(
            max_concurrency=threads_count,
            num_download_attempts=1,
            multipart_chunksize=part_size if part_size else DEFAULT_SIZE_PER_PART,
            multipart_threshold=DEFAULT_MULTIPART_TRANSFER_THRESHOLD
        )

        s3_transfer = S3Transfer(client=s3_client, config=config)
        s3_result = s3_transfer.upload_file(file_path, container_name, object_name, progress_callback)
        server_checksum = s3_result.get('ETag')
        extra = self.__get_extra_info(s3_result)
        result = models.UploadResult(
            checksum=server_checksum,
            checksum_type=self.checksum_type,
            **extra
        )
        logger.info('%s, checksum=%s, elapsed=%s, upload finished',
                    msg, result.checksum, stopwatch.elapsed())
        return result

    @exception_handler
    def delete_object(self, connection, object_name, container_name=None):
        """
        :param connection: `S3Connection`
        :type connection: :class:`S3Connection`

        :param object_name:
        :type  object_name: str

        :param container_name:
        :type container_name: str
        """
        s3_client = connection.get_client(container_name)
        s3_client.delete_object(Bucket=container_name, Key=object_name)

    @exception_handler
    def copy_object(self, connection, request):
        """
         :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param request: 对象复制请求
        :type  request: :class:``gddriver.models.S3CopyRequest``
        :return:
        """
        logger = self.logger

        src_container_name = request.container_name
        src_object_name = request.object_name
        # 默认复制到当前容器中
        dst_container_name = request.dst_container_name or src_container_name
        dst_object_name = request.dst_object_name
        storage_class = request.storage_class or DEFAULT_STORAGE_CLASS

        # 兼容基类的参数
        multi_threshold = request.multi_threshold if hasattr(request, 'multi_threshold') else None
        final_threshold = multi_threshold or DEFAULT_MULTIPART_TRANSFER_THRESHOLD

        object_meta = self.get_object_meta(connection, src_object_name, src_container_name)

        msg_template = ("copy object, from={src_container_name}:{src_object_name}, "
                        "to={dst_container_name}:{dst_object_name}, size={size}")
        msg = msg_template.format(
            src_container_name=src_container_name,
            src_object_name=src_object_name,
            dst_container_name=dst_container_name,
            dst_object_name=dst_object_name,
            size=object_meta.size
        )

        s3_client = connection.get_client(dst_container_name)
        if object_meta.size <= final_threshold:
            logger.debug(msg)
            s3_client.copy_object(
                Bucket=dst_container_name,
                CopySource={'Bucket': src_container_name, 'Key': src_object_name},
                Key=dst_object_name,
                StorageClass=storage_class,
            )
        else:
            stopwatch = timeutil.Stopwatch()
            stopwatch.start()
            # 文件较大时，使用分片复制
            create_upload_result = s3_client.create_multipart_upload(
                Bucket=dst_container_name,
                Key=dst_object_name,
                StorageClass=storage_class
            )
            upload_id = create_upload_result.get('UploadId')
            part_size = regulate_part_size(object_meta.size)

            logger.debug("%s, multipart copy, upload-id=%s, part-size=%s", msg, upload_id, part_size)
            parts, offset = self._copy_parts(
                s3_client,
                part_size,
                object_meta.size,
                upload_id,
                src_container_name,
                src_object_name,
                dst_container_name,
                dst_object_name
            )
            logger.info("%s %s copied  elapsed=%s, finished", msg, offset, stopwatch.elapsed())
            s3_client.complete_multipart_upload(
                Bucket=dst_container_name,
                Key=dst_object_name,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts}
            )

    @exception_handler
    def batch_delete_objects(self, connection, object_name_list, container_name):
        """批量删除文件。

        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param container_name: bucket name
        :type  container_name: :class:`str`

        :param object_name_list:
        :type object_name_list: list of str

        """
        logger = self.logger
        logger.debug('batch delete objects, %s', object_name_list)
        if not object_name_list:
            logger.warning('object key list is None')

        s3_client = connection.get_client(container_name)
        objects = [{u'Key': key} for key in object_name_list]
        batch_delet_result = s3_client.delete_objects(
            Bucket=container_name,
            Delete={
                'Objects': objects
            }
        )
        assert batch_delet_result['Deleted'] == objects
        logger.info('batch delete objects, result=%s', batch_delet_result)

    @exception_handler
    def archive_object(self, connection, src_container_name, src_object_name,
                       archive_container_name, archive_object_name, delete=False):
        """
        将文件从一个bucket中转归档到另一个bucket中，并删除原来的文件，适合不同类型的bucket之间的复制

        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param src_container_name: 原数据的bucket name
        :param src_object_name: 原数据的object_key
        :param archive_container_name: 要归档至的bucket name
        :param archive_object_name: 归档后的object key
        :param delete: 是否在归档完成后删除原文件
        """
        _bos_url_suffix = 'bcebos.com'
        _aws_url_suffix = 'amazonaws.com'

        if connection.host.endswith(_bos_url_suffix):
            storage_class = BceStorageClass.ARCHIVE
        elif connection.host.endswith(_aws_url_suffix):
            storage_class = S3StorageClass.GLACIER
        else:
            raise NotImplementedError

        self.__copy_object_between_buckets(
            connection=connection,
            src_bucket_name=src_container_name,
            src_obj_key=src_object_name,
            dst_bucket_name=archive_container_name,
            dst_obj_key=archive_object_name,
            storage_class=storage_class
        )
        if delete:
            self.delete_object(
                connection=connection,
                object_name=src_object_name,
                container_name=src_container_name)

    @exception_handler
    def restore_object(self, connection, src_container_name, src_object_name):
        """
        将低频存储类型暂时恢复为可访问的类型
        :param connection: `S3Connection`
        :param src_container_name: 原数据的bucket name
        :param src_object_name: 原数据的object_key
        :rtype: :class:``gddriver.models.RestoreResult``
        """
        _bos_url_suffix = 'bcebos.com'
        _aws_url_suffix = 'amazonaws.com'

        from baidubce import exception as bce_exs

        def get_bos_client(connection):
            """Get bos client
            :rtype :class:``baidubce.services.bos.bos_client.BosClient``
            """
            from baidubce.bce_client_configuration import BceClientConfiguration
            from baidubce.auth.bce_credentials import BceCredentials
            from baidubce.services.bos.bos_client import BosClient
            bos_host = '.'.join(connection.host.split('.')[-3:])
            access_key_id = connection.credential.access_key_id
            secret_access_key = connection.credential.access_key_secret
            config = BceClientConfiguration(credentials=BceCredentials(access_key_id, secret_access_key),
                                            endpoint=bos_host)
            bos_client = BosClient(config)
            return bos_client

        def get_restore_status(s3_client):
            meta = s3_client.head_object(Bucket=src_container_name, Key=src_object_name)
            _, restore_status, expiry_date = self.get_restore_status(meta)
            finished = restore_status == 'restored'
            return finished, expiry_date

        s3_client = connection.get_client(container_name=src_container_name)
        if connection.host.endswith(_aws_url_suffix):
            # aws
            try:
                self.logger.debug('restore: %s start', src_object_name)
                rsp = s3_client.restore_object(
                    Bucket=src_container_name,
                    Key=src_object_name,
                    RestoreRequest={
                        'Days': 1,
                        'GlacierJobParameters': {
                            'Tier': 'Standard',
                        },
                    },
                )
                if rsp['ResponseMetadata']['HTTPStatusCode'] == 202:
                    return models.RestoreResult(finished=False)
            except boto_exc.ClientError as e:
                code = e.response['Error']['Code']
                if code == 'RestoreAlreadyInProgress':
                    self.logger.info("restore already in process: %s/%s", src_container_name, src_object_name)
                    return models.RestoreResult(finished=False)
                else:
                    raise
            finished, expiry_date = get_restore_status(s3_client)
        elif connection.host.endswith(_bos_url_suffix):
            # bos
            bos_client = get_bos_client(connection)
            try:
                bos_client.restore_object(src_container_name, src_object_name, days=1)
                finished, expiry_date = get_restore_status(s3_client)
            except bce_exs.BceError as e:
                if hasattr(e.last_error, 'code') and e.last_error.code == 'RestoreAlready':
                    finished, expiry_date = get_restore_status(s3_client)
                else:
                    raise
        else:
            # ceph
            raise NotImplementedError

        return models.RestoreResult(
            finished=finished,
            expiry_date=expiry_date
        )

    @exception_handler
    def move_object(self, connection, src_object_name, dst_object_name,
                    container_name=None, dst_container_name=None):
        """
         将object移动到另一路径（不支持从标准存储向低频存储中移动，如有需要，则使用archive_object），

        :param connection: `S3Connection`
        :type  connection: :class:`S3Connection`

        :param container_name: 原数据的bucket name
        :param src_object_name: 原数据的object_key
        :param dst_object_name: 要归档至的bucket name
        :param dst_container_name: 归档后的object key
        """
        msg = ("move object, from={src_bucket_name}:{src_obj_key}, "
               "to={dst_bucket_name}:{dst_obj_key}").format(
            src_bucket_name=container_name,
            src_obj_key=src_object_name,
            dst_bucket_name=dst_container_name,
            dst_obj_key=dst_object_name
        )

        copy_request = models.S3CopyRequest(
            container_name=container_name,
            object_name=src_object_name,
            dst_container_name=dst_container_name or container_name,
            dst_object_name=dst_object_name
        )

        self.copy_object(connection, copy_request)
        self.delete_object(
            connection=connection,
            container_name=container_name,
            object_name=src_object_name
        )

    @exception_handler
    def get_object_sign_url(self, connection, object_name, container_name=None, expires=DEFAULT_URL_EXPIRES):
        s3_client = connection.get_client(container_name)
        expires = expires or DEFAULT_URL_EXPIRES
        url = s3_client.generate_presigned_url(
            ClientMethod='get_object',
            Params={
                'Bucket': container_name,
                'Key': object_name
            },
            ExpiresIn=expires
        )
        return url

    @exception_handler
    def init_multipart_upload(self, connection, object_name, container_name=None, overwrite=False):
        """
        :param connection:
        :type connection: OSSConnection
        :param object_name:
        :param container_name:
        :param overwrite: 默认直接覆盖上传，如非覆盖，则抛出文件已存在的异常
        :return:
        """

        if not overwrite:
            try:
                self.get_object_meta(connection, object_name, container_name)
                raise err.FileAlreadyExists('{} already exists'.format(object_name))
            except err.NotFound:
                pass

        s3_client = connection.get_client(container_name)
        result = s3_client.create_multipart_upload(
            Bucket=container_name,
            Key=object_name,
        )
        self.logger.debug(result)

        return result['UploadId']

    @exception_handler
    def upload_part(self, connection, request):
        s3_client = connection.get_client(request.container_name)
        s3_resp = s3_client.upload_part(
            Body=request.stream,
            Bucket=request.container_name,
            Key=request.object_name,
            UploadId=request.upload_id,
            PartNumber=request.part_number
        )
        return models.PartUploadResult(
            checksum=s3_resp['ETag'],
            checksum_type='md5',
            part_info=models.PartInfo(part_number=request.part_number, etag=s3_resp['ETag'])
        )

    @exception_handler
    def complete_multipart_upload(self, connection, request):

        def map_to_s3_part_info(part):
            """
            :type part: gddriver.models.PartInfo
            """
            return {
                'ETag': part.etag,
                'PartNumber': part.part_number
            }

        s3_client = connection.get_client(request.container_name)
        parts = map(map_to_s3_part_info, request.parts)
        parts.sort(key=lambda part: part['PartNumber'])
        s3_result = s3_client.complete_multipart_upload(
            Bucket=request.container_name,
            Key=request.object_name,
            UploadId=request.upload_id,
            MultipartUpload={"Parts": parts}
        )
        self.logger.debug(s3_result)

    def __copy_object_between_buckets(self, connection, src_bucket_name, src_obj_key,
                                      dst_bucket_name, dst_obj_key, storage_class):

        msg = ("copy between buckets, from={src_bucket_name}:{src_obj_key}, "
               "to={dst_bucket_name}:{dst_obj_key}").format(
            src_bucket_name=src_bucket_name,
            src_obj_key=src_obj_key,
            dst_bucket_name=dst_bucket_name,
            dst_obj_key=dst_obj_key
        )
        self.logger.debug(msg)
        copy_request = models.S3CopyRequest(
            container_name=src_bucket_name,
            object_name=src_obj_key,
            dst_container_name=dst_bucket_name,
            dst_object_name=dst_obj_key
        )
        copy_request.storage_class = storage_class
        self.copy_object(connection, copy_request)

    @staticmethod
    def __get_extra_info(result):
        """
        :param result: s3 api请求的返回值
        :rtype: dict
        """
        return {'request_id': result.get('ResponseMetadata').get('RequestId'), 'etag': result.get('ETag')}

    @classmethod
    def get_restore_status(cls, meta):
        """
        通过meta获取restore的状态信息
        :param meta: meta of head_object
        :type meta: dict
        :return: 存储类型， restore状态， 过期时间
        :rtype: str | str | datetime.datetime
        """
        storage_class, restore, finished, expiry_date = cls.__get_restored_info(meta)
        # 普通文件
        if storage_class not in S3_ARCHIVE_CLASS_LIST:
            return storage_class, '', None
        # archived
        elif not restore:
            return storage_class, 'archived', None
        # restoring or restored
        elif finished:
            return storage_class, 'restored', expiry_date
        else:
            return storage_class, 'restoring', None

    @classmethod
    def __get_restored_info(cls, meta):
        """
        当文件非restoring或restored状态的文件，返回的第二个参数restore 为False，
        is_finished 为False，expiry_date 为None

        :param meta: meta of head_object
        :return: storage_class, is_restore_object, is_finished_restore, expiry
        """
        finished = False
        restore = False
        expiry_date = None

        # 如果Bucket类型为GLACIER，且用户已经提交Restore请求，则响应头中会以x-amz-restore返回该Object的Restore状态，分如下几种情况：
        #     a.如果没有提交Restore或者Restore已经超时，则不返回该字段。
        #     b.如果已经提交Restore，且Restore没有完成时，则返回的x-amz-restore值为: ongoing-request ="true"。
        #     c.如果已经提交Restore，且Restore已经完成，
        #       则返回的x-amz-restore值为: x-amz-restore: ongoing-request="false", expiry-date="Fri, 23 Dec 2012 00:00:00 GMT"。

        # x-amz-storage-class展示Object的存储类型：'STANDARD','REDUCED_REDUNDANCY','STANDARD_IA','ONEZONE_IA',
        # 'INTELLIGENT_TIERING','GLACIER','DEEP_ARCHIVE','OUTPOSTS'
        # 与百度云兼容，新增类型：COLD, ARCHIVE
        storage_class = meta.get('StorageClass')
        if not storage_class:
            # 当文档类型是STANDARD时，不会返回storageclass
            storage_class = BaseStorageClass.STANDARD
        if storage_class not in S3_ARCHIVE_CLASS_LIST:
            return storage_class, restore, finished, expiry_date

        # 状态为restoring的文件，meta中包含信息 'x-amz-restore'为True，
        # 同时也可以从meta中获取： meta.get('Restore')
        restore_progress = meta.get('Restore') or meta['ResponseMetadata']['HTTPHeaders'].get('x-bce-restore')
        if not restore_progress:
            return storage_class, restore, finished, expiry_date
        else:
            restore = True

        if 'true' not in restore_progress:
            # x-amz-restore: ongoing-request="false", expiry-date="Sun, 16 Apr 2017 08:12:33 GMT"
            # x-bce-restore: 'ongoing-request="false", expiry-date="Sun, 31 Jan 2021 08:22:23 GMT"'
            finished = True
            restore = True
            expiry_time = cls.get_expiry_time(restore_progress)
            expiry_date = timeutil.timestamp_to_date(expiry_time)

        return storage_class, restore, finished, expiry_date

    @classmethod
    def get_expiry_time(cls, restore_progress):
        """Get restore expiry time from restore progress string

        :param restore_progress: e.g. ongoing-request="false", expiry-date="Sun, 16 Apr 2017 08:12:33 GMT"
        :return Unix 时间戳
        """
        expiry_date_str = restore_progress.split(',', 1)[1]
        expiry_date_str = expiry_date_str.replace(' expiry-date="', '').replace('"', '')
        expiry_time = timeutil.http_to_unixtime(expiry_date_str)
        return expiry_time

    def _upload_parts(self, upload_id, stream, container_name, object_name, client):
        parts = []
        with ThreadPoolExecutor() as executor:
            part_num = 0
            all_task = []
            for chunk in stream:
                part_num += 1
                task = executor.submit(
                    self._upload_part,
                    upload_id,
                    container_name,
                    object_name,
                    client,
                    part_num,
                    chunk
                )
                all_task.append(task)

        for future in as_completed(all_task):
            data = future.result()
            parts.append(data)
        parts.sort(key=lambda part: part['PartNumber'])
        return parts

    @staticmethod
    def _upload_part(upload_id, container_name, object_name, client, part_num, chunk):
        response = client.upload_part(
            Body=chunk,
            Bucket=container_name,
            Key=object_name,
            UploadId=upload_id,
            PartNumber=part_num
        )
        etag = response['ETag']
        return {'ETag': etag, 'PartNumber': part_num}

    def _copy_parts(self, client, part_size, total_size, upload_id, src_container_name,
                    src_object_name, dst_container_name, dst_object_name):
        parts = []
        part_number = 1
        offset = 0
        all_task = []

        with ThreadPoolExecutor() as executor:
            while offset < total_size:
                parts_to_upload = min(part_size, total_size - offset)
                # 左闭右闭
                byte_range = (offset, offset + parts_to_upload - 1)
                byte_range_str = _make_range_string(byte_range)

                task = executor.submit(
                    self._copy_part,
                    client,
                    src_container_name,
                    src_object_name,
                    dst_container_name,
                    dst_object_name,
                    part_number,
                    byte_range_str,
                    upload_id
                )
                offset += parts_to_upload
                part_number += 1
                all_task.append(task)

        for future in as_completed(all_task):
            data = future.result()
            parts.append(data)
        parts.sort(key=lambda part: part['PartNumber'])
        return parts, offset

    @staticmethod
    def _copy_part(client, src_container_name, src_object_name,
                   dst_container_name, dst_object_name, part_number, byte_range_str, upload_id):

        part_copy_result = client.upload_part_copy(
            Bucket=dst_container_name,
            CopySource={'Bucket': src_container_name, 'Key': src_object_name},
            CopySourceRange=byte_range_str,
            Key=dst_object_name,
            PartNumber=part_number,
            UploadId=upload_id
        )
        return {
            'ETag': part_copy_result['CopyPartResult']['ETag'],
            'PartNumber': part_number
        }


class S3Transfer(object):
    def __init__(self, client, config=None, executor_cls=ThreadPoolExecutor):
        self._client = client
        if config is None:
            config = TransferConfig()
        self._config = config
        self._executor_cls = executor_cls

    def upload_file(self, file_path, bucket, key, callback=None):
        if os.path.getsize(file_path) >= self._config.multipart_threshold:
            s3_result = self._multipart_upload(file_path, bucket, key, callback)
        else:
            s3_result = self._put_object(file_path, bucket, key, callback)
        return s3_result

    def _multipart_upload(self, file_path, bucket, key, callback=None):
        response = self._client.create_multipart_upload(Bucket=bucket, Key=key)
        upload_id = response['UploadId']
        parts = self._upload_parts(upload_id, file_path, bucket, key, callback)
        return self._client.complete_multipart_upload(
            Bucket=bucket,
            Key=key,
            UploadId=upload_id,
            MultipartUpload={'Parts': parts}
        )

    def _upload_parts(self, upload_id, file_path, bucket, key, callback=None):
        parts = []
        part_size = self._config.multipart_chunksize
        num_parts = int(math.ceil(os.path.getsize(file_path) / float(part_size)))
        max_workers = self._config.max_concurrency

        with self._executor_cls(max_workers=max_workers) as executor:
            upload_partial = functools.partial(
                self._upload_one_part, file_path, bucket, key, upload_id,
                part_size, callback)
            for part in executor.map(upload_partial, range(1, num_parts + 1)):
                parts.append(part)
        return parts

    @staticmethod
    def open_file_chunk_reader(filename, start_byte, size, callback):
        return ReadFileChunk.from_filename(filename, start_byte,
                                           size, callback,
                                           enable_callback=True)

    def _upload_one_part(self, file_path, bucket, key, upload_id,
                         part_size, callback, part_number):
        open_chunk_reader = self.open_file_chunk_reader
        with open_chunk_reader(file_path, part_size * (part_number - 1),
                               part_size, callback) as body:
            response = self._client.upload_part(
                Bucket=bucket,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=body
            )
            etag = response['ETag']
            return {'ETag': etag, 'PartNumber': part_number}

    def _put_object(self, file_path, bucket, key, callback=None):
        open_chunk_reader = self.open_file_chunk_reader
        with open_chunk_reader(file_path, 0,
                               os.path.getsize(file_path), callback) as body:
            return self._client.put_object(
                Bucket=bucket,
                Key=key,
                Body=body
            )


def regulate_part_size(object_size):
    part_size = DEFAULT_SIZE_PER_PART
    while part_size * S3_MAX_PART_NUM < object_size:
        # part_size 按MB递增
        part_size += part_size
    return part_size


def get_range_size(object_size, byte_range):
    """下载范围: (left, right)
        - byte_range 为 (0, 99)  -> 'bytes=0-99'，表示读取前100个字节
        - byte_range 为 (None, 99) -> 'bytes=-99'，表示读取最后99个字节
        - byte_range 为 (100, None) -> 'bytes=100-'，表示读取第101个字节到文件结尾的部分（包含第101个字节）
    """
    if not byte_range:
        return object_size
    left = byte_range[0]
    right = byte_range[1]
    if left == 0 and right > 0:
        return right - left + 1
    elif left is None and right > 0:
        return right
    elif left >= 0 and right is None:
        return object_size - left
    elif 0 <= left < right:
        return right - left + 1
    else:
        raise ValueError("illegal byte range")


def _make_range_string(range):
    """ convert byte_range to range_str
    下载范围: (left, right)
        - byte_range 为 (0, 99)  -> 'bytes=0-99'，表示读取前100个字节
        - byte_range 为 (None, 99) -> 'bytes=-99'，表示读取最后99个字节
        - byte_range 为 (100, None) -> 'bytes=100-'，表示读取第101个字节到文件结尾的部分（包含第101个字节）
    """
    if range is None:
        return ''

    start = range[0]
    last = range[1]

    if start is None and last is None:
        return ''

    return 'bytes=' + _range(start, last)


def _range(start, last):
    def to_str(pos):
        if pos is None:
            return ''
        else:
            return str(pos)

    return to_str(start) + '-' + to_str(last)


def calculate_multipart_etag(source_path, chunk_size, expected=None):
    """
    calculates a multipart upload etag for amazon s3
    Arguments:
    source_path -- The file to calculate the etage for
    chunk_size -- The chunk size to calculate for.
    Keyword Arguments:
    expected -- If passed a string, the string will be compared to the resulting etag and raise an exception if they don't match
    """

    import hashlib
    md5s = []

    with open(source_path, 'rb') as fp:
        while True:

            data = fp.read(chunk_size)

            if not data:
                break
            md5s.append(hashlib.md5(data))

    if len(md5s) > 1:
        digests = b"".join(m.digest() for m in md5s)
        new_md5 = hashlib.md5(digests)
        new_etag = '%s-%s' % (new_md5.hexdigest(), len(md5s))
    elif len(md5s) == 1:  # file smaller than chunk size
        new_etag = '%s' % md5s[0].hexdigest()
    else:  # empty file
        new_etag = ''

    if expected:
        if not expected == new_etag:
            raise ValueError('new etag %s does not match expected %s' % (new_etag, expected))

    return new_etag


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

