#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年10月02日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""


import time
import logging
import threading
from ib.opt.connection import Connection
from ibapi.handler import Handler
from ibapi.contract import Contract
from ibapi.order import Order

log = logging.getLogger('root')


class TWS(object):
    def __init__(self, config):
        self.mutex = threading.Lock()
        self.tick_id = 0
        self.config = config
        self.conn = self.get_connection()
        self.handler = Handler()
        self.data = self.handler.data
        self.register()
        self.subscribe_symbols = {}

    def subscribe_mkt_data(self):
        if 'STOCK' in self.config['MKT_DATA']:
            for s in self.config['MKT_DATA']['STOCK'].split(','):
                if len(s) > 0:
                    self.subscribe(s)
        if 'OPTION' in self.config['MKT_DATA']:
            for s in self.config['MKT_DATA']['OPTION'].split(','):
                if len(s) > 0:
                    self.subscribe(s)

    def get_connection(self):
        section = self.config['TWS']
        host = section['HOST']
        port = int(section['PORT'])
        client = int(section['CLIENT'])
        conn = Connection.create(host=host, port=port, clientId=client)
        conn.connect()
        time.sleep(1)
        if not conn.isConnected():
            log.error('tws connect error!')
            raise Exception('tws connect error!')
        else:
            log.info('tws connected!')
        return conn

    def register(self):
        conn, handler = self.conn, self.handler
        conn.registerAll(handler.watch_all)
        handlers = [getattr(handler, f) for f in dir(handler) if callable(getattr(handler, f)) and f.find('hand_') == 0]
        for h in handlers:
            conn.unregister(handler.watch_all, h.__dict__['msg_hook'])
            conn.register(h, h.__dict__['msg_hook'])
        log.info('register done!')

    def run(self):
        self.conn.reqAccountUpdates(True, '')
        self.conn.reqIds(1)
        self.subscribe_mkt_data()
        log.info('tws is running!')

    def stop(self):
        self.conn.disconnect()
        log.info('tws disconnected')

    def get_account(self):
        return self.data['account']

    def get_positions(self):
        return self.data['account'].positions

    @staticmethod
    def create_contract(symbol, sec_type='STK', expiry='', strike=0.0, right=''):
        contract = Contract()
        contract.symbol = symbol
        contract.sec_type = sec_type
        contract.exchange = 'SMART'
        contract.primary_exch = 'SMART'
        contract.currency = 'USD'
        contract.expiry = expiry
        contract.strike = strike
        contract.right = right
        return contract

    @staticmethod
    def create_order(action, quantity, price=None):
        order = Order()
        order.outsiderth = True
        order.action = action
        order.quantity = quantity
        order.transmit = True
        if price is not None:
            order.order_type = 'LMT'
            order.lmt_price = price
        else:
            order.order_type = 'MKT'
        return order

    def buy(self, symbol, quantity, price=None):
        order_id = self.data['next_vid']
        log.info("Orderid: ", order_id)
        contract = self.create_contract(symbol)
        order = self.create_order('BUY', quantity, price)
        self.conn.placeOrder(order_id, contract, order)
        time.sleep(1)
        self.conn.reqIds(1)
        return order_id

    def sell(self, symbol, quantity, price=None):
        order_id = self.data['next_vid']
        log.info("Orderid: ", order_id)
        contract = self.create_contract(symbol)
        order = self.create_order('SELL', quantity, price)
        self.conn.placeOrder(order_id, contract, order)
        time.sleep(1)
        self.conn.reqIds(1)
        return order_id

    def cancel_order(self, order_id):
        self.conn.cancelOrder(order_id)
        log.info("Cancel Order:", order_id)

    def cancel_all_orders(self):
        orders = self.get_open_orders()
        for order in orders:
            self.cancel_order(order.order_id)
        log.info('Orders of all canceled')

    def get_open_orders(self):
        self.data['open_orders'] = {}
        self.conn.reqAllOpenOrders()       # 该函数主动调用一次, 才会触发OpenOrder, OrderStatus事件
        while len(self.data['open_orders']) == 0:
            time.sleep(0.1)
            continue
        return self.data['open_orders'].values()

    def req_mkt_data(self, symbol, tick_id):
        # https://www.interactivebrokers.com/cn/software/api/apiguide/java/reqmktdata.htm
        arr = symbol.split('_')
        if len(arr) > 1:
            _symbol, expiry, strike, right = arr
            contract = self.create_contract(_symbol, 'OPT', expiry, strike, right)
        else:
            contract = self.create_contract(symbol)
        self.conn.reqMktData(tick_id, contract, '', False)

    def cancel_mkt_data(self, tick_id):
        self.conn.cancelMktData(tick_id)

    def get_tick_id(self):
        self.mutex.acquire()
        self.tick_id += 1
        self.mutex.release()
        return self.tick_id

    def subscribe(self, symbol):
        tick_id = self.get_tick_id()
        self.subscribe_symbols[symbol] = tick_id
        self.req_mkt_data(symbol, tick_id)
        log.info('market data [ %s ] subscribed!', symbol)

    def unsubscribe(self, symbol):
        tick_id = self.subscribe_symbols[symbol]
        self.cancel_mkt_data(tick_id)
        self.mutex.acquire()
        del self.subscribe_symbols[symbol]
        del self.handler.data['mkt_data'][tick_id]
        del self.handler.data['opt_greek'][tick_id]
        self.mutex.release()
        log.info('market data [ %s ] unsubscribed!', symbol)

    def get_subscribe_data(self):
        arr = []
        self.mutex.acquire()
        for symbol, tick_id in self.subscribe_symbols.items():
            if tick_id not in self.handler.data['mkt_data']:
                continue
            data = self.handler.data['mkt_data'][tick_id]
            data.symbol = symbol
            arr.append(data)
        self.mutex.release()
        return arr

    def get_option_greek(self):
        arr = []
        self.mutex.acquire()
        for symbol, tick_id in self.subscribe_symbols.items():
            if not symbol.find('_') > 0:
                continue
            if tick_id not in self.handler.data['opt_greek']:
                continue
            data = self.handler.data['opt_greek'][tick_id]
            data.symbol = symbol
            arr.append(data)
        self.mutex.release()
        return arr