import pandas as pd
import pyodbc

from RookieQuant.data_handler.DataFrame_bar_handler_base import DataFrameDataHandler

sws_sql_cmd = '''SELECT [BargainDate],[OpenPrice],[MaxPrice],[MinPrice],[ClosePrice],[BargainAmount],[StockCode]
            FROM [StockBase].[dbo].[Quotation] where StockCode='%s'
            and BargainDate>='%s' and BargainDate<='%s'
            order by StockCode, BargainDate'''

sws_sql_config = '' r'DRIVER={ODBC Driver 13 for SQL Server};' \
                 r''r'SERVER=192.30.1.40;' \
                 r''r'DATABASE=StockBase;' \
                 r''r'UID=du_songsy;' \
                 r''r'PWD=songsy;'  ''


class SqlBarDataHandler(DataFrameDataHandler):

    def __init__(self, sql_config, sql_cmd, sql_start_time, sql_end_time, events_queue,
                 init_tickers=None, start_time=None, end_time=None, period=86400,
                 calc_adj_returns=False):
        self.sql_config = sql_config
        self.sql_cmd = sql_cmd
        self.cursor = pyodbc.connect(self.sql_config)
        self.sql_start_time = sql_start_time
        self.sql_end_time = sql_end_time
        super().__init__(events_queue, init_tickers, start_time, end_time,
                         period, calc_adj_returns)
        self.sql_cmd = sql_cmd

    def get_data_from_sql(self, ticker):
        start = self.sql_start_time
        end = self.sql_end_time
        sql_cmd = self.sql_cmd % (ticker, start, end)
        df = pd.read_sql(sql_cmd, con=self.cursor)
        df.rename(columns={'BargainDate': 'Date', 'OpenPrice': 'Open',
                           'MaxPrice': 'High', 'MinPrice': 'Low', 'BargainAmount': 'Volume',
                           'ClosePrice': 'Close', 'StockCode': 'Ticker'}, inplace=True)
        date_column = (pd.to_datetime(df['Date'])).tolist()
        df.index = date_column
        df.drop('Date', axis=1, inplace=True)
        df['Adj Close'] = df['Close']
        self.tickers_data[ticker] = df

    def get_dataframe_bar_data(self, ticker):
        self.get_data_from_sql(ticker)


# data = SqlBarDataHandler(sws_sql_config, "2017/1/1", "2017/12/31", sws_sql_cmd)

