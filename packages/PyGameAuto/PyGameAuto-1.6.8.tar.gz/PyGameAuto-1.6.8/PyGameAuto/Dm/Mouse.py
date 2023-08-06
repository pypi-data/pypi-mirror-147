# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Mouse.py
# Time       ：2022/2/15 0:22
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：封装大漠鼠标API
"""
from .System import System


class Mouse:
    def __init__(self, dm_obj, start_time=0.5, end_time=1):
        self.__dm_obj = dm_obj
        self.start_time = start_time
        self.end_time = end_time

    def lClick(self):
        """
        左键点击
        """
        System.delay(self.start_time, self.end_time)
        self.__dm_obj.LeftClick()

    def rClick(self):
        """
        右键点击
        """
        System.delay(self.start_time, self.end_time)
        self.__dm_obj.RightClick()

    def move_lClick(self, int_x, int_y):
        """
        移动并点击
        """
        self.__dm_obj.MoveTo(int_x, int_y)
        System.delay(self.start_time, self.end_time)
        self.lClick()

    def move_double_click(self, int_x, int_y):
        """
        移动并双击
        """
        self.__dm_obj.MoveTo(int_x, int_y)
        System.delay(self.start_time, self.end_time)
        self.__dm_obj.LeftDoubleClick()
