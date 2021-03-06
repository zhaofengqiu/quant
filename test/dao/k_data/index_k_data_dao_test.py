import unittest

from dao.k_data.index_k_data_dao import index_k_data_dao
from log.quant_logging import logger
from test import before_run


class Index_K_Data_Dao_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def get_index_k_data_test(self):

        df = index_k_data_dao.get_k_data("^HSI", start="2018-01-01", end="2018-05-21")
        logger.debug(df.head())
        self.assertIsNotNone(df)

    def get_sh_k_data(self):
        df = index_k_data_dao.get_sh_k_data( start="2018-01-01", end="2018-05-21")
        logger.debug(df.head())
        self.assertIsNotNone(df)



