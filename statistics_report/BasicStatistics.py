from RookieQuant.statistics_report.base import AbstractStatistics


import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class BasicStatisticsReport(AbstractStatistics):

    def __init__(self, portfolio_handler):

        self.drawdowns = [0]
        self.equity = []
        self.equity_returns = [0.0]

        self.timeseries = ["0000-00-00 00:00:00"]

        current_equity = portfolio_handler.portfolio.equity
        self.high_water_mark = [current_equity]
        self.equity.append(current_equity)

    def update(self, timestamp, portfolio_handler):

        if timestamp != self.timeseries[-1]:

            current_equity = portfolio_handler.portfolio.equity

            self.equity.append(current_equity)
            self.timeseries.append(timestamp)

            pct = ((self.equity[-1] - self.equity[-2])/self.equity[-1])*100
            self.equity_returns.append(round(pct, 4))

            self.high_water_mark.append(max(self.high_water_mark[-1], self.equity[-1]))
            self.drawdowns.append(self.high_water_mark[-1]-self.equity[-1])


    def get_results(self):

        timeseries = self.timeseries
        timeseries[0] = pd.to_datetime(timeseries[1]) - pd.Timedelta(days=1)

        statistics = {}
        statistics["sharpe"] = self.calculate_sharpe()
        statistics["drawdowns"] = pd.Series(self.drawdowns, index=timeseries)
        statistics["max_drawdown"] = max(self.drawdowns)
        statistics["max_drawdown_pct"] = self.calculate_max_drawdown_pct()
        statistics["equity"] = pd.Series(self.equity, index=timeseries)
        statistics["equity_returns"] = pd.Series(self.equity_returns, index=timeseries)

        return statistics

    def calculate_sharpe(self, benchmark_return = 0.0265):

        excess_returns = pd.Series(self.equity_returns) - benchmark_return/252

        return round(self.annualised_sharpe(excess_returns), 4)

    def annualised_sharpe(self, returns, N=252):

        return np.sqrt(N) * returns.mean() / returns.std()

    def calculate_max_drawdown_pct(self):

        drawdown_series = pd.Series(self.drawdowns)
        equity_series = pd.Series(self.equity)
        bottom_index = drawdown_series.idxmax()

        try:
            top_index = equity_series[:bottom_index].idxmax()
            pct = (
                ((equity_series.ix[top_index] - equity_series.ix[bottom_index]) /
                equity_series.ix[top_index] )* 100
            )
            return round(pct, 4)
        except ValueError:
            return np.nan

    def plot_results(self):

        sns.set()
        fig = plt.figure()


        df = pd.DataFrame()
        df["equity"] = pd.Series(self.equity, index=self.timeseries)
        df["equity_returns"] = pd.Series(self.equity_returns, index=self.timeseries)
        df["drawdowns"] = pd.Series(self.drawdowns, index=self.timeseries)

        ax1 = fig.add_subplot(221, ylabel='Equity')
        df["equity"].plot(ax=ax1, color=sns.color_palette()[0])

        ax2 = fig.add_subplot(222, ylabel='Equity Returns')
        df["equity_returns"].plot(ax=ax2, color=sns.color_palette()[1])

        ax3 = fig.add_subplot(223, ylabel='Drawdowns')
        df["drawdowns"].plot(ax=ax3, color=sns.color_palette()[2])

        plt.show()

    def calculate_active_sharp(self):
            pass

    def calculate_tracking_error(self):
            pass

    def calculate_residual_risk(self):
            pass





















