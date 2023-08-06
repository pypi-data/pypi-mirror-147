# -*- coding: utf-8 -*-
from gddriver.sts.base import TYPES
from gddriver.sts.oss import *
from gddriver.sts.s3 import *
from gddriver.sts.wcs import *
from gddriver import errors

# from gddriver.sts
_NAME_2_CLASS = {
    "oss": {
        TYPES.upload: OSSUpload,
        TYPES.download: OSSDownload,
        TYPES.delete: OSSDelete,
        TYPES.copy: OSSCopy,
        TYPES.list: OSSList,
    },
    "s3": {
        # 按照DataManager程序，现在只支持upload和download的sts，oss实现了但是没有用到
        TYPES.upload: S3Upload,
        TYPES.download: S3Download
    },
    "wcs": {
        TYPES.upload: WCSUpload,
        TYPES.download: WCSDownload
    }
}


def sts_factory(sts_type, store_protocol="", **kwargs):
    klass = _NAME_2_CLASS.get(store_protocol, {}).get(sts_type)
    if not klass:
        raise errors.UnsupportedSTSOperation(message="unsupported: %s" % sts_type)
    return klass(**kwargs)
