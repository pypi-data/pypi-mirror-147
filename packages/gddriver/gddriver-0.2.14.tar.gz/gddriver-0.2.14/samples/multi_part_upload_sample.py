# -*- coding: utf-8 -*-

from gddriver import Provider
from gddriver import transmission
from gddriver import models


container_name = "your bucket or ftp directory"

# FTP
# credential = models.Credential(
#     user="your ftp user name",
#     password="your ftp password"
# )
#
#
# operator = transmission.GenericOperator(
#     host="your ftp host",
#     port=21,  # fpt port
#     credential=credential,
#     provider=Provider.FTP,
#     ssl=False,  # open ssl, default false,
#     pasv=False  # pasv, default false
# )


# OSS
credential = models.Credential(
    access_key_id="your access key id",
    access_key_secret="your access key secret"
)

operator = transmission.GenericOperator(
    host="endpoint",
    credential=credential,
    port=None,
    provider=Provider.OSS
)


object_name = "gddriver-test/test-multi.1"
upload_id = operator.init_multipart_upload(container_name=container_name,
                                           object_name=object_name)

with open("Path to file", "rb") as f:
    part_num = 0
    parts = []
    while True:
        part_num += 1
        # oss 最小分片要求100KB
        c = f.read(1024 * 100)
        if not c:
            break

        part_upload_request = models.PartUploadRequest(
            container_name=container_name,
            stream=c,
            object_name=object_name,
            part_number=part_num,
            upload_id=upload_id
        )
        result = operator.upload_part(request=part_upload_request)
        # 等价
        # parts.append({"etag": result.part_info.etag, "part_number": result.part_info.part_number})
        parts.append(result.part_info)
    print("Parts: {}".format(parts))

    request = models.CompleteMultipartUploadRequest(
        container_name=container_name,
        object_name=object_name,
        upload_id=upload_id,
        parts=parts
    )
    operator.complete_multipart_upload(request=request)

