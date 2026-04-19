import pandas as pd

class Portfolio:
    def __init__(self, capital=100000):
        self.capital = capital
        self.positions = {}  # ticker: {'shares': , 'avg_price': , 'current_price': }
        self.history = []  # list of trades

    def position_size(self, ticker, price, atr, risk_percent=1):
        risk_amount = self.capital * risk_percent / 100
        stop_loss = atr * 2  # 2 ATR stop
        shares = risk_amount / stop_loss
        max_shares = self.capital * 0.1 / price  # max 10% allocation
        shares = min(shares, max_shares)
        return int(shares)

    def buy(self, ticker, shares, price):
        if ticker not in self.positions:
            self.positions[ticker] = {'shares': 0, 'avg_price': 0}
        cost = shares * price
        if cost > self.capital:
            return False  # insufficient funds
        self.capital -= cost
        total_shares = self.positions[ticker]['shares'] + shares
        self.positions[ticker]['avg_price'] = (
            (self.positions[ticker]['shares'] * self.positions[ticker]['avg_price'] + cost) / total_shares
        )
        self.positions[ticker]['shares'] = total_shares
        self.history.append({'action': 'BUY', 'ticker': ticker, 'shares': shares, 'price': price})
        return True

    def sell(self, ticker, shares, price):
        if ticker not in self.positions or self.positions[ticker]['shares'] < shares:
            return False
        self.positions[ticker]['shares'] -= shares
        proceeds = shares * price
        self.capital += proceeds
        self.history.append({'action': 'SELL', 'ticker': ticker, 'shares': shares, 'price': price})
        if self.positions[ticker]['shares'] == 0:
            del self.positions[ticker]
        return True

    def update_prices(self, prices):
        for ticker, price in prices.items():
            if ticker in self.positions:
                self.positions[ticker]['current_price'] = price

    def get_pnl(self):
        total_value = self.capital
        for pos in self.positions.values():
            total_value += pos['shares'] * pos.get('current_price', pos['avg_price'])
        return total_value - 100000  # assuming initial capital

    def get_allocation(self):
        alloc = {}
        for ticker, pos in self.positions.items():
            value = pos['shares'] * pos.get('current_price', pos['avg_price'])
            alloc[ticker] = value / (self.capital + sum(v['shares'] * v.get('current_price', v['avg_price']) for v in self.positions.values())) * 100
        return alloc