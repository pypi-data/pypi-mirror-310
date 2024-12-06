# -*- coding: utf-8 -*-
'''
@Project : zwdx_minjiang
@File : __init__.py
@description : Packaging requires files
@Author : anonymous
@Date : 2024.11.01
'''
from .driver.zwdx_minjiang_test import MinJiangTest
from .driver import zwdx_minjiang_tools as MinJiangTools


__all__ = [
    MinJiangTest,
    MinJiangTools,
]