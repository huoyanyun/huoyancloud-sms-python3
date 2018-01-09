# coding=utf-8

import json
from collections import OrderedDict
from urllib.parse import quote
import hashlib
import time
import uuid
import requests

TIME_ZONE = "GMT"
FORMAT_ISO_8601 = "%Y-%m-%dT%H:%M:%SZ"
FORMAT_RFC_2616 = "%a, %d %b %Y %X GMT"


class HyApiException(Exception):
    def __init__(self, message, status):
        super().__init__(message, status)
        self.message = message
        self.status = status


class SmsClient(object):

    def __init__(self, access_key_id, access_key_secret, model="sms"):
        self.domain = 'b.dev.huoyancloud.com/api/{}/'.format(model)
        self.ACCESS_KEY_ID = access_key_id
        self.ACCESS_KEY_SECRET = access_key_secret

    def gen_url(self, params, security=False, access_key_id=None, access_key_secret=None, domain=None):
        if not access_key_id or access_key_id == '':
            access_key_id = self.ACCESS_KEY_ID
        if not access_key_secret or access_key_secret == '':
            access_key_secret = self.ACCESS_KEY_SECRET
        if not domain or domain == "":
            domain = self.domain
        if (not access_key_id or access_key_id == '') or (not access_key_secret or access_key_secret == '') or (
                not domain or domain == ""):
            raise HyApiException("参数未配置", 1)
        parameters = dict()
        parameters["Timestamp"] = self.get_iso_8061_date()
        parameters["SignatureMethod"] = "HMAC-SHA1"
        parameters["SignatureVersion"] = "1.0"
        parameters["SignatureNonce"] = self.get_uuid()
        parameters["AccessKeyId"] = access_key_id
        parameters.update(params)
        parameters = OrderedDict(sorted(parameters.items()))
        sorted_query_string_temp = list()
        for k, v in parameters.items():
            sorted_query_string_temp.append(
                "{}={}&".format(quote(k), quote(v)))
        sorted_query_string_temp = "".join(sorted_query_string_temp)
        # sorted_query_string_temp = quote(sorted_query_string_temp)
        string_to_sign = sorted_query_string_temp + access_key_secret
        sign = self.sha1(string_to_sign)
        schema = "http"
        if security:
            schema = "https"
        url = "{}://{}?{}Signature={}".format(schema,
                                              domain, sorted_query_string_temp, sign)
        return url

    def send_sms(self, phone_number, sign_name, template_code, template_param='', out_id=''):
        params = {'PhoneNumbers': phone_number, 'SignName': sign_name, 'TemplateCode': template_code,
                  'TemplateParam': template_param, 'OutId': out_id, 'Action': 'SendSms'}
        return self.request(params)

    def query_send_details(self, phone_number, biz_id, send_date, page_size=10, current_page=1):
        params = {'PhoneNumbers': phone_number, 'BizId': biz_id, 'SendDate': send_date,
                  'PageSize': page_size, 'CurrentPage': current_page, 'Action': 'QuerySendDetails'}
        return self.request(params)

    def request(self, params, security=False, access_key_id=None, access_key_secret=None, domain=None):
        url = self.gen_url(params, security, access_key_id,
                           access_key_secret, domain)
        response = requests.get(url)
        response.encoding = "utf-8"
        body = response.text
        if not body or body == "":
            return json.dumps({"code": "1", "msg": "服务器异常"}, ensure_ascii=False)
        try:
            json_obj = json.loads(body)
        except Exception as ex:
            print(ex)
            return json.dumps({"code": "1", "msg": "服务器异常"}, ensure_ascii=False)
        if not json_obj:
            return json.dumps({"code": "1", "msg": "服务器异常"}, ensure_ascii=False)
        return json_obj

    def get_uuid(self):
        return str(uuid.uuid4())

    def get_iso_8061_date(self):
        return time.strftime(FORMAT_ISO_8601, time.gmtime())

    def sha1(self, content):
        return hashlib.sha1(content.encode("utf-8")).hexdigest()
