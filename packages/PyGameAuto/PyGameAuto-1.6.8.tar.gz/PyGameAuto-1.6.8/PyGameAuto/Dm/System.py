# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : System.py
# Time       ：2022/2/15 9:29
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：
"""
import time
import random


class System:
    @classmethod
    def delay(cls, rand_start_time=0.5, rand_end_time=1):
        """
        随机延迟, 默认 0.5 ~ 1 之间随机
        :return:
        """
        random.seed(time.time())
        rand_time = random.uniform(rand_start_time, rand_end_time)
        time.sleep(rand_time)
