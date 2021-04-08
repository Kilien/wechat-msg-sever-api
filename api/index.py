# -*- coding: utf8 -*-
import os
from utils.webRequest import WebRequest as wq
from http.server import BaseHTTPRequestHandler
import urllib.parse as urlparse
import json


# 获取token
def get_token(id, secert):
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    params = {
        'corpid': id,
        'corpsecret': secert
    }
    r = wq().get(url, params=params).json
    return r['access_token']


# 发送请求
def send_msg(id, secert, agent_id, msg):
    token = get_token(id, secert)
    sendUrl = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=" + token

    data = {
        "safe": 0,
        "touser": "@all",
        "msgtype": "text",
        "agentid": agent_id,
        "text": {
            "content": msg
        }
    }
    return wq().post(sendUrl, data=data)


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 请求的url链接处理
        path = self.path
        parsed = urlparse.urlparse(path)
        querys = urlparse.parse_qs(parsed.query)
        querys = {k: v[0] for k, v in querys.items()}

        # 执行方法
        try:
            # 读取参数
            apiid=querys['id']
            apisecert=querys['secert']
            # agentId = os.environ.get('agentId')
            apiagentId = querys['agentId']
            apimsg = querys['msg']
        except:
            apimsg = '有必填参数没有填写，请检查是否填写正确和格式是否错误。'
            # apimsg = f'apiagentId:{apiagentId}'
            status = 1
        else:
            try:
                # 执行主程序
                send_msg(id=apiid, secert=apisecert, msg=apimsg, agent_id=apiagentId)
            except:
                status = 1
                apimsg = '主程序运行时出现错误，请检查参数是否填写正确。'
            else:
                status = 0

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status":status,
            "msg":apimsg
        }).encode('utf-8'))
        return