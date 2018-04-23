# Close price predict

import tushare as ts
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
from sklearn.linear_model import LassoCV
from sklearn.model_selection import train_test_split
from custom_feature_calculating import feature as feature_service
import pandas as pd
from dao import engine


def training(show_plot=False):
    sql = 'SELECT  t1.open, t1.close, t1.high, t1.low, t1.vol as volume,t2.close as rt_sh' \
          ' from tick_data_1min_hs300 t1' \
          ' LEFT JOIN tick_data_1min_sh t2 on t1.datetime = t2.datetime and t2.code=\'sh\'' \
          ' where t1.datetime > \'2018-01-01\''

    df = pd.read_sql_query(sql, engine.create())
    df = feature_service.fill_for_line_regression(df)

    df.to_csv('result.csv')
    df = df.dropna()

    feature = ['open', 'ma5', 'ma10', 'ma20', 'ubb', 'lbb', 'cci', 'evm', 'ewma', 'fi']
    # ^^^^^^^ need more features

    df_x_train, df_x_test, df_y_train, df_y_test = train_test_split(df[feature], df['close'], test_size=.3)

    # choose linear regression model

    reg = LassoCV(alphas=[1, 0.1, 0.001, 0.0005], normalize=True)

    # fit model with data(training)
    reg.fit(df_x_train, df_y_train)

    # test predict
    df_y_test_pred = reg.predict(df_x_test)

    # The Coefficients (系数 auto gen)
    print('Coefficients: \n', reg.coef_)
    # The Intercept(截距/干扰/噪声 auto gen)
    print('Intercept: \n', reg.intercept_)
    # The mean squared error(均方误差)
    print("Mean squared error: %.2f"
          % mean_squared_error(df_y_test, df_y_test_pred))
    # r2_score - sklearn评分方法
    print('Variance score: %.2f' % r2_score(df_y_test, df_y_test_pred))

    # Plot outputs
    if show_plot:
        plt.scatter(df_x_test['open'], df_y_test, color='black')
        plt.plot(df_x_test['open'], df_y_test_pred, color='blue', linewidth=3)
        plt.show()


def predict(code='600179', show_plot=False):
    pass


if __name__ == "__main__":
    code = input("Enter the code: ")

    if not code.strip():
        training(show_plot=True)
    else:
        training(code)
