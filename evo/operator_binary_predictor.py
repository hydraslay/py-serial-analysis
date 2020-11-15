from copy import deepcopy

import numpy as np

from evo import visualize


class BinaryPredictor(object):
    # state (10): [
    #      0     open,
    #      1     hi,
    #      2     low,
    #      3     close,
    #      4     volume
    #      5     open,
    #      6     hi,
    #      7     low,
    #      8     close,
    #      9     volume
    #           ]
    def __init__(self, verbose=False):
        self.state = np.zeros(10)
        self.no_predict = 400
        self.verbose = verbose
        self.score = 0.
        self.total_ticks = 0
        self.pred_ticks = 0
        self.actual_history = None
        self.predict_history = None
        self.threshold = 0
        self.win_rate = 0

    def __repr__(self):
        return ' score: {}' \
               ' threshold: {} ' \
               ' win rate: {} ' \
               ' pred_ticks : {} '.format(self.score, self.threshold, self.win_rate, self.pred_ticks)

    def get_data(self):
        return self.state

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
        for j in range(len(self.actual_history) - self.no_predict):
            i = j + self.no_predict
            self.pred_ticks += 1
            pred = self.predict_history[i]
            act = self.actual_history[i]
            predict = pred[0] - pred[1]
            confidence = np.abs(predict)
            result = 1. if (pred[0] > pred[1] and act[0] > act[1]) or (pred[0] < pred[1] and act[0] < act[1]) else 0.
            ticks.append([
                confidence,
                result
            ])

        sorted_by_confidence = sorted(ticks, key=lambda t: -t[0])
        threshold = 0
        correct_predict = 0
        for i in range(len(sorted_by_confidence)):
            if sorted_by_confidence[i][1] == 1.:
                threshold = sorted_by_confidence[i][0]
                correct_predict += 1
            else:
                break
        self.threshold = threshold
        self.win_rate = correct_predict / self.pred_ticks
        # score = -self.threshold + self.win_rate + (1 if self.win_rate > 0 else 0)
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

        self.state[0:] = deepcopy(market_info)

        self.total_ticks += 1

        if self.predict_history is not None:
            if self.actual_history is None:
                self.actual_history = [[self.market_open.tolist(), self.market_close.tolist()]]
            else:
                self.actual_history.append([self.market_open, self.market_close])

    # pred_nums -->
    #   [0] >= [1] : up
    #   [1] > [0] : down
    #   | [0] - [1] | : confidence
    def predict(self, pred_nums):
        if self.predict_history is None:
            self.predict_history = [pred_nums]
        else:
            self.predict_history.append(pred_nums)

        return


def test():
    a = BinaryPredictor(verbose=True)

    a.tick_market([120., 121., 120.000, 121., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.51, 0.49])
    a.tick_market([121., 121., 120.000, 122., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.54, 0.45])
    a.tick_market([122., 121., 120.000, 123., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.53, 0.47])

    for _ in range(150):
        a.tick_market([123., 121., 120.000, 122., 10, 120., 121., 120.000, 120, 10])
        a.predict([0.52, 0.46])
        a.tick_market([120., 121., 123.000, 122., 10, 120., 121., 120.000, 120, 10])
        a.predict([0.52, 0.46])

    a.tick_market([123., 121., 120.000, 121., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.48, 0.49])
    a.tick_market([121., 121., 120.000, 120., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.491, 0.496])

    a.calc_score()
    print(a)

    visualize.plot_binary_predictions(a.actual_history, a.predict_history, a.threshold, a.no_predict, True)

# test()
