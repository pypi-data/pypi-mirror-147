# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : NetLogin.py
# Time       ：2022/2/12 17:18
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：
"""
import time
import json
import requests


class RK_NetLogin:
    """ 瑞科网络验证 """

    def __init__(self, cardnum):
        self.cardnum = cardnum
        self.url = "http://api.ruikeyz.com/netver/webapi"
        self.heartbeatkey = ""
        self.token = ""
        self.endtime = ""
        self.maccode = "b38ee725812106809d1dabdcd3d76f71"  # Mac 地址需获取
        self.versionname = "v1.0"
        self.status = None

        self.param = {
            "businessid": None,
            "encrypttypeid": 0,
            "platformusercode": "1e97cda60a2616e1",  # 平台用户Code
            "goodscode": "e1ecb346e42da943",  # 软件编码
            "inisoftkey": "",
            "timestamp": None,
            "data": None,
            "sign": "",
            "platformtypeid": 1,
        }

    def loginInit(self):
        """ 卡密初始化 """
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "maccode": self.maccode,
            "versionname": self.versionname,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }

        data_json = json.dumps(send_data)
        param = self.param
        param["businessid"] = 1
        param["timestamp"] = int(round(time.time() * 1000))
        param["data"] = data_json

        re_data = requests.post(self.url, json=param, verify=False).json()
        if re_data["code"] == 0:
            # 成功
            # 请求标识 验证
            json_data = eval(re_data["data"])
            if json_data["requestflag"] == str(timestamp):
                # 初始化成功
                self.param["inisoftkey"] = json_data["inisoftkey"]
                return 1, "初始化成功"
        else:
            return 0, "初始化失败, %s" % re_data["msg"]
        return

    def loginCheck(self):
        """ 卡密登陆 """
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnum": self.cardnum,
            "maccode": self.maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }

        data_json = json.dumps(send_data)
        param = self.param
        param["businessid"] = 4
        param["timestamp"] = int(round(time.time() * 1000))
        param["data"] = data_json

        re_data = requests.post(self.url, json=param, verify=False).json()
        if re_data["code"] == 0:
            # 成功
            # 请求标识 验证
            json_data = eval(re_data["data"])

            if json_data["requestflag"] == str(timestamp):
                # 初始化成功
                self.heartbeatkey = json_data["heartbeatkey"]
                self.token = json_data["token"]
                self.endtime = json_data["endtime"]
                self.status = 1
                return 1, json_data["endtime"]
        else:
            return 0, "登陆失败, %s" % re_data["msg"]

    def loginHeart(self):
        """ 心跳 """
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": self.cardnum,
            "maccode": self.maccode,
            "token": self.token,
            "heartbeatkey": self.heartbeatkey,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }

        data_json = json.dumps(send_data)
        param = self.param
        param["businessid"] = 5
        param["timestamp"] = int(round(time.time() * 1000))
        param["data"] = data_json

        re_data = requests.post(self.url, json=param, verify=False).json()
        if re_data["code"] == 0:
            # 成功
            # 请求标识 验证
            json_data = eval(re_data["data"])

            if json_data["requestflag"] == str(timestamp):
                # 初始化成功
                self.heartbeatkey = json_data["heartbeatkey"]
                self.endtime = json_data["endtime"]
                self.status = 1
                return 1, "心跳验证成功"
        else:
            return 0, "心跳验证失败, %s" % re_data["msg"]

    def loginExit(self):
        """ 退出登陆"""
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": self.cardnum,
            "maccode": self.maccode,
            "token": self.token,
            "timestamp": timestamp
        }

        data_json = json.dumps(send_data)
        param = self.param
        param["businessid"] = 7
        param["timestamp"] = int(round(time.time() * 1000))
        param["data"] = data_json

        re_data = requests.post(self.url, json=param, verify=False).json()
        if re_data["code"] == 0:
            # 成功
            # 请求标识 验证
            self.status = 0
            return 1, "退出成功"
        else:
            return 0, "退出失败, %s" % re_data["msg"]

    def loginUnbind(self):
        """ 解绑 """
        timestamp = int(round(time.time() * 1000))
        send_data = {
            "cardnumorusername": self.cardnum,
            "maccode": self.maccode,
            "timestamp": timestamp,
            "requestflag": str(timestamp)
        }

        data_json = json.dumps(send_data)
        param = self.param
        param["businessid"] = 9
        param["timestamp"] = int(round(time.time() * 1000))
        param["data"] = data_json

        re_data = requests.post(self.url, json=param, verify=False).json()
        if re_data["code"] == 0:
            self.status = 0
            return 1, "解绑成功"
        else:
            return 0, "解绑失败"


if __name__ == '__main__':
    net_check = RK_NetLogin("0a202d59aa01a700")
    check_code, check_msg = net_check.loginInit()
    print(check_msg)
    # net_check.loginUnbind()

    if check_code:
        # 初始化成功
        check_code, check_msg = net_check.loginCheck()
        print(check_msg)
        # 登陆成功
        if check_code:
            # for i in range(3):
            #     check_code, check_msg = net_check.loginHeart()
            #     print(check_msg)
            #     time.sleep(300)
            # 心跳验证 需超过5min
            check_code, check_msg = net_check.loginHeart()
            print(check_msg)
        check_code, check_msg = net_check.loginExit()
        print(check_msg)
