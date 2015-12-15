#!/usr/bin/env python
# coding=utf-8
from datetime import datetime
start = datetime(2010, 1, 1)
end = datetime(2015, 1, 1)
benchmark = 'SH50'
universe = set_universe("SH")
capital_base = 100000

window = 80  # 历史窗口长度
max_t = 30   # 持仓时间
max_n = 5    # 持仓数量
v_thres = 4  # 交易量倍数
r_thres = 0.05 # 收益率上限

def initialize(account):
    add_history('hist', window)
    account.hold_period = {}

def handle_data(account):
    buylist = []
    for stock in acount.universe:
        v = sum(account.hist[stock]['turnoverVol'].iloc[:-1]) / window
        p = account.hist[stock]['closePrice'].iloc[-1] / account.hist[stock]['preClosePrice'].iloc[-1] - 1
        if account.hist[stock]['turnoverVol'].iloc[-1] >= v_thres * v and 0 < p <= r_thres:
            buylist.append(stock)
    rebalance(account, buylist)

def rebalance(account, buylist):
    c = account.cash
    n = 0
    for stock, t in account.hold_period.items():
        if t == max_t:
            order_to(stock, 0)
            c += account.hist[stock]['closePrice'].iloc[-1] * account.stkpos.get(stock, 0)
            del account.hold_period[stock]
        else:
            account.hold_period[stock] += 1
    if n == max_n or buylist ==[]:
        return

    b = max_n - n
    buylist = [s for s in buylist if s not in account.hold_period]
    for stock in buylist[:b]:
        order(stock, c / b / account.hist[stock]['closePrice'].iloc[-1])
        account.hold_period[stock] = 0


