# -*-coding:utf-8-*-

"""
提取pdf信息的公用方法
"""

from decimal import Decimal
from math import ceil


def _base_rect(arr, height):
    rect = [int(Decimal(min(arr, key=lambda x: Decimal(x['x0']))['x0'])),
            int(Decimal(max(arr, key=lambda x: Decimal(x['bottom']))['bottom'])),
            ceil(Decimal(max(arr, key=lambda x: Decimal(x['x1']))['x1'])),
            int(ceil(Decimal(min(arr, key=lambda x: Decimal(x['top']))['top'])))]
    return rect


# 计算矩形的面积
def rect_area(rect):
    if not rect:
        return 0
    return (rect[2] - rect[0]) * (rect[3] - rect[1])


def bbox_to_str(bbox):
    return [str(v) for v in bbox]
