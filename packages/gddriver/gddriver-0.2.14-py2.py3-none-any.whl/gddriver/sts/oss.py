# -*- coding: utf-8 -*-
import sys
import json

from gddriver.sts.base import STS
from gddriver import errors
from aliyunsdkcore import client
from aliyunsdkcore.acs_exception import exceptions as acs_exs
from aliyunsdksts.request.v20150401 import AssumeRoleRequest


class OSSSTS(STS):
    prefix = "acs:oss"
    version = "1"

    def get_policy(self):
        raise NotImplementedError

    def _signature(self, access_key_id, access_key_secret, region, role_arn, role_session_name, endpoint, timeout=900,
                   **kwargs):
        policy = self.get_policy()

        clt = client.AcsClient(access_key_id, access_key_secret, region)
        req = AssumeRoleRequest.AssumeRoleRequest()
        req.set_RoleArn(role_arn)
        req.set_Policy(policy)
        req.set_RoleSessionName(role_session_name)  # The length of RoleSessionName have to be between 2-32
        req.set_DurationSeconds(timeout)
        try:
            response = clt.do_action_with_exception(req)
        except (acs_exs.ServerException, acs_exs.ClientException) as e:
            raise errors.SignatureError(e.message)

        body = json.loads(response)

        credential_dict = body.get('Credentials')
        if not credential_dict:
            raise RuntimeError("get temporary token fail")

        return credential_dict

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
        return {
            "Effect": "Allow",
            "Action": [
                "oss:ListObjects"
            ],
            "Resource": [
                self._get_resource_list_str()
            ],
            "Condition": {
                "StringLike": {
                    "oss:Prefix": self.object_name
                }
            }
        }

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

    def _get_statement_list_objects(self):
        return {
            "Effect": "Allow",
            "Action": [
                "oss:ListObjects"
            ],
            "Resource": [
                self._get_resource_list_str()
            ],
            "Condition": {
                "StringLike": {
                    "oss:Prefix": self.object_name
                }
            }
        }


class OSSUpload(OSSSTS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'] = [
            self._get_statement_normal_action(), self._get_statement_list_objects()
        ]
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "oss:PutObject",
            "oss:ListMultipartUploads",
            "oss:AbortMultipartUpload",
            "oss:ListParts",
            "oss:GetObject"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions


class OSSDownload(OSSSTS):
    """ 下载提供list的权限 """

    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'] = [self._get_statement_normal_action(), self._get_statement_list_objects()]
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "oss:GetObject"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions


class OSSDelete(OSSSTS):
    """ 删除的权限 """

    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'].append(self._get_statement_normal_action())
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "oss:DeleteObject"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions


class OSSList(OSSSTS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'].append(self._get_statement_list_objects())
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        return []


class OSSCopy(OSSSTS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'].append(self._get_statement_normal_action())
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "oss:GetObject",
            "oss:PutObject"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions
