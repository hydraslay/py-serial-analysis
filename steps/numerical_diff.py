import unittest

import numpy as np


def as_array(x):
    if np.isscalar(x):
        return np.array(x)
    return x


class Variable:
    def __init__(self, data_in):
        if data_in is not None:
            if not isinstance(data_in, np.ndarray):
                raise TypeError('{} is not supported', format(type(data_in)))

        self.data = data_in
        self.grad = None
        self.creator = None

    def set_creator(self, func):
        self.creator = func

    def backward(self):
        if self.grad is None:
            self.grad = np.ones_like(self.data)

        funcs = [self.creator]
        while funcs:
            f = funcs.pop()
            x, y = f.input, f.output
            x.grad = f.backward(y.grad)
            if x.creator is not None:
                funcs.append(x.creator)


class Function:
    def __call__(self, input):
        x = input.data
        y = self.forward(x)
        output = Variable(as_array(y))
        output.set_creator(self)
        self.input = input
        self.output = output
        return output

    def forward(self, x):
        raise NotImplementedError()

    def backward(self, gy):
        raise NotImplementedError()


class Square(Function):
    def forward(self, x):
        return x ** 2

    def backward(self, gy):
        x = self.input.data
        return gy * 2 * x


class Exp(Function):
    def forward(self, x):
        return np.exp(x)

    def backward(self, gy):
        x = self.input.data
        return gy * np.exp(x)


def square(x):
    return Square()(x)


def exp(x):
    return Exp()(x)


# 数値微分
def numerical_diff(f, x, eps=1e-4):
    x0 = Variable(np.array(x.data - eps))
    x1 = Variable(np.array(x.data + eps))
    y0 = f(x0)
    y1 = f(x1)
    return (y1.data - y0.data) / (2 * eps)


def f(x):
    return square(exp(square(x)))


# back propagation
def back_prop(gy):

    x = Variable(np.array(gy))
    y = square(exp(square(x)))
    y.backward()
    return x.grad


# 数値微分
print(numerical_diff(f, Variable(np.array(1))))


# back propagation
print(back_prop(1))

