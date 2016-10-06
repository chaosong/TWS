#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月01日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

import logging
import functools
from ib.opt import message
from ibapi.tick import Tick, OptionGreek
from ibapi.account import Account
from ibapi.position import Position
import utility

log = logging.getLogger('root')


def handlermethod(msg_hook):
    def wrapper(handler):
        @functools.wraps(handler)
        def _wrapper(*args, **kwargs):
            return handler(*args, **kwargs)
        _wrapper.__dict__['msg_hook'] = msg_hook
        return _wrapper
    return wrapper


class Handler(object):
    def __init__(self):
        self.data = {
            'account': Account(),
            'mkt_data': {},
            'opt_greek': {},
            'open_orders': {},
            'next_vid': 0
        }

    @staticmethod
    def watch_all(msg):
        log.info('Watch All: %s', msg)

    @staticmethod
    @handlermethod(message.error)
    def hand_error(msg):
        log.error('Server Error: %s', msg)

    @handlermethod(message.connectionClosed)
    def hand_connection_closed(self, msg):
        log.info('Connection Closed!')

    @staticmethod
    @handlermethod(message.updateAccountTime)
    def hand_update_account_time(msg):
        pass

    @staticmethod
    @handlermethod(message.accountDownloadEnd)
    def hand_account_download_end(msg):
        pass

    @staticmethod
    @handlermethod(message.tickString)
    def hand_tick_string(msg):
        pass

    @staticmethod
    @handlermethod(message.tickGeneric)
    def hand_tick_generic(msg):
        pass

    @handlermethod(message.nextValidId)
    def hand_next_valid_id(self, msg):
        next_vid = int(msg.orderId)
        if self.data['next_vid'] < next_vid:
            self.data['next_vid'] = next_vid
        else:
            log.error("Next Valid Id Error!")

    @handlermethod(message.updateAccountValue)
    def hand_account_value(self, msg):
        account = self.data['account']
        if msg.key == 'AccountCode':          #账户号码
            account.account_code = msg.value
        if msg.key == 'NetLiquidation':       #净清算(★)
            account.net_liquidation = float(msg.value)
        if msg.key == 'CashBalance':          #现金余额
            account.cash = msg.value
        if msg.key == 'InitMarginReq':        #初始保证金
            account.initial_margin_requirement = msg.value
        if msg.key == 'MaintMarginReq':       #维持保证金
            account.maintenance_margin_requirement = msg.value

        if msg.key == 'AvailableFunds':       #剩余流动性
            account.available_funds = msg.value
        if msg.key == 'BuyingPower':          #购买力
            account.buying_power = msg.value
        if msg.key == 'Cushion':              #剩余杠杆比率
            account.cushion = msg.value
        if msg.key == 'GrossPositionValue':   #持仓总成本
            account.total_positions_value = msg.value

        if msg.key == 'RegTMargin':           #当前保证金
            account.regt_margin = msg.value
        if msg.key == 'RealizedPnL':          #已经实现盈亏
            account.realized_pnl = msg.value
        if msg.key == 'UnrealizedPnL':        #未实现盈亏
            account.unrealized_pnl = msg.value

        if msg.key == 'StockMarketValue':     #股票头寸总价值
            account.stock_mkt_value = msg.value
        if msg.key == 'OptionMarketValue':    #期权头寸总价值
            account.option_mkt_value = msg.value

        if msg.key == 'AccruedCash':          #累计利息
            account.accrued_cash = msg.value

    @handlermethod(message.updatePortfolio)
    def hand_position(self, msg):
        def get_id(c):
            d = {'C': '看涨期权(call)', 'P': '看跌期权(put)'}
            if c.m_secType == 'STK':
                return c.m_symbol
            elif c.m_secType == 'OPT':
                return '%s_%s_%s_%s' % (c.m_symbol, d[c.m_right], c.m_expiry, str(c.m_strike))
        position = Position()
        position.contract = msg.contract
        position.size = int(msg.position)
        position.mkt_price = round(float(msg.marketPrice), 2)
        position.mkt_value = round(float(msg.marketValue), 2)
        position.avg_cost = round(float(msg.averageCost), 2)
        position.cost = round(msg.position * float(msg.averageCost), 2)
        position.realized_pnl = round(float(msg.realizedPNL), 2)
        position.unrealized_pnl = round(float(msg.unrealizedPNL), 2)
        position.unrealized_ratio = round(float(msg.unrealizedPNL)/(abs(int(msg.position)) * float(msg.averageCost)), 2)
        pid = get_id(msg.contract)
        self.data['account'].positions[pid] = position

    @handlermethod(message.tickPrice)
    def hand_tick_price(self, msg):
        tid = msg.tickerId
        if tid not in self.data['mkt_data']:
            tk = Tick()
            self.data['mkt_data'][tid] = tk
        else:
            tk = self.data['mkt_data'][tid]
        tk.tid = tid
        tk.timestamp = utility.get_seconds()
        if msg.field == 1:
            tk.bid_price = msg.price
        if msg.field == 2:
            tk.ask_price = msg.price
        if msg.field == 4:
            tk.last_price = msg.price
        self.data['mkt_data'][tid] = tk

    @handlermethod(message.tickSize)
    def hand_tick_size(self, msg):
        tid = msg.tickerId
        if tid not in self.data['mkt_data']:
            tk = Tick()
            self.data['mkt_data'][tid] = tk
        else:
            tk = self.data['mkt_data'][tid]
        tk.tid = tid
        tk.timestamp = utility.get_seconds()
        if msg.field == 0:
            tk.bid_size = msg.size
        if msg.field == 3:
            tk.ask_size = msg.size
        if msg.field == 5:
            tk.last_size = msg.size
        if msg.field == 8:
            tk.volume = msg.size
        self.data['mkt_data'][tid] = tk

    @handlermethod(message.tickOptionComputation)
    def hand_option_greek(self, msg):
        if msg.field != 13:
            return
        tid = msg.tickerId
        if tid not in self.data['opt_greek']:
            og = OptionGreek()
            self.data['opt_greek'][tid] = og
        else:
            og = self.data['opt_greek'][tid]
        og.tid = tid
        og.timestamp = utility.get_seconds()
        og.implied_vol = round(msg.impliedVol, 6)
        og.delta = round(msg.delta, 6)
        og.gamma = round(msg.gamma, 6)
        og.vega = round(msg.vega, 6)
        og.theta = round(msg.theta, 6)
        og.div = round(msg.pvDividend, 6)
        og.opt_price = round(msg.optPrice, 2)
        self.data['opt_greek'][tid] = og

    @staticmethod
    @handlermethod(message.execDetails)
    def hand_exec_details(msg):
        print('ID', msg.execution.m_execId, 'PRICE', msg.execution.m_price)

    @staticmethod
    @handlermethod(message.commissionReport)
    def hand_commission_report(msg):
        print('ID', msg.commissionReport.m_execId, 'COM', msg.commissionReport.m_commission)

    @staticmethod
    @handlermethod(message.orderStatus)
    def hand_order_status(msg):
        print('Status==>:', msg)

    @staticmethod
    @handlermethod(message.openOrder)
    def hand_open_orders(msg):
        print('OpenOrder==>:', msg)

