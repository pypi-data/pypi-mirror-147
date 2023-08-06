# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Color.py
# Time       ：2022/2/15 0:27
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：封装大漠颜色API
"""
from .Mouse import Mouse


class Color:
    def __init__(self, dm_obj):
        self.__dm_obj = dm_obj

    def find_color(self, int_x1, int_y1, int_x2, int_y2, color, sim=0.9, direct=0):
        """
        找色
        :param int_x1:
        :param int_y1:
        :param int_x2:
        :param int_y2:
        :param color: 色彩格式
        :param sim:
        :param direct:
        :return:
        """
        dm_ret = self.__dm_obj.FindColor(int_x1, int_y1, int_x2, int_y2, color, sim, direct)
        return dm_ret

    def find_color_click(self, int_x1, int_y1, int_x2, int_y2, color, sim=0.9, direct=0):
        """
        找色 并 点击
        :param int_x1:
        :param int_y1:
        :param int_x2:
        :param int_y2:
        :param color: 色彩格式
        :param sim:
        :param direct:
        :return: 成功 1, 失败 0
        """
        dm_ret = self.__dm_obj.FindColor(int_x1, int_y1, int_x2, int_y2, color, sim, direct)
        if dm_ret[2] == -1:
            return
        else:
            int_x = dm_ret[1]
            int_y = dm_ret[2]
            Mouse(self.__dm_obj).move_lClick(int_x, int_y)
            return 1
