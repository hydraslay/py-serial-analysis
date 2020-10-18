from dezero.functions import rosenbrock

if '__file__' in globals():
    import os, sys

    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import numpy as np
# should use is_simple_core = True in dezero/__init__.py
from dezero import Variable


x0 = Variable(np.array(1.5), 'x0')
x1 = Variable(np.array(0.5), 'x1')
lr = 0.0001
iters = 1000

for i in range(iters):

    y0 = rosenbrock(x0, x1)
    x0.cleargrad()
    x1.cleargrad()
    y0.backward()

    x0.data -= lr * x0.grad
    x1.data -= lr * x1.grad

print(x0, x1)
