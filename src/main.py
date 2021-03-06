#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年09月27日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""

import time
import logging
from common import *
from ibapi.context import Context
from ibapi.tws import TWS
from utility import async


class AppMain():
    def __init__(self):
        config = get_system_conf()
        self.tws = TWS(config)

    @async
    def account_info(self):
        print("=====================================================")
        print("                     账户信息                         ")
        print("=====================================================")
        while True:
            account = self.tws.get_account()
            print('Account: ', account)
            time.sleep(3)

    @async
    def position_info(self):
        print("=====================================================")
        print("                     头寸信息                         ")
        print("=====================================================")
        while True:
            positions = self.tws.get_positions()
            for k, v in positions.items():
                print("position: ", v)
                print('--------------------------')
            time.sleep(3)

    @async
    def subscribe_info(self):
        print("=====================================================")
        print("                     订阅数据                         ")
        print("=====================================================")
        while True:
            for v in self.tws.get_subscribe_data():
                print(v)
                print("-----------------------------------------")
            time.sleep(3)


    @async
    def opt_greek_info(self):
        print("=====================================================")
        print("                     期权数据                         ")
        print("=====================================================")
        while True:
            for v in self.tws.get_option_greek():
                print(v)
                print("-----------------------------------------")
            time.sleep(3)

    @async
    def order_info(self):
        print("=====================================================")
        print("                     挂单信息                         ")
        print("=====================================================")
        while True:
            orders = self.tws.get_open_orders()
            for order in orders:
                print(order)
                print('-----------------------------------------')
            time.sleep(3)


    def run(self):
        self.tws.run()
        time.sleep(1)
        self.account_info()
        self.position_info()
        self.subscribe_info()
        self.opt_greek_info()
        self.order_info()


        #id1 = self.tws.buy('UVXY', 25000, 16.2)
        #self.tws.cancel_order(id1)
        #time.sleep(2)
        #id2 = self.tws.sell('UVXY', 1, 45.0)
        #self.tws.cancel_order(id2)

    def stop(self):
        self.tws.stop()


if __name__ == '__main__':
    log = logging.getLogger('root')
    log.info('System start!')

    app = AppMain()
    app.run()
    time.sleep(10000)
    app.stop()
    log.info('System exit!')