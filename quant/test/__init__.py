# -*- coding: UTF-8 -*-
# greg.chen - 2018/5/21

from sqlalchemy import create_engine

from quant.config import config
from quant.dao.data_source import dataSource
from quant.log.quant_logging import quant_logging as logging

PROJECT_NAME = "quant-test"


def init_db():
    default_config = config['default']

    # 如果配置DATABASE_QUANT_URI属性, 实例化mysql_quant_engine
    if default_config.DATABASE_QUANT_URI:
        # 使用单例模式保存数据库engine
        mysql_quant_engine = create_engine(default_config.DATABASE_QUANT_URI, encoding='utf8',
                                           convert_unicode=True, pool_size=10, pool_recycle=1200)
        dataSource.mysql_quant_engine = mysql_quant_engine


def init_logger():
    default_config = config['default']
    # 使用单例模式保存logger
    logging.create_logger(default_config.DEBUG, PROJECT_NAME)


def before_run():
    init_logger()
    init_db()