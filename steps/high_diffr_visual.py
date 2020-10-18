import numpy as np
import matplotlib.pyplot as plt
from dezero import Variable, plot_dot_graph
import dezero.functions as F

x = Variable(np.array(1.0), 'x')
y = F.tanh(x)
y.name = 'y'
y.backward(create_graph=True)

iters = 3

for i in range(iters):
    gx = x.grad
    x.cleargrad()
    gx.backward(create_graph=True)

gx = x.grad
gx.name = 'gx' + str(iters + 1)
plot_dot_graph(gx, verbose=False, to_file='tanh.png')
