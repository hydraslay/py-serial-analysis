from copy import deepcopy

import numpy as np

tag = 'USD/JPY'
unit_lot = 0.01
lot_amount = 100000
leverage_rate = 1000

spread_pips = 0.015
wave_range = 0.010


def buy_price(price):
    low = price + spread_pips - wave_range
    high = price + spread_pips + wave_range
    return np.random.uniform(low=low, high=high)


def sell_price(price):
    low = price - wave_range
    high = price + wave_range
    return np.random.uniform(low=low, high=high)

class Account(object):
    # state (10): [
    #      0     balance,
    #      1     buy position(lot),
    #      2     avg cost buy,
    #      3     sell position(lot),
    #      4     avg cost sell,
    #      5     open,
    #      6     hi,
    #      7     low,
    #      8     close,
    #      9     volume
    #           ]
    def __init__(self, verbose=False):
        self.state = np.zeros(20)
        self.threshold = 0.5
        self.verbose = verbose

    def __repr__(self):
        return 'Account state: ' \
               ' balance: {} '\
               ' buy position : {} avg cost: {}' \
               ' sell position: {} avg cost: {}'.format(self.balance, self.pos_buy, self.cost_buy, self.pos_sell, self.cost_sell)

    def get_data(self):
        return self.state

    @property
    def balance(self):
        return self.state[0]

    def set_balance(self, x0):
        self.state[0] = x0

    @property
    def pos_buy(self):
        return self.state[1]

    def set_pos_buy(self, pos):
        self.state[1] = pos

    @property
    def cost_buy(self):
        return self.state[2]

    def set_cost_buy(self, cost):
        self.state[2] = cost

    @property
    def pos_sell(self):
        return self.state[3]

    def set_pos_sell(self, pos):
        self.state[3] = pos

    @property
    def cost_sell(self):
        return self.state[4]

    def set_cost_sell(self, cost):
        self.state[4] = cost

    @property
    def market_close(self):
        return self.state[8]

    @property
    def exposure(self):
        exposure = 0
        if self.pos_buy > 0:
            exposure += self.calc_profit(self.cost_buy - self.market_close, self.pos_buy)
        if self.pos_sell > 0:
            exposure += self.calc_profit(self.market_close - self.cost_sell, self.pos_sell)
        return exposure

    def tick_market(self, market):
        if isinstance(market, np.ndarray):
            market_info = market
        else:
            if isinstance(market, list):
                market_info = np.array(market)
            else:
                raise TypeError('{} is not supported', format(type(market)))

        # print('market: next tick')
        self.state[5:] = deepcopy(market_info)

        if self.exposure > self.balance:
            # print('market: busted!!')
            self.set_balance(self.balance - self.exposure)

        return self.balance

    def tp_buy(self, real_price):
        # take profit
        # print('tp(buy) {} at price {}'.format(self.pos_buy, real_price))
        profit = self.calc_profit(real_price - self.cost_buy, self.pos_buy)
        self.set_balance(self.balance + profit)
        self.set_pos_buy(0)
        self.set_cost_buy(0)
        if self.verbose:
            print('tp(buy) at {}, balance={}'.format(real_price, self.balance))
        return

    def tp_sell(self, real_price):
        # take profit
        # print('tp(sell) {} at price {}'.format(self.pos_sell, real_price))
        profit = self.calc_profit(self.cost_sell - real_price, self.pos_sell)
        self.set_balance(self.balance + profit)
        self.set_pos_sell(0)
        self.set_cost_sell(0)
        if self.verbose:
            print('tp(sell) at {}, balance={}'.format(real_price, self.balance))
        return

    def order_buy(self, lot, real_price):
        # print('buy {} at price {}'.format(lot, real_price))
        old_budget = self.calc_budget(self.cost_buy, self.pos_buy)
        budget = self.calc_budget(real_price, lot)
        self.set_pos_buy(self.pos_buy + lot)
        new_cost = self.calc_cost(old_budget + budget, self.pos_buy)
        self.set_cost_buy(new_cost)
        if self.verbose:
            print('order(buy) {} lot at {}'.format(lot, real_price))
        return

    def order_sell(self, lot, real_price):
        # print('sell {} at price {}'.format(lot, real_price))
        old_budget = self.calc_budget(self.cost_sell, self.pos_sell)
        budget = self.calc_budget(real_price, lot)
        self.set_pos_sell(self.pos_sell + lot)
        new_cost = self.calc_cost(old_budget + budget, self.pos_sell)
        self.set_cost_sell(new_cost)
        if self.verbose:
            print('order(sell) {} lot at {}'.format(lot, real_price))
        return

    def calc_budget(self, price, lot):
        return price * lot * lot_amount / leverage_rate

    def calc_profit(self, price, lot):
        return price * lot * lot_amount

    def calc_cost(self, budget, lot):
        return budget * leverage_rate / (lot * lot_amount)

    # action_bits -->
    #   0: take profit buy
    #   1: take profit sell
    #   2: order buy
    #   3: order sell
    #   4 ~ 7: binary unit count max = 1111 = 15
    def act(self, action_bits):
        if action_bits[0] > self.threshold:
            real_price = sell_price(self.market_close)
            self.tp_buy(real_price)

        if action_bits[1] > self.threshold:
            real_price = sell_price(self.market_close)
            self.tp_sell(real_price)

        lot = 0
        if action_bits[4] > self.threshold:
            lot += 8 * unit_lot
        if action_bits[5] > self.threshold:
            lot += 4 * unit_lot
        if action_bits[6] > self.threshold:
            lot += 2 * unit_lot
        if action_bits[7] > self.threshold:
            lot += 1 * unit_lot

        if lot > 0:
            if action_bits[2] > self.threshold and action_bits[2] > action_bits[3]:
                # buy
                real_price = buy_price(self.market_close)
                self.order_buy(lot, real_price)
            if action_bits[3] > self.threshold and action_bits[3] > action_bits[2]:
                # sell
                real_price = sell_price(self.market_close)
                self.order_sell(lot, real_price)

        return self.balance


def test():
    a = Account()
    a.set_balance(10000)
    print(a)

    a.tick_market([0,120., 121., 120.000, 10])
    # buy 0.03
    a.act([0., 0., 0., 1., 0., 0., 1., 1.])
    print(a)

    a.tick_market([0,120., 121., 119.000, 10])
    # tp
    a.act([0., 1., 0., 0., 0., 0., 0., 0.])
    print(a)

    a.tick_market([0,120., 121., 121.000, 10])
    # tp
    a.act([0., 0., 1., 0., 0., 0., 1., 0.])
    print(a)

    a.tick_market([0,120., 121., 122.000, 10])
    # tp
    a.act([1., 0., 0., 0., 0., 0., 0., 0.])
    print(a)

# test()
