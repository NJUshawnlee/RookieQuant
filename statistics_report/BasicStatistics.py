from RookieQuant.statistics_report.base import AbstractStatistics


import datetime
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class BasicStatisticsReport(AbstractStatistics):

    def __init__(self, portfolio_handler, benchmark=None):

        self.benchmark = None
        self.drawdowns = [0]
        self.drawdowns_pct = [0.0]
        self.equity = []
        self.equity_benchmark = [1.0]
        self.equity_returns = [0.0]
        self.net_equity = [1.0]
        self.timeseries = ["0000-00-00 00:00:00"]
        self.benchmark_value = [1.0]


        current_equity = portfolio_handler.portfolio.equity
        self.high_water_mark = [current_equity]
        self.equity.append(current_equity)

    def update(self, timestamp, portfolio_handler, benchmark):

        if timestamp != self.timeseries[-1]:


            current_equity = portfolio_handler.portfolio.equity

            self.equity.append(current_equity)
            self.timeseries.append(timestamp)
            self.net_equity.append(self.equity[-1]/self.equity[0])

            pct = ((self.equity[-1] - self.equity[-2])/self.equity[-1])*100
            self.equity_returns.append(round(pct, 4))

            self.high_water_mark.append(max(self.high_water_mark[-1], self.equity[-1]))
            self.drawdowns.append(self.high_water_mark[-1]-self.equity[-1])
            self.drawdowns_pct.append(-self.drawdowns[-1]/self.high_water_mark[-1])

        cur_equity_value = 0.0
        if benchmark.bench_equity is not None:
            for ticker, pct in benchmark.bench_equity.items():
                cur_equity_value += benchmark.equity_value[ticker][-1] \
                                / benchmark.equity_value[ticker][0] * pct

        cur_bond_value = 0.0
        if benchmark.bench_bond is not None:
            for ticker, pct in benchmark.bench_bond.items():
                cur_bond_value += benchmark.bond_value[ticker][-1] \
                              / benchmark.bond_value[ticker][0] * pct

        self.benchmark_value.append(benchmark.cash_pct * benchmark.cash + \
                               benchmark.equity_pct * cur_equity_value + \
                               benchmark.bond_pct * cur_bond_value)

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

        sns.set_style("whitegrid")
        fig = plt.figure()
        current_palette = sns.color_palette()

        df = pd.DataFrame()
        df["equity"] = pd.Series(self.equity, index=self.timeseries)
        df["net_equity"] = pd.Series(self.net_equity, index=self.timeseries)
        df["benchmark"] =  pd.Series(self.benchmark_value, index=self.timeseries)
        df["drawdowns"] = pd.Series(self.drawdowns, index=self.timeseries)
        df["drawdowns_pct"] = pd.Series(self.drawdowns_pct, index=self.timeseries)

        ax1 = fig.add_subplot(221, ylabel='Equity Curve')
        df["equity"].plot(ax=ax1, color=current_palette[0], label='Equity')
        ax1.yaxis.grid(linestyle=':')
        ax1.xaxis.grid(linestyle=':')
        ax1.legend()

        ax2 = fig.add_subplot(222, ylabel='Net Equity')
        df["net_equity"].plot(ax=ax2, color=current_palette[1], label='Net Equity')
        df["benchmark"].plot(ax=ax2, color=current_palette[2], label='Benchmark')
        ax2.yaxis.grid(linestyle=':')
        ax2.xaxis.grid(linestyle=':')
        ax2.axhline(y=1, color=current_palette[1], linestyle='dashed')
        ax2.legend()

        ax3 = fig.add_subplot(223, ylabel='Drawdowns')
        df["drawdowns"].plot(ax=ax3, color=current_palette[3], label='Drawdowns')
        ax3.yaxis.grid(linestyle=':')
        ax3.xaxis.grid(linestyle=':')
        ax3.legend()

        ax4 = fig.add_subplot(224, ylabel="Drawdown pct")
        ax4.yaxis.grid(linestyle=':')
        ax4.xaxis.grid(linestyle=':')
        df["drawdowns_pct"].plot(ax=ax4, kind='area', alpha=0.5,
                                 color=current_palette[2], label='Drawndown Pct')
        ax4.legend()
        plt.show()

    def calculate_active_sharp(self):
            pass

    def calculate_tracking_error(self):
            pass

    def calculate_residual_risk(self):
            pass





















