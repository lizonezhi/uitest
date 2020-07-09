#!/usr/bin/env python
# coding=utf-8

import json
# 支持自动序列化的基类
class archive_json(object):
    def from_json(self, json_str):
        obj = json.loads(json_str)
        for key in vars(self):
            if key in obj:
                setattr(self, key, obj[key])

    def to_json(self):
        return json.dumps(vars(self))

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError:
            return False
        return True