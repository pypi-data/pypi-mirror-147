# -*- coding: utf-8 -*-
"""
@Time : 2022/4/19 9:28 
@Author : YarnBlue 
@description : 
@File : price_interface.py 
"""
from abc import ABC


class PriceInterface(ABC):
    def call(self, **kwargs):
        pass
