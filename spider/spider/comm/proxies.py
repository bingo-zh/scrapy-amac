#!/usr/bin/env python
# encoding: utf-8
"""
@version: 0.1
@author: zhangwb
"""
import json
import os
import random


class Proxies(object):
    def __init__(self):
        self.file_path = os.path.abspath(os.path.dirname(__file__))
        self.filename = 'proxies.txt'
        self.proxies_list = []
        with open(self.file_path + '/' + self.filename) as f:
            lines = f.readlines()
            for line in lines:
                li = json.loads(line)
                type = li.get('type')
                host = str(li.get('host'))
                port = str(li.get('port'))
                ip = type + '://' + host + ':' + port
                self.proxies_list.append(ip)

    #随机获取代理
    def getProxy(self):
        length = len(self.proxies_list)
        i = random.randint(0, length)
        return self.proxies_list[i]