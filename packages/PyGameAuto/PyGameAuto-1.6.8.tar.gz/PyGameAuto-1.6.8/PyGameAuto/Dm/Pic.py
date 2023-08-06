# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : Pic.py
# Time       ：2022/2/20 16:40
# Author     ：Lex
# email      : 2983997560@qq.com
# Description：封装大漠图片API
"""
from .Mouse import Mouse


class Pic:
    def __init__(self, dm_obj):
        self.__dm_obj = dm_obj

    def find_pic(self, int_x1, int_y1, int_x2, int_y2, pic_name, delta_color="050505", sim=0.9, direct=0):
        """
        找图
        :param int_x1:
        :param int_y1:
        :param int_x2:
        :param int_y2:
        :param pic_name:
        :param delta_color:
        :param sim:
        :param direct:
        :return: 成功 返回坐标, 失败 -1, -1, -1
        """
        dm_ret = self.__dm_obj.FindPic(int_x1, int_y1, int_x2, int_y2, pic_name, delta_color, sim, direct)
        return dm_ret

    def find_pic_click(self, int_x1, int_y1, int_x2, int_y2, pic_name, delta_color="050505", sim=0.9, direct=0):
        """
        找图并点击
        :return: 成功 1, 失败 0
        """
        dm_ret = self.__dm_obj.FindPic(int_x1, int_y1, int_x2, int_y2, pic_name, delta_color, sim, direct)
        if dm_ret[2] == -1:
            return
        else:
            int_x = dm_ret[1]
            int_y = dm_ret[2]
            Mouse(self.__dm_obj).move_lClick(int_x, int_y)
            return 1
