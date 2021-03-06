# -*- coding: UTF-8 -*-
# greg.chen - 2018/6/7
from sqlalchemy import text

from common_tools.decorators import exc_time
from dao.data_source import dataSource
import pandas as pd
from dao import cal_direction
from crawler.yahoo_finance_api import yahoo_finance_api
import tushare as ts


class StockIndustryDao:

    @exc_time
    def get_by_code(self, code):
        sql = ("select `bk_code`, bk_name, code, name from stock_industry where code = %(code)s")

        df = pd.read_sql(sql=sql, params={"code":code}
                         , con=dataSource.mysql_quant_conn)

        return df


    @exc_time
    def get_list(self):
        sql = ("select `bk_code`, bk_name, code, name from stock_industry ")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def get_by_bkcode(self, bk_code):
        sql = text('''select `bk_code`, bk_name, code, name from stock_industry where bk_code = :bk_code and 
                          code not like '9%' and code not like '2%' and name not like '*%' and name not like '*st' and name not like 'st%' ''')

        df = pd.read_sql(sql=sql, params={"bk_code":bk_code}
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def get_bkcode_list(self):
        sql = ("select DISTINCT `bk_code` from stock_industry")

        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

    @exc_time
    def get_stock_code_list(self):
        # sql = ("select DISTINCT code from stock_industry")
        sql = text("select DISTINCT code FROM stock_industry where code not like '9%' and code not like '2%'  and name not like '*%' and name not like '*st' and name not like 'st%'")
        df = pd.read_sql(sql=sql
                         , con=dataSource.mysql_quant_conn)

        return df

stock_industry_dao = StockIndustryDao()