import numpy as np
from dezero import Variable
import dezero.functions as F
from dezero.utils import sum_to

x = Variable(np.random.randn(2, 3))
W = Variable(np.random.randn(3, 4))


y = F.matmul(x, W)
y.backward()

print(x.grad.shape)
print(W.grad.shape)

print(x / 2.0)
