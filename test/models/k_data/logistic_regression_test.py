import unittest
from datetime import datetime

from dao.k_data.index_k_data_dao import index_k_data_dao
from dao.k_data.k_data_dao import k_data_dao
from log.quant_logging import logger
from models.k_data.logistic_regression_classifier import LogisticRegressionClassifier
from config import default_config
import futuquant as ft

from models.pca_model import PCAModel


class Logistic_Regression_Test(unittest.TestCase):
    def setUp(self):
        # before_run()
        self.futu_quote_ctx = ft.OpenQuoteContext(host=default_config.FUTU_OPEND_HOST, port=default_config.FUTU_OPEND_PORT)

    def tearDown(self):
        self.futu_quote_ctx.close()

    def test_training(self):
        code = '600196'
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_training_data(code, '2012-01-01',datetime.now().strftime("%Y-%m-%d"), self.futu_quote_ctx)

        data.to_csv("result.csv")
        logger.debug("features:%s, length:%s" % (features, len(features)))

        pac = PCAModel('k_data');
        pac.training_model(code=code, data=data,features=features)

        model = LogisticRegressionClassifier()
        model.training_model(code, data, features)



    def test_predict(self):
        code = '600196'
        df_index = index_k_data_dao.get_rel_price();

        df, features = k_data_dao.get_k_predict_data_with_features(code, df_index)
        logger.debug("features:%s, length:%s" % (features, len(features)))

        df.to_csv("result.csv")
        model = LogisticRegressionClassifier()
        y_predict = model.predict(code, df[features])

        print(y_predict)
