# -*- coding: utf-8 -*-
import json

from gddriver.sts.base import STS
import hmac
from hashlib import sha256
import time
import requests


def generate_sign(params, headers, secret_key):
    sign = "sign"
    and_ = "&"
    equal = "="
    req_time = "requestTime"

    if not secret_key:
        return None

    inner_param_map = {}
    if params:
        for key, value in params.items():
            if value:
                inner_param_map[key] = value
    inner_header_map = {}
    inner_header_map.update(headers)

    for key, value in inner_header_map.items():
        if key != sign:
            inner_param_map[key] = value
        else:
            inner_param_map[req_time] = inner_header_map.get(req_time)
    l = []
    for key, value in inner_param_map.items():
        l.append((key, json.dumps(value, separators=(',', ':'))))
    l.sort(key=lambda x: x[0])
    s = ""
    for item in l:
        s = and_.join([s, equal.join([item[0], item[1]])])
    s = s[1:]
    signature = hmac.new(bytes(secret_key).encode("utf-8"), bytes(s).encode("utf-8"), digestmod=sha256).digest().encode(
        "hex")
    return signature


class WCSSTS(STS):
    prefix = "wcs:oss"
    version = "1"

    def __init__(self, region="*", bucket_owner="",
                 bucket="*", object_name="*", extra_action_list=None):
        self._init(region, bucket_owner, bucket, object_name, extra_action_list)

    def _get_statement_list_objects(self):
        return {
            "Effect": "Allow",
            "Action": [
                "oss:bucket:list"
            ],
            "Resource": [
                self._get_resource_list_str()
            ]
        }

    def _signature(self, access_key_id, access_key_secret, region, role_arn, role_session_name, endpoint, timeout=900,
                   **kwargs):
        policy = self.get_policy()
        alg_type = "HmacSHA256"
        req_time = str(int(round(time.time() * 1000)))

        headers = {"algorithm": alg_type,
                   "requestTime": req_time,
                   "accessKey": access_key_id,
                   "signedHeader": "1"}
        params = {
            "properties": {
                "durationSeconds": 86400,
                "policyContent": json.loads(policy)
            }
        }

        headers["sign"] = generate_sign(params, headers, access_key_secret)
        credential_dict = requests.post(endpoint, json=params,
                                        headers=headers).json().get("result", {})

        if not credential_dict:
            raise RuntimeError("get temporary token fail")

        credential_dict["AccessKeyId"] = credential_dict.pop("accessKeyId")
        credential_dict["AccessKeySecret"] = credential_dict.pop("accessKeySecret")
        credential_dict["SecurityToken"] = credential_dict.pop("securityToken")
        credential_dict["Expiration"] = credential_dict["expiresAt"]

        return credential_dict


class WCSDownload(WCSSTS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'] = [self._get_statement_normal_action(), self._get_statement_list_objects()]
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "oss:object:download",
            "oss:object:get"
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions


class WCSUpload(WCSSTS):
    def get_policy(self):
        policy = self._get_policy_template()
        policy['Statement'] = [
            self._get_statement_normal_action(), self._get_statement_list_objects()
        ]
        return json.dumps(policy)

    def _get_allowed_sts_actions(self):
        actions = [
            "oss:object:upload",
            "oss:multipart:abort",
            "oss:multipart:listParts",
            "oss:object:download",
            "oss:multipart:initialize",
            "oss:multipart:complete",
            "oss:object:get",
            "oss:multipart:upload",
        ]
        if self.extra_action_list:
            actions += self.extra_action_list

        return actions
