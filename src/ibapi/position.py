#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年09月29日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""


from ib.ext.Contract import Contract


class Position(object):
    def __init__(self):
        self.contract = None
        self.size = 0
        self.mkt_price = 0.0
        self.mkt_value = 0.0
        self.avg_cost = 0.0
        self.cost = 0.0
        self.realized_pnl = 0.0
        self.unrealized_pnl = 0.0
        self.unrealized_ratio = 0.0

    def __str__(self):
        d = {'C': '看涨期权(call)', 'P': '看跌期权(put)'}
        if self.contract.m_secType == 'STK':
            return ('证券代码:{0}, 证券类型: 股票, 头寸:{1}, 市场价格:{2}, 市场价值:{3}, '
                    '持仓均价:{4}, 持仓成本:{5}, 已实现盈亏:{6}, 未实现盈亏:{7}, 未实现盈亏比率:{8}%').format(
                self.contract.m_symbol, self.size, self.mkt_price, self.mkt_value,
                self.avg_cost, self.cost, self.realized_pnl, self.unrealized_pnl, round(self.unrealized_ratio * 100,2))
        elif self.contract.m_secType == 'OPT':
            return ('证券代码:{0}, 证券类型:{1}, 行权日:{2}, 执行价:{3}, 头寸:{4}, 市场价格:{5}, '
                    '市场价值:{6}, 持仓均价:{7}, 持仓成本:{8}, 已实现盈亏:{9}, 未实现盈亏:{10}, 未实现盈亏比率:{11}%').format(
                self.contract.m_symbol, d[self.contract.m_right], self.contract.m_expiry, self.contract.m_strike,
                self.size, self.mkt_price, self.mkt_value, self.avg_cost, self.realized_pnl, self.unrealized_pnl,
                round(self.unrealized_ratio * 100, 2))