import unittest
import weakref
import numpy as np
import contextlib
from memory_profiler import profile


class Config:
    enable_back_prop = True


@contextlib.contextmanager
def using_config(name, value):
    old_value = getattr(Config, name)
    setattr(Config, name, value)
    try:
        yield
    finally:
        setattr(Config, name, old_value)


def no_grad():
    return using_config("enable_back_prop", False)


def as_array(x):
    if np.isscalar(x):
        return np.array(x)
    return x


def as_variable(obj):
    if isinstance(obj, Variable):
        return obj
    return Variable(obj)


class Variable:
    __array_priority__ = 200

    def __init__(self, data_in, name=None):
        if data_in is not None:
            if not isinstance(data_in, np.ndarray):
                raise TypeError('{} is not supported', format(type(data_in)))

        self.data = data_in
        self.name = name
        self.grad = None
        self.creator = None
        self.generation = 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        if self.data is None:
            return 'variable(None)'
        p = str(self.data).replace('\n', '\n' + ' ' * 9)
        return 'variable(' + p + ')'

    @property
    def shape(self):
        return self.data.shape

    @property
    def ndim(self):
        return self.data.ndim

    @property
    def size(self):
        return self.data.size

    @property
    def dtype(self):
        return self.data.dtype

    def set_creator(self, func):
        self.creator = func
        self.generation = func.generation + 1

    def backward(self, retain_grad = False):
        if self.grad is None:
            self.grad = np.ones_like(self.data)

        funcs = []
        seen_set = set()

        def add_func(f):
            if f not in seen_set:
                funcs.append(f)
                seen_set.add(f)
                funcs.sort(key=lambda x: x.generation)

        add_func(self.creator)

        while funcs:
            f = funcs.pop()
            gys = [output().grad for output in f.outputs]
            gxs = f.backward(*gys)
            if not isinstance(gxs, tuple):
                gxs = (gxs,)

            for x, gx in zip(f.inputs, gxs):
                if x.grad is None:
                    x.grad = gx
                else:
                    x.grad = x.grad + gx
                if x.creator is not None:
                    add_func(x.creator)

            if not retain_grad:
                for y in f.outputs:
                    y().grad = None


class Function:
    def __call__(self, *inputs):
        inputs = [as_variable(x) for x in inputs]
        xs = [x.data for x in inputs]
        ys = self.forward(*xs)
        if not isinstance(ys, tuple):
            ys = (ys,)
        outputs = [Variable(as_array(y)) for y in ys]
        if Config.enable_back_prop:
            self.generation = max([x.generation for x in inputs])
            for output in outputs:
                output.set_creator(self)
            self.inputs = inputs
            self.outputs = [weakref.ref(output) for output in outputs]
        return outputs if len(outputs) > 1 else outputs[0]

    def forward(self, x):
        raise NotImplementedError()

    def backward(self, gy):
        raise NotImplementedError()


class Add(Function):
    def forward(self, a, b):
        return a + b

    def backward(self, gy):
        return gy, gy


class Mul(Function):
    def forward(self, a, b):
        return a * b

    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return gy * x1, gy * x0


class Square(Function):
    def forward(self, x):
        return x ** 2

    def backward(self, gy):
        x = self.inputs[0].data
        return gy * 2 * x


class Neg(Function):
    def forward(self, x):
        return -x

    def backward(self, gy):
        return -gy


class Sub(Function):
    def forward(self, x0, x1):
        return x0 - x1

    def backward(self, gy):
        return gy, -gy


class Div(Function):
    def forward(self, x0, x1):
        return x0 / x1

    def backward(self, gy):
        x0, x1 = self.inputs[0].data, self.inputs[1].data
        return gy / x1, gy * (-x0 / x1 ** 2)


class Pow(Function):
    def __init__(self, c):
        self.c = c

    def forward(self, x):
        return x ** self.c

    def backward(self, gy):
        x = self.inputs[0].data
        c = self.c
        return c * x ** (c - 1) * gy


def add(a, b):
    return Add()(a, as_array(b))


def mul(a, b):
    return Mul()(a, as_array(b))


def neg(a):
    return Neg()(a)


def sub(a, b):
    return Sub()(a, as_array(b))


def rsub(a, b):
    return Sub()(as_array(b), a)


def div(x0, x1):
    return Div()(x0, as_array(x1))


def rdiv(x0, x1):
    return Div()(as_array(x1), x0)


def pow(x, c):
    return Pow(c)(x)


def square(x):
    return Square()(x)


Variable.__add__ = add
Variable.__radd__ = add
Variable.__mul__ = mul
Variable.__rmul__ = mul
Variable.__neg__ = neg
Variable.__sub__ = sub
Variable.__rsub__ = rsub
Variable.__div__ = div
Variable.__rdiv__ = rdiv
Variable.__pow__ = pow


@profile
def main():
    # x = Variable(np.array(2.0))
    # a = square(x)
    # y = add(square(a), square(a))
    # y.backward()
    # print(y.data)
    # print(x.grad)
    #
    # with no_grad():
    #     m = Variable(np.array(3.0))
    #     n = add(square(m), square(m))
    #     print(n.data)


    # for i in range(10):
    #     x1 = Variable(np.random.randn(10000))
    #     y1 = square(square(square(x1)))
    #     y1.backward()
    #     print(x1.grad)

    a = Variable(np.array(3))
    b = Variable(np.array(2))
    c = Variable(np.array(1))
    y = - a + np.array([20]) * b ** 5
    y.backward()

    print(y)
    print(a.grad)
    print(b.grad)
main()