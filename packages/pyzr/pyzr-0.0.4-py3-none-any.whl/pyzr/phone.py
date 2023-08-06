# -*- coding: utf-8 -*-

"""
@author: guzhi
@file: phone.py
@time: 2022/04/24
@projectExplain: 电话告警
"""

import json

import requests


class Phone(object):

    def __init__(self, uid, url, token, model_code):
        '''
        :param uid: 业务名称
        :param url: 告警url
        :param delay: 报警降频是否开启 默认关闭
        :param interval: 报警间隔 默认10s
        '''
        assert uid
        assert url
        assert token
        assert model_code
        self.uid = uid
        self.url = url
        self.token = token
        self.model_code = model_code

    def _alert(self, param):
        headers = {
            'uid': self.uid,
            'Request-Origion': 'SwaggerBootstrapUi',
            'accept': '*/*',
            'Content-Type': 'application/json; charset=utf-8',
        }
        data = json.dumps(param)

        r = requests.post(
            self.url,
            headers=headers,
            data=data
        )

    def alter_phone(self, mobiles, data):
        """
        打电话
        :param mobiles:  手机号 或者手机号列表 支持list或,拼接
        :param data: 告警内容
        :return:
        """

        assert isinstance(mobiles, (str, list))
        if isinstance(mobiles, str):
            mobiles = mobiles.split(',')

        for mobile in mobiles:
            param = {
                'token': self.token,
                'to': mobile,
                'modelCode': self.model_code,
                'params': data,
            }
            self._alert(param)
