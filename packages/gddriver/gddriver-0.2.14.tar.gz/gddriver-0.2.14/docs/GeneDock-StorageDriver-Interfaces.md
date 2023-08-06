
## Object对象

Object对象只持有server端文件的基本信息

``` python

class Object(object):
    def __init__(self, name, size=0, **kwargs):
        """
        Operable object

        :param name: Object name (must be unique per container).
        :type  name: ``str``

        :param container: Object container.
        :type  container: :class:`Container`

        """
        self.name = name
        self.extra = {}
        self.size = size
        for key, value in kwargs.items():
            self.extra[key] = value

    def __str__(self):
        return 'name: {}, size: {}, extra: {}'.format(self.name, self.size, self.extra)


```

## Connection

Connection用于管理Storage server 的store_host, store_port, access_id, access_key等信息，对于不同的存储服务有不同的实现

``` python

class Connection(object):
    """
     Storage Server的连接信息，Driver执行操作时，通过connection信息完成服务认证
    """

    def __init__(self, host, port, access_id, access_key):
        self.host = host
        self.port = port
        self.access_id = access_id
        self.access_key = access_key

    def get_client(self, container=None):
        """
          获取认证后的连接
        """
        raise NotImplementedError(
            'get_client not implemented for this connection')
```

## 存储驱动

StorageDriver提供数据对象的基本操作（暂不提供容器的操作）：
* 上传
    * 上传本地文件
    * 通过流上传
    * 追加上传（追加上传只能以流的形式上传）
* 下载
    * 下载到本地文件
    * 以流的形式下载
* 删除
    * 删除对象
    * 通过前缀删除（部分实现）
    * 批量删除（部分实现）
* 冷备、恢复
* 获取前面链接
* iterate container
* list container

类函数：accept_connect  通过store_host等信息，初始化相应的Connection对象

StorageDriver中所有的操作都需要Connection，即使参数中未显式地传入，也通过Container或Object对象传入，在这里StorageDriver履行专一的工作，不管理用户的Connection信息

``` python

class StorageDriver(object):
    connection_class = Connection

    @classmethod
    def create_connection_manager(cls, store_host, store_port, access_id, access_key, **kwargs):
        """
        :param store_host:
        :param store_port:
        :param access_id:
        :param access_key:
        :return:
        """
        return cls.connection_class(store_host, store_port, access_id, access_key, **kwargs)

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_object_meta(self, connection, object_name, container_name=None):
        """
        Return an object instance.

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Container name.
        :type  container_name: ``str``

        :param object_name: Object name.
        :type  object_name: ``str``

        :return: :class:`Object` instance.
        :rtype: :class:`Object`
        """
        raise NotImplementedError(
            'get_object_meta not implemented for this driver')

    def upload_file(self, connection, file_path, container_name, object_name, checksum_type=None,
                    threads=None, progress_callback=None, **kwargs):
        """
        Upload an object currently located on a disk


        :param file_path: Path of the object on disk.
        :type file_path: ``str``

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param object_name: Object name.
        :type object_name: ``str``

        :param checksum_type: checksum type
        :type checksum_type: ``str``

        :param threads:
        :type threads: ``int``

        :param progress_callback: print transfer progress
        :type  progress_callback: ProgressCallback

        :rtype: ```UploadResult`
        """

        raise NotImplementedError(
            'upload_file not implemented for this driver')

    def upload_object_via_stream(self, connection, iterator, container_name, object_name, checksum_type=None,
                                 progress_callback=None, **kwargs):
        """
        Streaming upload

        :param iterator: must a file like object or an iterator
        :type iterator: ```object`

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param object_name: Object name.
        :type object_name: ``str``

        :param checksum_type: checksum type
        :type checksum_type: ``str``

        :param progress_callback: print transfer progress
        :type  progress_callback: ProgressCallback

        :rtype: ``UploadResult``
        """
        raise NotImplementedError(
            'upload_object_via_stream not implemented for this driver')

    def append_object(self, connection, iterator, container_name, object_name, position=0, checksum_type=None,
                      progress_callback=None, **kwargs):
        """
        Append an object using stream.

        :param iterator: a File like object with read method.
        :type iterator: :class:`object`

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param object_name: Object name.
        :type object_name: ``str``

        :param position: Start position. If it is a new append upload, position is 0
        :type position: ``long``

        :param checksum_type: checksum type
        :type checksum_type: ``str``

        :param progress_callback: print transfer progress
        :type  progress_callback: ProgressCallback

        :rtype: ``AppendResult``
        """
        raise NotImplementedError(
            'append_object_via_stream not implemented for this driver')

    def download_file(self, connection, container_name, object_name, dst_path, progress_callback=None, **kwargs):
        """
        Download an object to the specified destination path.

        :param object_name: Object name.
        :type object_name: `str`

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param dst_path: Full path to a file or a directory where the
                                 incoming file will be saved.
        :type dst_path: ``str``

        :param progress_callback: print transfer progress
        :type  progress_callback: ProgressCallback

        """
        raise NotImplementedError(
            'download_file not implemented for this driver')

    def download_object_as_stream(self, connection, container_name, object_name, chunk_size=None,
                                  progress_callback=None, **kwargs):
        """
        Return a generator which data in chunks.

        :param object_name: Object name.
        :type object_name: `str`

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param chunk_size: Optional chunk size (in bytes).
        :type chunk_size: ``int``

        :param progress_callback: print transfer progress
        :type  progress_callback: `ProgressCallback`

        :return: A generator of file chunk
        :rtype: :class:``StreamDownloadResult``

        """
        raise NotImplementedError(
            'download_object_as_stream not implemented for this driver')

    def copy_object(self, connection, src_container_name, src_obj_key, dst_obj_key, dst_container_name=None, **kwargs):
        """

        :param connection:
        :type  connection: :class:`Connection`

        :param src_obj_key:
        :type  src_obj_key:  `str`

        :param dst_obj_key:
        :type  dst_obj_key: `str`

        :param src_container_name:
        :type  src_container_name: `str`

        :param dst_container_name:
        :type  dst_container_name: `str`

        :return:
        """
        raise NotImplementedError(
            'copy_object not implemented for this driver')

    def archive_object(self, connection, src_container_name, src_object_name,
                       archive_container_name, dst_object_name, **kwargs):
        """
        :param connection:
        :type  connection: :class:`Connection`

        :param src_object_name:
        :type  src_object_name: :class:`str`

        :param src_container_name:
        :type  src_container_name: :class:`str`

        :param archive_container_name:
        :type  archive_container_name: :class:`str`

        :param dst_object_name:
        :type  dst_object_name: :class:`str`

        :rtype: `boolean`
        """
        raise NotImplementedError(
            'archive not implemented for this driver')

    def restore_object(self, connection, src_container_name, src_object_name, **kwargs):
        """
        :param connection:
        :type  connection: :class:`Connection`

        :param src_object_name:
        :type  src_object_name: :class:`str`

        :param src_container_name:
        :type  src_container_name: :class:`str`

        :rtype: :class:`RestoreResult`
        """
        raise NotImplementedError(
            'restore not implemented for this driver')

    def delete_object(self, connection, object_name, container_name=None):
        """
        :param container_name:
        :type container_name: `str`

        :param object_name: Object name.
        :type object_name: `str`

        :param connection: Destination container.
        :type connection: :class:`Connection`

        """
        raise NotImplementedError(
            'delete_object not implemented for this driver')

    def batch_delete_objects(self, connection, key_list, container_name=None):
        """
        Batch delete

        :param connection:
        :type  connection: :class:`Connection`

        :param key_list: not None
        :type key_list: list of str

        :param container_name:
        :type  container_name: :class:`str`

        """
        raise NotImplementedError(
            'batch_delete_objects not implemented for this driver')

    def iterate_container_objects(self, connection, container_name, prefix=None):
        """
        Return a generator of objects for the given container.

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param prefix:
        :type  prefix: :class:`str`

        :return: A generator of Object instances.
        :rtype: collections.Iterable[Object]
        """
        raise NotImplementedError(
            'iterate_container_objects not implemented for this driver')

    def list_container_objects(self, connection, container_name, prefix=None, **kwargs):
        """
        Return a list of objects for the given container.

        :param connection:
        :type  connection: :class:`Connection`

        :param container_name: Destination container.
        :type container_name: :class:`str`

        :param prefix:
        :type  prefix: :class:`str`

        :return: A list of Object instances, next_marker.
        :rtype: ``list`` of :class:`Object` | ``str``
        """
        raise NotImplementedError(
            'list_container_objects not implemented for this driver')

    def get_container(self, connection, container_name, **kwargs):
        """
         Return a list of objects for the given container.

         :param connection: Connection instance.
         :type connection: :class:`Connection`

         :param container_name:
         :type  container_name: :class:`str`

         :return: Container instances.
         :rtype: :class:`Container`
         """
        raise NotImplementedError(
            'list_container_objects not implemented for this driver')

    def get_object_sign_url(self, connection, object_name, container_name=None):
        raise NotImplementedError(
            'get_object_sign_url not implemented for this driver')

    def enable_object_cdn(self, connection, object_name, container_name=None, **kwargs):
        raise NotImplementedError(
            'enable_object_cdn not implemented for this driver')
```


## 其它模型

```python
class OperationResult(object):
    def __init__(self, **kwargs):
        self.extra = {}
        for key, value in kwargs.items():
            self.extra[key] = value

    def __str__(self):
        return "extra: " + str(self.extra)


class DownloadResult(OperationResult):
    def __init__(self, server_checksum=None, client_checksum=None, checksum_type=None, **kwargs):
        super(DownloadResult, self).__init__(**kwargs)
        self.__server_checksum = server_checksum
        self.__client_checksum = client_checksum
        self.__checksum_type = checksum_type

    @property
    def server_checksum(self):
        return self.__server_checksum

    @property
    def client_checksum(self):
        return self.__client_checksum

    @property
    def checksum_type(self):
        return self.__checksum_type

    def __str__(self):
        return 'server checksum: {}, client checksum: {}, ' \
               'checksum type: {}.'.format(self.server_checksum, self.client_checksum, self.checksum_type)


class StreamDownloadResult(DownloadResult):
    """
        iterable object
    """

    def __init__(self, iterator, **kwargs):
        super(StreamDownloadResult, self).__init__(**kwargs)
        self.iterator = iterator

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        return next(self.iterator)


class UploadResult(OperationResult):
    def __init__(self, checksum, checksum_type, **kwargs):
        super(UploadResult, self).__init__(**kwargs)
        self.__checksum = checksum
        self.__checksum_type = checksum_type

    def __str__(self):
        return "checksum: {}  type: {}  {}".format(self.checksum, self.checksum_type,
                                                   super(UploadResult, self).__str__())

    @property
    def checksum(self):
        return self.__checksum

    @property
    def checksum_type(self):
        return self.__checksum_type


class AppendResult(UploadResult):
    def __init__(self, next_position, **kwargs):
        super(AppendResult, self).__init__(**kwargs)
        self.next_position = next_position

    def __str__(self):
        return "next_position: {}  {}".format(self.next_position, super(AppendResult, self).__str__())
```