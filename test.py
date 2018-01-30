import os
import pandas as pd
from RookieQuant.data_handler.CSV_bar_handler import CsvBarDataHandler
import pyodbc
import pandas as pd

#
# index_col = 0, names = (
#     "Date", "Open", "High", 'Low',
#     "Close", "Volume", "Adj Close"
# )
# )
cursor = pyodbc.connect(
    r'DRIVER={ODBC Driver 13 for SQL Server};'
    r'SERVER=192.30.1.40;'
    r'DATABASE=StockBase;'
    r'UID=du_songsy;'
    r'PWD=songsy;')

sqlcmd = '''SELECT [BargainDate],[OpenPrice],[MaxPrice],[MinPrice],[ClosePrice],[BargainAmount],[StockCode]
        FROM [StockBase].[dbo].[Quotation] where StockCode='000001'
        and BargainDate>='2017/1/1' and BargainDate<='2017/12/31'
        order by StockCode, BargainDate'''
df = pd.read_sql(sqlcmd, con=cursor)
print(df)
df.rename(columns={'BargainDate': 'Date', 'OpenPrice': 'Open',
                    'MaxPrice': 'High', 'MinPrice': 'Low', 'BargainAmount': 'Volume',
                    'ClosePrice': 'Close', 'StockCode': 'Ticker'}, inplace=True)
date_column = (pd.to_datetime(df['Date'])).tolist()
df.index = date_column
df.drop('Date', axis=1, inplace=True)
df['Adj Close'] = df['Close']
print(df)



#ticker_path = os.path.join(self.csv_dir, "%s.csv"%ticker)

"""
# self.tickers_data[ticker] = 
"""
#
# ticker_path = os.path.join("H:\Github\RookieQuant\data", "SP500.csv")
#
# sp_data = pd.io.parsers.read_csv(
#             ticker_path, header=0, parse_dates=True,
#             index_col=0, names=(
#                 "Date", "Open", "High", 'Low',
#                 "Close", "Volume", "Adj Close"
#             )
#         )
# sp_data["Ticker"] = "SP500"
# SP =
# print(sp_data)


