#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月03日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""


class Tick(object):
    def __init__(self):
        self.symbol = ''
        self.timestamp = 0

        self.ask_price = 0.0
        self.bid_price = 0.0
        self.last_price = 0.0

        self.ask_size = 0
        self.bid_size = 0
        self.last_size = 0

        self.volume = 0

    def __str__(self):
        return '证券代码:{0}, 时间戳:{1}, 卖出价:{2}×{3}, 买入价:{4}×{5}, 最后价:{6}×{7}, 成交量:{8}'.format(
            self.symbol, self.timestamp, self.ask_price, self.ask_size, self.bid_price, self.bid_size,
            self.last_price,self.last_size, self.volume)


class OptionGreek(object):
    def __init__(self):
        self.symbol = ''
        self.timestamp = 0
        self.div = 0
        self.implied_vol = 0
        self.delta = 0
        self.gamma = 0
        self.vega = 0
        self.theta = 0
        self.opt_price = 0

    def __str__(self):
        return '证券代码:{0}, 时间戳:{1}, 股息:{2}, 隐含波动率:{3}, delta:{4}, gamma:{5}, vega:{6}, theta:{7}, 期权价格:{8}'.format(
            self.symbol, self.timestamp, self.div, self.implied_vol, self.delta, self.gamma, self.vega, self.theta,
            self.opt_price)