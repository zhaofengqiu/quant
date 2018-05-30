# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from quant.dao.k_data_dao import k_data_dao
from datetime import datetime
from quant.log.quant_logging import quant_logging as logging
from quant.models.base_model import BaseModel
from quant.feature_utils.feature_collector import get_col_name_list, collect_features
from sklearn.decomposition import PCA
from sklearn import preprocessing
from sklearn.manifold import TSNE
from sklearn.metrics import accuracy_score
from quant.dao.k_data_model_log_dao import k_data_model_log_dao


class LogisticRegressionModel(BaseModel):
    """
        1. 70% training/grid search 选择超参数
        2. 30% test
    """

    def training_model(self, code):
        # 从数据库中获取2015-01-01到今天的所有数据
        data, features = k_data_dao.get_k_data_with_features(code, '2015-01-01', datetime.now().strftime("%Y-%m-%d"))

        logging.logger.debug("features:%s" % features)

        # 数据按30%测试数据, 70%训练数据进行拆分
        X_train, X_test, y_train, y_test = train_test_split(data[features], data['next_direction'], test_size=.3,
                                                            shuffle=False)

        X_train = preprocessing.scale(X_train)
        X_test = preprocessing.scale(X_test)

        # 交叉验证查找合适的超参数: penalty, C
        # penalty
        tuned_parameters = {
            'penalty': ['l1', 'l2'],
            'C': [0.001, 0.01, 0.1, 1, 10, 100]
        }
        # 网格搜索训练
        grid = GridSearchCV(LogisticRegression(), tuned_parameters, cv=None, n_jobs=-1)
        grid.fit(X_train, y_train)
        logging.logger.debug(grid.best_estimator_)  # 训练的结果
        logging.logger.debug("logistic regression's best score: %.4f" % grid.best_score_)  # 训练的评分结果

        logistic_regression = grid.best_estimator_
        # 使用训练数据, 重新训练
        logistic_regression.fit(X_train, y_train)

        # 使用测试数据对模型进评平分
        y_test_pred = logistic_regression.predict(X_test)

        # test_score = logistic_regression.score(X_test, y_test)

        # 在测试集中的评分
        test_score = accuracy_score(y_test, y_test_pred)
        logging.logger.debug('test score: %.4f' % test_score)

        # 使用所有数据, 重新训练
        logistic_regression.fit(data[features], data['next_direction'])

        # 记录日志
        k_data_model_log_dao.insert(code=code, name="LogisticRegressionModel"
                                    , best_estimator=grid.best_estimator_,
                                    train_score=grid.best_score_, test_score=test_score)