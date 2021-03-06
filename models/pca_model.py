# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/28
from models.base_model import BaseModel
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.externals import joblib

from common_tools.decorators import exc_time


class PCAModel(BaseModel):
    model_name = 'pca'

    def __init__(self, module_name):
        self.module_name = module_name

    @exc_time
    def training_model(self, code, data, features):
        X = data[features]
        X = preprocessing.scale(X)

        pca = PCA(n_components=None)
        pca.fit(X)
        # 输出模型
        joblib.dump(pca, self.get_model_path(code, self.module_name, self.model_name))

    def load(self, code: object) -> object:
        pca = joblib.load(self.get_model_path(code, self.module_name, self.model_name))
        return pca
