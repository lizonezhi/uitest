# -*- coding:utf-8 -*-
# author：lizonezhi
from uitest import archive_json


class SignDataModel(archive_json):

    def __init__(self):
        self.sign = ''  # 签名
        self.data = ''  # 内容 具体类的rsa加密后的json字符串


class ResponseModel(archive_json):

    def __init__(self):
        self.code = 200
        self.msg = 'SUCCESS'
        self.data = None