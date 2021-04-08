#!/usr/bin/env python
# encoding: utf-8
"""
    File Name：     WebRequest
    Description :   Network Requests Class
"""
from requests.models import Response
from faker import Faker
from lxml import etree
import requests
import time
import logging

FORMAT = "[%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s"
logging.basicConfig(format=FORMAT, level=logging.INFO)
log = logging.getLogger()

requests.packages.urllib3.disable_warnings()  # NOTE: Remove SSL authentication warnings


class WebRequest:
    name = "web_request"

    def __init__(self):
        self.param = {}
        self.log = log
        self.retry_time = 3
        self.timeout = 5
        self.retry_interval = 5
        self.response = Response()

    @property
    def header(self):
        """
            basic header
        """
        ip = Faker().ipv4()
        return {'User-Agent': Faker().user_agent(),
                'Accept': '*/*',
                'Connection': 'keep-alive',
                'Accept-Language': 'zh-CN,zh;q=0.8',
                'X-Client-IP': ip,
                'X-Remote-Addr': ip,
                'X-Forwarded-For': ip}

    def get_header(self, url):
        while True:
            try:
                header = requests.head(url=url, headers=self.header, timeout=5, verify=False)
                if header.status_code == 200:
                    return header
            except Exception as e:
                self.log.error("requests: %s error: %s" % (url, str(e)))
                self.retry_time -= 1
                if self.retry_time <= 0:
                    resp = Response()
                    resp.status_code = 200
                    return self
                self.log.info("retry %s second after" % self.retry_interval)
                time.sleep(self.retry_interval)

    def get(self, url, **kwargs):
        """
            get method
            :param url: target url
        """
        if kwargs.get('headers') and isinstance(kwargs['headers'], dict):
            kwargs['headers'].update(self.header)
        else:
            kwargs['headers'] = self.header

        if not kwargs.get('timeout'):
            kwargs['timeout'] = self.timeout

        while True:
            try:
                self.response = requests.get(url=url, **kwargs)
                return self
            except Exception as e:
                self.log.error("requests: %s error: %s" % (url, str(e)))
                self.retry_time -= 1
                if self.retry_time <= 0:
                    resp = Response()
                    resp.status_code = 200
                    return self
                self.log.info("retry %s second after" % self.retry_interval)
                time.sleep(self.retry_interval)

    def post(self, url, data, **kwargs):
        """
            post method
            :param url: target url
            :param data: json data
        """
        if kwargs.get('headers') and isinstance(kwargs['headers'], dict):
            kwargs['headers'].update(self.header)
        else:
            kwargs['headers'] = self.header

        if not kwargs.get('timeout'):
            kwargs['timeout'] = self.timeout

        while True:
            try:
                self.response = requests.post(url=url, json=data, **kwargs)
                return self
            except Exception as e:
                self.log.error("requests: %s error: %s" % (url, str(e)))
                self.retry_time -= 1
                if self.retry_time <= 0:
                    resp = Response()
                    resp.status_code = 200
                    return self
                self.log.info("retry %s second after" % self.retry_interval)
                time.sleep(self.retry_interval)

    @property
    def json(self):
        return self.response.json()

    @property
    def content(self):
        return self.response.content

    @property
    def tree(self):
        return etree.HTML(self.response.content)

    @property
    def text(self):
        return self.response.text

    @property
    def status_code(self):
        return self.response.status_code
