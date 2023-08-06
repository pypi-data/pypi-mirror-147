# -*- coding: utf-8 -*-
import datetime
import json
import sys

from gddriver.sts import models


class _Type(object):
    __slots__ = ()

    @property
    def upload(self):
        return models.STSActionType.UPLOAD

    @property
    def download(self):
        return models.STSActionType.DOWNLOAD

    @property
    def delete(self):
        return models.STSActionType.DELETE

    @property
    def list(self):
        return models.STSActionType.LIST

    @property
    def copy(self):
        return models.STSActionType.COPY


TYPES = _Type()


class STS(object):
    prefix = ""
    version = ""

    def __init__(self, region="*", bucket_owner="*",
                 bucket="*", object_name="*", extra_action_list=None):
        self._init(region, bucket_owner, bucket, object_name, extra_action_list)

    def _init(self, region="*", bucket_owner="*",
              bucket="*", object_name="*", extra_action_list=None):
        """

        :param prefix: acs:oss
        :param region: cn-beijing cn-shenzhen
        :param bucket_owner:
        :param bucket: bucket name
        :param object_name: oss object name
        :param extra_action_list: 类似如下格式：
                [
                    "oss:PutObject",
                    "oss:ListMultipartUploads",
                    "oss:AbortMultipartUpload",
                    "oss:ListParts",
                    "oss:GetObject"
                ]
        :type extra_action_list: list or None
        """
        self.region = region
        self.bucket_owner = bucket_owner
        self.bucket = bucket
        self.object_name = object_name

        if extra_action_list and not isinstance(extra_action_list, list):
            raise ValueError("must be a list of str")
        self.extra_action_list = extra_action_list

    def get_policy(self):
        raise NotImplementedError

    def signature(self, sts_access_id, sts_access_key, action_role_arn, region, role_session_name, endpoint="",
                  timeout=900,
                  **kwargs):
        """创建临时签名

        :type store_info: DataManager.roshan.storage.StoreMeta
        :param role_session_name: str, 形如  " action[0] + "_" + entity_id " 格式
        :param timeout: 证书超时时间
        :rtype: dict
        :return:
                {
                    'AccessKeyId': xxx
                    'AccessKeySecret': xxx
                    'SecurityToken': xxx
                }
        """

        return self._signature(
            sts_access_id,
            sts_access_key,
            region,
            action_role_arn,
            role_session_name,
            timeout=timeout,
            endpoint=endpoint
        )

    def _signature(self, access_key_id, access_key_secret, region, role_arn, role_session_name, endpoint, timeout=900,
                   **kwargs):
        raise NotImplementedError

    def _get_allowed_sts_actions(self):
        """ 返回形如：
                [
                    "oss:PutObject",
                    "oss:ListMultipartUploads",
                    "oss:AbortMultipartUpload",
                    "oss:ListParts",
                    "oss:GetObject"
                ]
        :rtype: list
        """
        raise NotImplementedError

    def _get_policy_template(self):
        return {
            "Version": self.version,
            "Statement": [
            ]
        }

    def _get_statement_list_objects(self):
        raise NotImplementedError

    def _get_statement_normal_action(self):
        return {
            "Effect": "Allow",
            "Action": self._get_allowed_sts_actions(),
            "Resource": [
                self._get_resource_str()
            ]
        }

    def _get_resource_str(self):
        return ":".join([
            self.prefix, self.region, self.bucket_owner, self.bucket + "/" + self.object_name
        ])

    def _get_resource_list_str(self):
        return ":".join([
            self.prefix, self.region, self.bucket_owner, self.bucket
        ])
