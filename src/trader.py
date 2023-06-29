import json

# find 2 highest idx
def find_highest_indexes(group: list, count=2, exclude=()):
    non_excluded = [x for i, x in enumerate(group) if i not in exclude]
    n_highest = sorted(non_excluded, reverse=True)[:count]
    indexes = []
    for idx, item in enumerate(group):
        if item in n_highest:
            indexes.append(idx)
    return indexes

class SimulationWrapper:
    def __init__(self, prices: tuple):
        self.prices = prices

def save(trade_data):
    with open("trade_info.json", "w") as f:
        f.write(json.dumps(trade_data, indent=4))

class Trader:
    def __init__(self, sim, profit_take=1.05, loss_limit=0.95):
        self.take_profit_at = profit_take
        self.take_loss_at = loss_limit

        # (stock, buy_price, buy_amount)
        self.outgoing_trades = []
        self.sim = sim
        self.bal = 10000
        self.inv = [0, 0, 0, 0]

    # amount
    def buy(self, stock, count):
        if count < 0: # buy max
            count = self.bal // self.sim.prices[stock]
        expense = count * self.sim.prices[stock]
        assert self.bal - expense >= 0
        self.bal -= expense
        self.inv[stock] += count

    # dollars
    def buy_amount(self, stock, amount):
        count = amount // self.sim.prices[stock]
        self.buy(stock, count)
        return count

    def sell(self, stock, count):
        assert self.inv[stock] >= count
        if count < 0: # sell max
            count = self.inv[stock]
        self.bal += count * self.sim.prices[stock]
        self.inv[stock] -= count

    def sell_amount(self, stock, amount):
        count = amount // self.sim.prices[stock]
        self.sell(stock, count)
        return count
  
    def update(self):
        transaction_performed = {"sell": [], "buy": []}
        # check past trades
        sold = []
        for i in self.outgoing_trades:
            stock, buy_price, buy_amount = i
            buy_net = buy_price * buy_amount
            curr_net = self.sim.prices[stock] * buy_amount
            if curr_net >= self.take_profit_at * buy_net \
                    or curr_net <= self.take_loss_at * buy_net:
                try:
                    self.sell(stock, buy_amount)
                    print(f"Transaction: SELL {buy_amount} shares of {stock} ({self.sim.prices[stock]} each). New bal: {self.bal}")
                    transaction_performed["sell"].append((stock, int(buy_amount)))
                    sold.append(stock)
                except AssertionError as e:
                    raise e

                self.outgoing_trades.remove(i)

        outgoing_count = len(self.outgoing_trades)
        current_stocks = [x[0] for x in self.outgoing_trades]
        current_stocks.extend(sold)
        if outgoing_count <= 1:
            highest = find_highest_indexes(self.sim.prices, 2, exclude=current_stocks)
            highest1 = highest[0]
            highest2 = highest[1]
        
        if outgoing_count == 1:
            count = self.buy_amount(highest1, self.bal)
            transaction_performed["buy"].append((highest1, count))
            print(f"Transaction: BUY {count} shares of {highest1} ({self.sim.prices[highest1]} each). New bal: {self.bal}")
            self.outgoing_trades.append((highest1, self.sim.prices[highest1], self.inv[highest1]))
        elif outgoing_count == 0:
            amount1 = 0.75 * self.bal
            amount2 = 0.25 * self.bal
            
            count = self.buy_amount(highest1, amount1)
            transaction_performed["buy"].append((highest1, count))
            self.outgoing_trades.append((highest1, self.sim.prices[highest1], self.inv[highest1]))
            print(f"Transaction: BUY {count} shares of {highest1} ({self.sim.prices[highest1]} each). New bal: {self.bal}")
            
            count = self.buy_amount(highest2, amount2)
            transaction_performed["buy"].append((highest2, count))
            self.outgoing_trades.append((highest2, self.sim.prices[highest2], self.inv[highest2]))
            print(f"Transaction: BUY {count} shares of {highest2} ({self.sim.prices[highest2]} each). New bal: {self.bal}")

        return transaction_performed

    def get_nw(self):
        nw = self.bal
        for stock, price in enumerate(self.sim.prices):
            nw += self.inv[stock] * price
        return nw
