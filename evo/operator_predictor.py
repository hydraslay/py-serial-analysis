from copy import deepcopy

import numpy as np


class Predictor(object):
    # state (15): [
    #      0     open,
    #      1     hi,
    #      2     low,
    #      3     close,
    #      4     volume
    #      ...
    #           ]
    def __init__(self, n, prev, verbose=False):
        self.state = np.zeros(15)
        self.N = n
        self.prev = prev
        #  g0 [p1  p2  p3]
        #  g1 [p1  p2  p3]
        #  g2 [p1  p2  p3]
        self.predict_mat = np.zeros((n, n))
        #  [a1  a2  a3]
        self.actual_arr = np.zeros(n)
        self.verbose = verbose
        self.score = 0
        self.total_ticks = 0
        self.pred_ticks = 0
        # more score for further ticks (multiply times per tick)
        # 2.15443469 : x ^ (1+2+3) = 100 for N = 4
        # self.future_factor = 2.15443469
        self.finalized = False
        self.actual_history = None
        self.predict_history = None

    def __repr__(self):
        if self.pred_ticks == 0:
            return 'not start predict'

        return ' avg score: {}' \
               ' total_ticks: {} ' \
               ' pred_ticks : {} '.format(self.score / self.pred_ticks, self.total_ticks, self.pred_ticks)

    def get_data(self):
        return self.state

    def final_evaluate(self):
        if self.finalized:
            raise RuntimeError('should not call final_evaluate twice')
        # evaluate partial unknown ticks
        # for i in range(self.N - 1):
        #     self.score += self.calc_score(i + 1)
        #     self.pred_ticks += 1
        self.finalized = True
        return self.score / self.pred_ticks

    @property
    def market_close(self):
        return np.array(self.state[3])

    def calc_score(self, index):
        arr = self.predict_mat[index]
        score = 0
        # ticks
        for i in range(len(arr) - index):
            # actual index (offset for those partially confirmed ticks)

            a_index = i + index
            diff = np.min([arr[i] - self.actual_arr[a_index], self.actual_arr[a_index] - arr[i]])
            score += diff
            # method: divide * multiply
            # should --> 1 and always 0 < y <= 1
            # divided = np.min([abs(arr[i] / self.actual_arr[a_index]), abs(self.actual_arr[a_index] / arr[i])])
            # score *= divided ** 4
            # score *= self.future_factor ** i

        if self.verbose:
            print('score calculated: {}'.format(score))
        return score

    #  add actual data, calc score
    #      *
    #  g0  a0  a1  a2
    #      p1  p2  p3
    #  g1      a0  a1  a2
    #          p1  p2  p3
    #  g2          a0  a1  a2
    #              p1  p2  p3
    def tick_market(self, market):
        if isinstance(market, np.ndarray):
            market_info = market
        else:
            if isinstance(market, list):
                market_info = np.array(market)
            else:
                raise TypeError('{} is not supported', format(type(market)))

        self.state[0:] = deepcopy(market_info)
        self.actual_arr[0: self.N - 1] = self.actual_arr[1: self.N]
        self.actual_arr[self.N - 1] = self.market_close
        self.total_ticks += 1

        if self.verbose:
            if self.actual_history is None:
                self.actual_history = np.array([self.market_close])
            else:
                self.actual_history = np.concatenate([self.actual_history, [self.market_close]])

    # action_bits -->
    #   next N tick ratio to previous tick
    def predict(self, pred_nums):
        if self.total_ticks >= self.prev:
            # move prev predicts
            self.predict_mat[0: self.N - 1] = self.predict_mat[1: self.N]
            # set current predict
            # + 0.5: move sigmoid(0~1) to (0.5~1.5)
            predicted_value = (np.array(pred_nums) + 0.5) * self.market_close
            self.predict_mat[self.N - 1] = predicted_value

        # evaluate finished predicts
        if self.predict_mat[0, 0] != 0:
            self.score += self.calc_score(0)
            self.pred_ticks += 1

            if self.verbose:
                if self.predict_history is None:
                    self.predict_history = []
                combined = deepcopy(self.actual_history.tolist())
                combined.extend(self.predict_mat[0].tolist())
                self.predict_history.append(combined)

        return


def test():
    a = Predictor(4, 1, verbose=True)
    print(a)

    a.tick_market([0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    a.predict([0.51, 0.50, 0.49, 0.48])
    print(a)

    a.tick_market([0, 120., 121., 119.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    a.predict([0.54, 0.54, 0.49, 0.45])
    print(a)

    a.tick_market([0, 120., 121., 121.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    a.predict([0.53, 0.53, 0.47, 0.47])
    print(a)

    a.tick_market([0, 120., 121., 122.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    a.predict([0.52, 0.52, 0.45, 0.46])
    print(a)

    a.tick_market([0, 120., 121., 122.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    a.predict([0.50, 0.51, 0.48, 0.49])

    print(a)

    a.tick_market([0, 120., 121., 122.000, 10, 0, 120., 121., 120.000, 10, 0, 120., 121., 120.000, 10])
    a.predict([0.499, 0.501, 0.491, 0.496])

    print(a)

    a.final_evaluate()
    print(a)

# test()
