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
    def __init__(self, init_funcd, max_margin_rate, verbose=False):
        self.state = np.zeros(20)
        self.state[0] = init_funcd
        self.init_fund = init_funcd
        self.max_margin_rate = max_margin_rate
        self.verbose = verbose
        self.max_exposure = 0
        self.max_drop_rate = 0
        self.lived_ticks = 0
        self.current_price = 0
        self.busted = False
        self.error = False

    def __repr__(self):
        return 'Account state: ' \
               ' balance: {} '\
               ' buy position : {} avg cost: {}' \
               ' sell position: {} avg cost: {}' \
               ' market: {} ' \
               ' exposure: {}'.format(self.balance, self.pos_buy, self.cost_buy, self.pos_sell, self.cost_sell, self.current_price, self.exposure)

    def get_data(self):
        return self.state

    def evaluate(self):
        # exposure : as 10%
        # win rate: x * win_rate * 100
        # max drop rate: x * (1 - max_drop_rate)
        return (self.balance - (self.exposure / 100)) * (1 - self.max_drop_rate) + self.lived_ticks

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
    def drop_rate(self):
        drop_rate = (self.init_fund - (self.balance - self.exposure)) / self.init_fund
        if drop_rate > 0:
            return drop_rate
        return 0

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
        self.current_price = self.market_close

        exposure = self.exposure
        # update max record
        self.max_exposure = exposure if self.max_exposure < exposure else self.max_exposure
        drop_rate = self.drop_rate
        self.max_drop_rate = drop_rate if drop_rate > self.max_drop_rate else self.max_drop_rate

        if self.exposure > self.balance:
            # print('market: busted!!')
            self.set_balance(self.balance - self.exposure)
            self.busted = True

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
        if budget > self.balance * self.max_margin_rate:
            return False
        self.set_pos_buy(self.pos_buy + lot)
        new_cost = self.calc_cost(old_budget + budget, self.pos_buy)
        self.set_cost_buy(new_cost)
        if self.verbose:
            print('order(buy) {} lot at {}'.format(lot, real_price))
        return True

    def order_sell(self, lot, real_price):
        # print('sell {} at price {}'.format(lot, real_price))
        old_budget = self.calc_budget(self.cost_sell, self.pos_sell)
        budget = self.calc_budget(real_price, lot)
        if budget > self.balance * self.max_margin_rate:
            return False
        self.set_pos_sell(self.pos_sell + lot)
        new_cost = self.calc_cost(old_budget + budget, self.pos_sell)
        self.set_cost_sell(new_cost)
        if self.verbose:
            print('order(sell) {} lot at {}'.format(lot, real_price))
        return True

    def calc_budget(self, price, lot):
        return price * lot * lot_amount / leverage_rate

    def calc_profit(self, price, lot):
        return price * lot * lot_amount

    def calc_cost(self, budget, lot):
        return budget * leverage_rate / (lot * lot_amount)

    # action_bits -->
    #   diff <10% do nothing
    #   [0] > 100, [1] = 0: take profit buy
    #   [1] > 100, [0] = 0: take profit sell
    #   [0] > [1]: order buy (diff / [1] = 10% -> 1 unit 0.01 lot )
    #   [1] > [0]: order sell
    #   no position but tp: balance -> -1
    def act(self, action_nums):
        if action_nums[0] == 0 and action_nums[1] == 0:
            return

        if action_nums[0] == 0 or action_nums[1] == 0:
            if action_nums[0] > 0:
                if self.pos_buy > 0:
                    real_price = sell_price(self.market_close)
                    self.tp_buy(real_price)
                else:
                    self.error = True
                    return

            if action_nums[1] > 0:
                if self.pos_sell > 0:
                    real_price = sell_price(self.market_close)
                    self.tp_sell(real_price)
                else:
                    self.error = True
                    return
        else:
            buy_factor = (action_nums[0] - action_nums[1]) / action_nums[1] if not action_nums[1] == 0 else 0
            sell_factor = (action_nums[1] - action_nums[0]) / action_nums[0] if not action_nums[0] == 0 else 0
            if buy_factor > 0.1:
                # buy
                lot = unit_lot * np.round(buy_factor * 10, decimals=0)
                real_price = buy_price(self.market_close)
                if not self.order_buy(lot, real_price):
                    self.error = True
                    return
            if sell_factor > 0.1:
                # sell
                lot = unit_lot * np.round(sell_factor * 10, decimals=0)
                real_price = sell_price(self.market_close)
                if not self.order_sell(lot, real_price):
                    self.error = True
                    return

        self.lived_ticks += 1
        return


def test():
    a = Account(10000, 0.75, verbose=True)
    print(a)

    a.tick_market([0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    # buy 0.03
    a.act([0., 0., 2., 1.])
    print(a)

    a.tick_market([0, 120., 121., 119.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    # tp
    a.act([1., 0., 0., 0.])
    print(a)

    a.tick_market([0, 120., 121., 121.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    # tp
    a.act([0., 0., 3., 4.])
    print(a)

    a.tick_market([0, 120., 121., 122.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    # tp
    a.act([0., 1., 0., 0.])
    print(a)

# test()
