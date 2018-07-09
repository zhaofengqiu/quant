import unittest
from quant.test import before_run
from quant.dao.basic.stock_pool_dao import stock_pool_dao


class Stock_pool_Test(unittest.TestCase):
    def setUp(self):
        before_run()

    def test_init_pool(self):
        stock_pool_dao.init_pool();

    def test_get_list(self):
        df = stock_pool_dao.get_list()
        print(df)