# -*- coding: utf-8 -*-

"""
@author: guzhi
@file: alert.py
@time: 2022/04/24
@projectExplain: 报警/通知模块
"""

import json
import time
import socket
import datetime

import requests


class Alert(object):

    def __init__(self, name, url, delay=False, interval=10):
        '''
        :param name: 业务名称
        :param url: 告警url
        :param delay: 报警降频是否开启 默认关闭
        :param interval: 报警间隔 默认10s
        '''
        assert name
        assert url
        try:
            self.name = f"服务器: {socket.gethostname()} \n IP: {socket.gethostbyname(socket.gethostname())} \n 业务名称: {name}"
        except:
            self.name = name
        self.url = url
        self.delay = delay
        self.interval = interval
        self._alert_time = 0

    def _alert(self, message, msgtype):
        content = f"{datetime.datetime.now()}: \n {self.name} \n\n {message}"
        if msgtype:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": content,
                }
            }
        else:
            data = {
                "msgtype": "text",
                "text": {
                    "content": content,
                },
            }
        data = json.dumps(data)
        r = requests.post(
            self.url,
            headers={'Content-Type': 'application/json; charset=utf-8'},
            data=data
        )

    def _alert_now(self, message, msgtype):
        self._alert(message, msgtype)

    def _alert_delay(self, message, msgtype):
        if time.time() - self._alert_time > self.interval:
            self._alert(message, msgtype)
            self._alert_time = time.time()

    def _distribute_alert(self, keyword, message, msgtype):
        if self.delay:
            self._alert_delay(f"{keyword} - {message}", msgtype)
        else:
            self._alert_now(f"{keyword} - {message}", msgtype)

    def error(self, message: str, keyword='error', msgtype=None):
        '''
        发送重要错误信息 keyword - error
        :param message:
        :param keyword:
        :param msgtype:
        :return:
        '''
        self._distribute_alert(keyword, message, msgtype)

    def warning(self, message: str, keyword='warning', msgtype=None):
        '''
        发送告警信息 keyword - warning
        :param message:
        :param keyword:
        :param msgtype:
        :return:
        '''
        self._distribute_alert(keyword, message, msgtype)

    def info(self, message: str, keyword='info', msgtype=None):
        '''
        发送通知信息 keyword - info
        :param message:
        :param keyword:
        :param msgtype:
        :return:
        '''
        self._distribute_alert(keyword, message, msgtype)

    def statistics(self, message: str, keyword='statistics', msgtype=None):
        '''
        发送统计通知信息 keyword - 统计
        :param message:
        :param keyword:
        :param msgtype:
        :return:
        '''
        self._distribute_alert(keyword, message, msgtype)
