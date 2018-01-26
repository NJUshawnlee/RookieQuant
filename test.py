import os
import pandas as pd
from RookieQuant.data_handler.CSV_bar_handler import CsvBarDataHandler

#ticker_path = os.path.join(self.csv_dir, "%s.csv"%ticker)

"""
# self.tickers_data[ticker] = 
"""

ticker_path = os.path.join("H:\Github\RookieQuant\data", "SP500.csv")

sp_data = pd.io.parsers.read_csv(
            ticker_path, header=0, parse_dates=True,
            index_col=0, names=(
                "Date", "Open", "High", 'Low',
                "Close", "Volume", "Adj Close"
            )
        )
sp_data["Ticker"] = "SP500"
SP =
print(sp_data)


