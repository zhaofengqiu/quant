import unittest
from quant.test import before_run
from quant.dao.k_data_dao import k_data_dao
from quant.log.quant_logging import quant_logging as logging


class K_Data_Dao_Test(unittest.TestCase):

    def setUp(self):
        before_run()

    def test_get_k_data(self):

        df = k_data_dao.get_k_data("600000", start="2015-01-01", end="2018-05-27")
        self.assertIsNotNone(df)
        df.to_csv("result.csv")
        i = 1
        while i < 100:

            next_direction = df.iloc[i]["next_direction"]
            p_change = df.iloc[i+1]["p_change"]

            # 如果next_direction ==0(代表跌), 检查下一日的p_change是否小于0
            # 验证next_direction是否正确
            if next_direction == 0:
                self.assertTrue(p_change <= 0)
            elif next_direction == 1:
                self.assertTrue(p_change > 0)

            i = i + 1






