# -*- coding: utf-8 -*-
import json
import os

from fake_useragent import UserAgent, FakeUserAgentError


class UserAgentUtil(object):
    file_path = os.getcwd() + '/useragent.txt'
    file_json = {}

    def getUA(self):
        file_exists = os.path.isfile(self.file_path)
        if file_exists:
            with open(self.file_path, 'r') as f:
                self.file_json = json.loads(f.read())
        else:
            try:
                ua = UserAgent()
                ua_list = []
                for i in ua.data_browsers.values():
                    ua_list.extend(i)
                self.file_json['useragent'] = ua_list
                with open(self.file_path, 'w') as f:
                    f.write(json.dumps(self.file_json, indent=4))
            except FakeUserAgentError:
                print("获取UA失败，请重试。。。")
        return self.file_json
