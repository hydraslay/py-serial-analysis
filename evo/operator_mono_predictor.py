import numpy as np
from evo import visualize


class MonoPredictor(object):
    # state (10): [
    #      0~4   open,hi,low,close,volume(fast tick)
    #      5~9   open,hi,low,close,volume(slow tick)
    # direction:
    # 0: for down
    # 1: for up
    def __init__(self, direction, verbose=False, no_predict=400, threshold=100, max_low_confidence_tick=10):
        self.direction = direction
        self.state = np.zeros(10)
        self.no_predict = no_predict
        self.verbose = verbose
        self.pred_ticks = 0.
        self.total_ticks = 0
        self.actual_history = None
        self.predict_history = None
        self.threshold = threshold
        self.low_confidence_tick = 0
        self.max_low_confidence_tick = max_low_confidence_tick
        self.latest_predict = 0

    def __repr__(self):
        return ' direction: {}' \
               ' score : {} '.format(self.direction, self.score)

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

    @property
    def score(self):
        #
        strong_predicts = 0
        for j in range(len(self.predict_history) - self.no_predict):
            i = j + self.no_predict
            if self.predict_history[i] > self.threshold:
                strong_predicts += 1

        return self.pred_ticks + strong_predicts / (len(self.predict_history) - self.no_predict)

    # add actual data, calc score
    # -1: too many low confidence
    # 0: predict wrong
    # 1: predict correct
    # 2: low confidence
    # 3: no predict
    # <= 0 should make train stop
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

        if self.total_ticks > self.no_predict + 1:
            self.pred_ticks += 1
            if self.latest_predict > self.threshold:
                # confidence strong
                if (self.market_open < self.market_close and self.direction == 1) \
                        or (self.market_open > self.market_close and self.direction == 0):
                    # correct predict
                    self.low_confidence_tick = 0
                    return 1
                else:
                    return 0
            else:
                # confidence low
                self.low_confidence_tick += 1
                if self.low_confidence_tick > self.max_low_confidence_tick:
                    return -1
                else:
                    return 2
        else:
            #  no predict
            return 3

    # pred_nums -->
    #   [0] : confidence
    def predict(self, pred_nums):
        self.latest_predict = pred_nums[0]
        if self.predict_history is None:
            self.predict_history = pred_nums
        else:
            self.predict_history.append(pred_nums[0])

        return


def test():
    a = MonoPredictor(1, verbose=True, no_predict=10)

    a.tick_market([120., 121., 120.000, 121., 10, 120., 121., 120.000, 120, 10])
    a.predict([0.61])
    print(a.tick_market([121., 121., 120.000, 122., 10, 120., 121., 120.000, 120, 10]))
    a.predict([0.54])
    print(a.tick_market([122., 121., 120.000, 123., 10, 120., 121., 120.000, 120, 10]))
    a.predict([0.53])

    for _ in range(5):
        print(a.tick_market([123., 121., 120.000, 122., 10, 120., 121., 120.000, 120, 10]))
        a.predict([0.52])
        print(a.tick_market([120., 121., 125.000, 125., 10, 120., 121., 120.000, 120, 10]))
        a.predict([0.59])

    print(a.tick_market([125., 121., 120.000, 124., 10, 120., 121., 120.000, 120, 10]))
    a.predict([100.18])
    print(a.tick_market([124., 121., 128.000, 128., 10, 120., 121., 120.000, 120, 10]))
    a.predict([0.491])

    print(a)

    visualize.plot_mono_predictions(a.direction, np.array(a.actual_history), np.array(a.predict_history),
                                    a.threshold, a.no_predict, True)

# test()
