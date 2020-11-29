import numpy as np
from dezero import Variable
from dezero.models import Model, MLP
import dezero.layers as L
import dezero.functions as F
import dezero.optimizers as O


np.random.seed(1)
x = np.random.rand(100, 1)
y = np.sin(2 * np.pi * x) + np.random.rand(100, 1)
model = MLP((10, 10, 1))
model.plot(x)


lr = 0.1
iters = 20000

optimizer = O.Adam(lr).setup(model)


for i in range(iters):
    y_pred = model(x)
    loss = F.mean_squared_error(y, y_pred)

    model.cleargrads()
    loss.backward()

    optimizer.update()

    if i % 1000 == 0:
        print(loss)
