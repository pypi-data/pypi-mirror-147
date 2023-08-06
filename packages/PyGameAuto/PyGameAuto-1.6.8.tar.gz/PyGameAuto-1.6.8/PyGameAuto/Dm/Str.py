# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Str.py
# Time       ：2022/2/27 17:48
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：封装大漠字库API
"""

from .Mouse import Mouse


class Str:
    def __init__(self, dm_obj):
        self.__dm_obj = dm_obj

    def find_strF(self, int_x1, int_y1, int_x2, int_y2, str_name, color_format, sim=0.9):
        """
        找字
        """
        dm_ret = self.__dm_obj.FindStrFast(int_x1, int_y1, int_x2, int_y2, str_name, color_format, sim)
        return dm_ret

    def find_strF_click(self, int_x1, int_y1, int_x2, int_y2, str_name, color_format, sim=0.9):
        """
        找字并点击
        :param int_x1:
        :param int_y1:
        :param int_x2:
        :param int_y2:
        :param str_name:
        :param color_format:
        :param sim:
        :return: 成功 1, 失败 0
        """
        dm_ret = self.__dm_obj.FindStrFast(int_x1, int_y1, int_x2, int_y2, str_name, color_format, sim)
        if dm_ret[2] == -1:
            return
        else:
            int_x = dm_ret[1]
            int_y = dm_ret[2]
            Mouse(self.__dm_obj).move_lClick(int_x, int_y)
            return 1
