import numpy as np


class BenchmarkPortfolio(object):

    def __init__(self, data_handler, risk_free_rate, bench_equity,
                 cash_pct=0.50, equity_pct=0.50, bond_pct=0.00, bench_bond=None):
        self.data_handler = data_handler
        self.risk_free_rate = risk_free_rate/365.0
        self.bench_equity = bench_equity
        self.cash_pct = cash_pct
        self.equity_pct = equity_pct
        self.bond_pct = bond_pct
        self.bench_bond = bench_bond
        self.past_days = 0
        self.cash = 1.00
        if self.bench_equity is not None:
            self.equity_value = {}
            for ticker in self.bench_equity.keys():
                self.equity_value[ticker] = []
        if self.bench_bond is not None:
            self.bond_value = {}
            for ticker in self.bench_bond.keys():
                self.bond_value[ticker] = []

    def update_benchmark_value(self, start_time, end_time):

        self.past_days = (end_time-start_time).days
        self.cash = np.exp(self.past_days * self.risk_free_rate)

        if self.bench_equity is not None:
            for ticker in self.bench_equity.keys():
                self.equity_value[ticker].append(self.data_handler.get_last_close(ticker))

        if self.bench_bond is not None:
            for ticker in self.bench_bond.keys():
                self.equity_value[ticker].append(self.data_handler.get_last_close(ticker))
