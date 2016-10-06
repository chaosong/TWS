#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on 2016年09月29日
@author: gongqingyi
@email:  gongqingyi@qq.com
"""


class Account(object):
    account_code = ''                      #账户号码
    net_liquidation = 0.0                  #净清算
    cash = 0.0                             #现金余额
    initial_margin_requirement = 0.0       #初始保证金
    maintenance_margin_requirement = 0.0   #维持保证金

    available_funds = 0.0                  #剩余流动性
    buying_power = 0.0                     #购买力
    cushion = 0.0                          #剩余杠杆比率
    total_positions_value = 0.0            #持仓总成本

    regt_margin = 0.0                      #当前保证金
    realized_pnl = 0.0                     #已实现盈亏
    unrealized_pnl = 0.0                   #未实现盈亏

    stock_mkt_value = 0.0                  #股票头寸总价值
    option_mkt_value = 0.0                 #期权头寸总价值

    accrued_cash = 0.0                     #累计利息

    positions = {}                         #投资组合信息

    def __str__(self):
        return ('账户号码:{0}, 净清算:{1}, 现金余额:{2}, 初始保证金:{3}, 维持保证金:{4}, 剩余流动性:{5}, 购买力:{6}, '
                '剩余杠杆比率:{7}, 持仓总成本:{8}, 当前保证金:{9}, 已实现盈亏:{10}, 未实现盈亏:{11}, 股票头寸总价值:{12}, '
                '期权头寸总价值:{13}, 累积利息:{14}').format(
            self.account_code, self.net_liquidation, self.cash, self.initial_margin_requirement,
            self.maintenance_margin_requirement, self.available_funds, self.buying_power, self.cushion,
            self.total_positions_value, self.regt_margin, self.realized_pnl, self.unrealized_pnl,
            self.stock_mkt_value, self.option_mkt_value, self.accrued_cash)
