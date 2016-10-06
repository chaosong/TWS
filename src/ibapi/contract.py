#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月03日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

from ib.ext.Contract import Contract as IBContract


class Contract(IBContract):
    def __init__(self):
        super(Contract, self).__init__()

    @property
    def symbol(self):
        return self._symbol
    @symbol.setter
    def symbol(self, value):
        self._symbol = value
        self.m_symbol = value

    @property
    def sec_type(self):
        return self._sec_type

    @sec_type.setter
    def sec_type(self, value):
        self._sec_type = value
        self.m_secType = value

    @property
    def exchange(self):
        return self._exchange
    @exchange.setter
    def exchange(self, value):
        self._exchange = value
        self.m_exchange = value

    @property
    def primary_exch(self):
        return self._symbol
    @primary_exch.setter
    def primary_exch(self, value):
        self._primary_exch = value
        self.m_primaryExch = value

    @property
    def currency(self):
        return self._currency
    @currency.setter
    def currency(self, value):
        self._currency = value
        self.m_currency = value

    @property
    def expiry(self):
        return self._expiry
    @expiry.setter
    def expiry(self, value):
        self._expiry = value
        self.m_expiry = value

    @property
    def strike(self):
        return self._strike
    @strike.setter
    def strike(self, value):
        self._strike = value
        self.m_strike = value

    @property
    def right(self):
        return self._right
    @right.setter
    def right(self, value):
        self._right = value
        self.m_right = value

    def __str__(self):
        if self.sec_type == 'STK':
            return '证券代码:{0}, 证券类型:股票, 货币:{1}'.format(self.symbol, self.currency)
        elif self.sec_type == 'OPT':
            d1 = {'C': '看涨', 'P': '看跌'}
            d2 = {'C': '(call)', 'P': '(put)'}
            return '证券代码:{0}, 证券类型:{1}期权{2}, 货币:{3}, 行权日期:{4}, 行权价:{5}'.format(self.symbol,
                d1[self.right], d2[self.right], self.currency, self.expiry, self.strike)