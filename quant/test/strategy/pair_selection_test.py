# coding =utf-8
# ae_h - 2018/6/4
import unittest

from quant.test import before_run
from quant.strategy.pair_selection import code_muning, cal_p_value, cal_pair_stocks
import tushare as ts
from quant.dao.k_data.k_data_dao import K_Data_Dao


class PairStrategyTest(unittest.TestCase):

    def setUp(self):
        before_run()

    def test_strategy(self):
        data = ts.get_sz50s()
        code_set = code_muning(data)
        cal_pair_stocks(code_set)