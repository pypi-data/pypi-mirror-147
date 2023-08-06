# -*- coding: utf-8 -*-
import json

from gddriver.sts.base import STS
from gddriver import errors
import boto3


class S3STS(STS):
    prefix = "arn:aws:s3"
    # minio和s3一致
    version = "2012-10-17"

    def __init__(self, region="", bucket_owner="",
                 bucket="*", object_name="*", extra_action_list=None):
        self._init(region, bucket_owner, bucket, object_name, extra_action_list)

    def _get_statement_list_objects(self):
        return {
            "Effect": "Allow",
            "Action": [
                "s3:ListBucket"
            ],
            "Resource": [
                self._get_resource_list_str()
            ],
            "Condition": {
                "StringLike": {
                    "s3:prefix": self.object_name
                }
            }
        }

    def _signature(self, access_key_id, access_key_secret, region, role_arn, role_session_name, endpoint, timeout=900,
                   **kwargs):
        policy = self.get_policy()
        clt = boto3.client("sts",
                           aws_access_key_id=access_key_id,
                           aws_secret_access_key=access_key_secret,
                           endpoint_url=endpoint,
                           region_name=region)
        credential_dict = clt.assume_role(
            RoleArn=role_arn,
            RoleSessionName=role_session_name,
            Policy=policy,
            DurationSeconds=3600
        ).get('Credentials')

        if not credential_dict:
            raise RuntimeError("get temporary token fail")

        credential_dict["AccessKeySecret"] = credential_dict.pop("SecretAccessKey")
        credential_dict["SecurityToken"] = credential_dict.pop("SessionToken")
        credential_dict["Expiration"] = credential_dict["Expiration"].strftime("%Y-%m-%dT%H:%M:%S%Z")

        return credential_dict


class S3Download(S3STS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'] = [self._get_statement_normal_action(), self._get_statement_list_objects()]
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "s3:GetObject"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions


class S3Upload(S3STS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'] = [
            self._get_statement_normal_action(), self._get_statement_list_objects()
        ]
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "s3:PutObject",
            "s3:ListBucketMultipartUploads",
            "s3:AbortMultipartUpload",
            "s3:ListMultipartUploadParts",
            "s3:GetObject"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions
