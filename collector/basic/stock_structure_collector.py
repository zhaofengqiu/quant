# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/06


from dao.data_source import dataSource
from log.quant_logging import logger
from crawler.sina_finance_api import sina_finance_api
import time
from dao.basic.stock_industry_dao import stock_industry_dao

def collect_all():
    df = stock_industry_dao.get_list()
    for code in df['code'].values:
        try:
            collect_single(code)
            time.sleep(1)
        except Exception as e:
            logger.error(repr(e))


def collect_single(code, retry=0):

    if retry > 3:
        return
    try:
        data = sina_finance_api.get_stock_structure_by_code(code)
        if data is not None:
            data = data.drop_duplicates('date', 'first')
            data.to_sql('stock_structure', dataSource.mysql_quant_engine, if_exists='append', index=False)
    except Exception as e:
        retry += 1
        collect_single(code, retry)