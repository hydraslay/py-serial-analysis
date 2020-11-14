from copy import deepcopy

import numpy as np

from evo import visualize


class MonoPredictor(object):
    # state (10): [
    #      0~4   open,hi,low,close,volume(fast tick)
    #      5~9   open,hi,low,close,volume(slow tick)
    # direction:
    # 0: for down
    # 1: for up
    def __init__(self, direction, verbose=False, no_predict=400):
        self.direction = direction
        self.state = np.zeros(10)
        self.no_predict = no_predict
        self.verbose = verbose
        self.score = 0.
        self.total_ticks = 0
        self.pred_ticks = 0
        self.actual_history = None
        self.predict_history = None
        self.threshold = 0
        self.win_rate = 0

    def __repr__(self):
        return ' direction: {}' \
               ' threshold: {} ' \
               ' win rate: {} ' \
               ' pred_ticks : {} '.format(self.direction, self.threshold, self.win_rate, self.pred_ticks)

    def get_data(self):
        d = self.state
        # (hi - close) / close, (close - low) / close, close, volume
        # for fast and slow ticks
        if d[3] == 0:
            print('error data: not zero')
        return [
            (d[1] - d[3]) / d[3],
            (d[3] - d[2]) / d[3],
            d[3],
            d[4],
        ]

    @property
    def market_open(self):
        return np.array(self.state[0])

    @property
    def market_close(self):
        return np.array(self.state[3])

    # threshold > 0: minimum confidence to keep predict 100% correct
    # score = win rate (this part can bu tuned to utilize training)
    def calc_score(self):
        ticks = []
        self.pred_ticks = 0
        for j in range(len(self.actual_history) - self.no_predict):
            i = j + self.no_predict
            self.pred_ticks += 1
            act = self.actual_history[i]
            confidence = self.predict_history[i]
            result = 0.
            if act[0] > act[1] and self.direction == 0:
                result = 1.
            if act[0] < act[1] and self.direction == 1:
                result = 1.
            ticks.append([confidence, result])

        sorted_by_confidence = sorted(ticks, key=lambda t: -t[0])
        threshold = 0
        correct_predict = 0
        same_confidence = {}
        for i in range(len(sorted_by_confidence)):
            if sorted_by_confidence[i][1] == 1.:
                threshold = sorted_by_confidence[i][0]
                if threshold in same_confidence:
                    same_confidence[threshold] += 1
                else:
                    same_confidence[threshold] = 1
                correct_predict += 1
            else:
                # failed: but same confidence with some correct
                if threshold in same_confidence:
                    correct_predict -= same_confidence[threshold]
                break
        self.threshold = threshold
        self.win_rate = correct_predict / self.pred_ticks
        self.score = self.win_rate
        if self.verbose:
            print('score calculated: {}'.format(self.score))

        return self.score

    #  add actual data, calc score
    def tick_market(self, market):
        if isinstance(market, np.ndarray):
            market_info = market
        else:
            if isinstance(market, list):
                market_info = np.array(market)
            else:
                raise TypeError('{} is not supported', format(type(market)))

        self.state[0:] = market_info

        self.total_ticks += 1

        if self.predict_history is not None:
            if self.actual_history is None:
                self.actual_history = [[self.market_open.tolist(), self.market_close.tolist()]]
            else:
                self.actual_history.append([self.market_open.tolist(), self.market_close.tolist()])

    # pred_nums -->
    #   [0] >= [1] : up
    #   [1] > [0] : down
    #   | [0] - [1] | : confidential
    def predict(self, pred_nums):
        if self.predict_history is None:
            self.predict_history = pred_nums
        else:
            self.predict_history.append(pred_nums[0])

        return


def test():
    a = MonoPredictor(0, verbose=True, no_predict=200)

    a.tick_market([120., 121., 120.000, 121., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.61])
    a.tick_market([121., 121., 120.000, 122., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.54])
    a.tick_market([122., 121., 120.000, 123., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.53])

    for _ in range(100):
        a.tick_market([123., 121., 120.000, 122., 10, 120., 121., 120.000, 120, 10])
        a.predict([0.52])
        a.tick_market([120., 121., 125.000, 125., 10, 120., 121., 120.000, 120, 10])
        a.predict([0.52])

    a.tick_market([125., 121., 120.000, 124., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.18])
    a.tick_market([124., 121., 128.000, 128., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.491])

    a.calc_score()
    print(a)

    visualize.plot_mono_predictions(a.direction, np.array(a.actual_history), np.array(a.predict_history),
                                    a.threshold, a.no_predict, True)


# test()
