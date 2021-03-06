# ae_h - 2018/7/13

import pandas as pd

from pitcher.domain.portfolio import Portfolio


class Context:
    def __init__(self, start, end, base_capital):
        # 开始时间
        self.start = start
        # 结束时间
        self.end = end
        # 初始金额
        self.init_capital = base_capital
        # 总金额
        self.base_capital = base_capital

        self.pool = []
        # 账户余额
        self.blance = base_capital

        # 下单记录
        self.order_book = []
        # 投资组合, 'code', 'shares', 'price', 'total'
        self.portfolio = Portfolio()
        # 当前时间
        self.current_date = None
        # 印花税
        self.tax_rate = 0.001
        # 佣金, 双边收费
        self.commission_rate = 0.00025
        # 记录每日收益
        self.profits = []

    def __getattr__(self, item):
        return item
