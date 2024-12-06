#!/usr/bin/python3
# @Time    : 2024-11-10
# @Author  : Kevin Kong (kfx2007@163.com)
import requests

URL = "https://secure.nmi.com/api/transact.php"


class Comm(object):
    def __get__(self, instance, owner):
        self.security_key = instance.security_key
        return self

    def get_headers(self):
        return {
            "accept": "application/x-www-form-urlencoded",
            "content-type": "application/x-www-form-urlencoded",
        }

    def post(self, type, data):
        data.update({"type":type,"security_key": self.security_key})
        print('+++sdk+++')
        print(data)
        resp = requests.post(URL, data=data, headers=self.get_headers())
        resp.raise_for_status()
        items = resp.text.split('&')
        for item in items:
            key, value = item.split('=')
            data.update({key: value})
        return data
