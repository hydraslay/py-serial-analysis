import numpy as np
from dezero.models import MLP
import dezero.functions as F

x = np.array([[0.2, -0.4], [0.3, 0.5], [1.3, -3.2], [2.1, 0.3]])
t = np.array([1, 0, 1, 0])
model = MLP((10, 3))
y = model(x)
loss = F.softmax_cross_entropy_simple(y, t)
print(loss)
