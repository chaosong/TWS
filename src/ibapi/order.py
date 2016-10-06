#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月03日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

from enum import Enum, unique
from ib.ext.Order import Order as IBOrder
from ib.ext.OrderState import OrderState as IBOrderState

@unique
class Status(Enum):
    # https://www.ibkr.com.cn/cn/software/api/apiguide/java/orderstatus.htm
    PendingSubmit = 1
    PendingCancel = 2
    PreSubmitted = 3
    Submitted = 4
    Cancelled = 5
    Filled = 6
    Inactive = 7


class Order(IBOrder):
    def __init__(self):
        super(Order, self).__init__()

    @property
    def outsiderth(self):
        return self._outsiderth
    @outsiderth.setter
    def outsiderth(self, value):
        self._outsiderth = value
        self.m_outsideRth = value

    @property
    def action(self):
        return self._action
    @action.setter
    def action(self, value):
        self._action = value
        self.m_action = value

    @property
    def quantity(self):
        return self._quantity
    @quantity.setter
    def quantity(self, value):
        self._quantity = value
        self.m_totalQuantity = value

    @property
    def transmit(self):
        return self._transmit
    @transmit.setter
    def transmit(self, value):
        self._transmit = value
        self.m_transmit = value

    @property
    def lmt_price(self):
        return self._lmt_price
    @lmt_price.setter
    def lmt_price(self, value):
        self._lmt_price = value
        self.m_lmtPrice = value

    @property
    def order_type(self):
        return self._order_type
    @order_type.setter
    def order_type(self, value):
        self._order_type = value
        self.m_orderType = value



    def __str__(self):
        d1 = {True: '是', False: '否'}
        d2 = {'BUY': '买', 'SELL': '卖'}
        d3 = {'LMT': '限价单', 'MKT': '市价单'}
        return '常规交易时间以外:{0}, 买/卖:{1}, 数量:{2}, 是否传送:{3}, 订单类型:{4}, 限价:{5}'.format(d1[self.outsiderth],
            d2[self.action], self.quantity, d1[self.transmit], d3[self.order_type], self.lmt_price)


class OpenOrder(object):
    def __init__(self):
        self.order_id = 0
        self.parent_id = 0
        self.symbol = ''
        self.action = ''
        self.lmt_price = 0.0
        self.quantity = 0
        self.order_type = ''
        self.status = None
        self.filled = 0
        self.remaining = 0
        self.avg_filled_price = 0.0
        self.last_filled_price = 0.0

    def __str__(self):
        return '订单id:{0}, 父订单id:{1}, 证券代码:{2}, 动作:{3}, 限价:{4}, 订单大小:{5}, 订单类型:{6}, 订单状态:{7}, 已成交:{8}, 剩余:{9}, 平均成交价:{10}, 最后成交价{11}'.format(
            self.order_id, self.parent_id, self.symbol, self.action, self.lmt_price, self.quantity, self.order_type,
            self.status, self.filled, self.remaining, self.avg_filled_price, self.last_filled_price
        )

